from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

from logistics_container_agents.agents import AGENT_ROSTER
from logistics_container_agents.domain.models import BookingRequest, WorkflowResult
from logistics_container_agents.ensemble.runner import EnsembleRunner
from logistics_container_agents.llm.config import LLMConfigError
from logistics_container_agents.llm.factory import create_llm_provider


def _load_request(path: str | None) -> BookingRequest:
    if path:
        raw = Path(path).read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()
    data = json.loads(raw)
    return BookingRequest.model_validate(data)


def cmd_agents_list(_: argparse.Namespace) -> int:
    for cls in AGENT_ROSTER:
        print(f"- {cls.role} -> {cls.output_schema.__name__}")
    return 0


async def cmd_book(args: argparse.Namespace) -> int:
    try:
        llm = create_llm_provider()
    except LLMConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1

    request = _load_request(args.request)
    runner = EnsembleRunner(llm)
    result: WorkflowResult = await runner.run(request)
    print(json.dumps(result.model_dump(mode="json"), indent=2))
    return 0 if result.success else 2


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Maritime FCL container booking agent ensemble",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    book = sub.add_parser("book", help="Run booking pipeline on a JSON request file")
    book.add_argument(
        "--request",
        "-r",
        required=True,
        help="Path to BookingRequest JSON (use - for stdin)",
    )
    book.set_defaults(func=cmd_book)

    agents = sub.add_parser("agents", help="Agent commands")
    agents_sub = agents.add_subparsers(dest="agents_cmd", required=True)
    list_p = agents_sub.add_parser("list", help="List ensemble agents")
    list_p.set_defaults(func=cmd_agents_list)

    args = parser.parse_args(argv)
    if getattr(args, "request", None) == "-":
        args.request = None
    func = args.func
    if asyncio.iscoroutinefunction(func):
        return asyncio.run(func(args))
    return func(args)


if __name__ == "__main__":
    raise SystemExit(main())
