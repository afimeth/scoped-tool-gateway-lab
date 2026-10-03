# Architecture

`Fixture admission -> scope/expiry/argument/budget gate -> reserved dispatch -> adapter -> audit`

`app.py` contains the complete executable path. `tests/test_app.py` exercises success and refusal paths. Fixtures are synthetic. The CI matrix runs unit tests and demo on Linux/Windows and Python 3.11/3.14.

## Design and tradeoffs

Admission grants one named tool for <=300 seconds and a positive call budget. Arguments require exactly one bounded text field. Budget is reserved under a thread lock before adapter entry. Adapter failure consumes the budget and records OUTCOME_UNKNOWN.

The small implementation favors an inspectable boundary over breadth. No external dependency or remote execution participates in the demo.

## Operational limitations

No MCP wire protocol, network listener, authenticated principal, persistent grants/audit, cryptographic authority, distributed budget, or sandbox isolation. In-process Python code can mutate grants/tools; trusted callers only. Fixture admission is deliberately available locally and is not an authorization service.
