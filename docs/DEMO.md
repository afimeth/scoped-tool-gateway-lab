# Demo walkthrough

1. Run `python -m unittest discover -s tests -v`.
2. Run `python app.py` and inspect the JSON.
3. Read each test containing `failure`, `replay`, `restart`, `fabricated`, `modified`, or `concurrent` to locate the negative proof.
4. Explain the conservative boundary and its limits in `CONTRACTS.md` and `EVIDENCE.md`.

Role scenario: **AI Platform / Tool Infrastructure**.

Safe CV wording: "Implemented a local capability-scoped tool gateway with expiry, atomic usage budgets, denial audit events, and concurrent replay tests."

Do not claim production deployment, real provider integration, generalized agent reliability, source truth, or MCP compatibility from this demo.
