# Contract pack v1

Admission grants one named tool for <=300 seconds and a positive call budget. Arguments require exactly one bounded text field. Budget is reserved under a thread lock before adapter entry. Adapter failure consumes the budget and records OUTCOME_UNKNOWN.

## Interfaces and failure behavior

Read the public functions in `app.py` together with the tests. Invalid admission/task input raises `ValueError`; gateway denial raises `Denied`, runtime replay raises `Blocked`. The eval demo exits 1 if any labelled fixture fails. The other demos demonstrate expected refusals and exit 0 when the walkthrough completes.

## Trust boundary

The host process, code and local data are trusted. Source binding, durable state, and admission are distinct from identity authentication and world verification. No successful return establishes production authority.

## Schema evolution

This v1 lab has no automatic migration. Change the contracts and their rejection tests together; use a new fixture database for incompatible runtime changes.

## Gateway API

`admit_fixture(tool: str, ttl: number = 30, budget: int = 1)` returns a random process-local fixture token. Only the registered `uppercase` tool is available by default. TTL is finite and greater than zero, at most 300 seconds; budget is a positive integer and booleans are rejected.

`call(token: str, tool: str, args: dict)` accepts exactly `{"text": <string <=4096 characters>}`. Default result: `{"text": <uppercase string>}`. The grant must exist, match the tool, remain unexpired, and have remaining budget. On denial, no adapter runs and no budget is reserved. On admitted adapter failure the reserved budget stays consumed.

Stable denials: `GRANT_INVALID`, `UNKNOWN_GRANT`, `TOOL_SCOPE`, `EXPIRED`, `BUDGET_EXHAUSTED`, `ARGS_INVALID`. Audit entries contain status, tool or reason only; tokens and argument text are omitted. Audit is in-memory and records DISPATCHED before invocation. The lock protects admission and budget reservation across local threads, not across processes.
