# Agent roles

Each agent returns **JSON matching a Pydantic model**. Free-form prose is not used for handoffs.

## ShipperIntakeAgent

- **Input:** raw `BookingRequest`
- **Output:** validated/enriched `BookingRequest`
- **Focus:** required fields, container types, incoterm sanity

## RoutePlanningAgent

- **Input:** `BookingRequest`, schedule tool summary
- **Output:** `RoutePlan` (legs, transit days, transshipment)
- **Focus:** feasible port pairs from mock schedules

## RateQuotingAgent

- **Input:** `BookingRequest`, `RoutePlan`, rate tool summary
- **Output:** `RateQuote` (ocean freight, surcharges, validity)
- **Focus:** rank lane rates for container type/qty

## CarrierSelectionAgent

- **Input:** `RoutePlan`, `RateQuote`, carrier options from tools
- **Output:** `CarrierOffer` (line, voyage, allocation)
- **Focus:** balance cost vs reliability score from tool data

## ComplianceAgent

- **Input:** shipper party name, cargo hazmat flag, sanctions tool result
- **Output:** `ComplianceResult` (`blocked`, `flags`, `reasons`)
- **Focus:** deny listed parties; flag hazmat for extra review

## DocumentationAgent

- **Input:** consolidated booking facts
- **Output:** `BookingDocuments` (SI draft, B/L instructions)
- **Focus:** accurate parties, ports, container, commodity

## BookingOrchestrator

- **Input:** all prior artifacts
- **Output:** `ConfirmedBooking` (reference, cut-offs, summary)
- **Focus:** single confirmed record when prior stages align

## TrackingAgent (stub)

Reserved for milestone/ETA tracking; not invoked in v1 pipeline.
