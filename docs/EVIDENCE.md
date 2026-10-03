# Evidence and limitations

Measured: 2026-10-03T15:55:26.672825+00:00. Python 3.14.7, Windows local execution.

`python -m unittest discover -s tests -v`: **9 passed**, exit 0.
`python app.py`: exit 0. See [test output](../evidence/local-tests.txt) and [demo JSON](../evidence/demo.json).

This is producer-run local validation, not an independent review. GitHub CI is a separate run; inspect Actions for its actual status. No L3/L4 acceptance, live provider evidence or production validation is claimed.

No MCP wire protocol, network listener, authenticated principal, persistent grants/audit, cryptographic authority, distributed budget, or sandbox isolation. In-process Python code can mutate grants/tools; trusted callers only. Fixture admission is deliberately available locally and is not an authorization service.

Safe CV claim: "Implemented a local capability-scoped tool gateway with expiry, atomic usage budgets, denial audit events, and concurrent replay tests."
