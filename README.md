# Scoped Tool Gateway Lab

A small, runnable proof of work for **AI Platform / Tool Infrastructure** interviews. Standard-library Python 3.11+; no API key, installation, or external service required.

## Run in under a minute

```sh
git clone https://github.com/afimeth/scoped-tool-gateway-lab.git
cd scoped-tool-gateway-lab
python -m unittest discover -s tests -v
python app.py
```

The demo uses synthetic inputs and prints JSON. Tests fail with a nonzero exit code. The runtime demo creates and removes a temporary SQLite database; other demos operate in memory.

## What this demonstrates

Implemented a local capability-scoped tool gateway with expiry, atomic usage budgets, denial audit events, and concurrent replay tests.

Flow: `Fixture admission -> scope/expiry/argument/budget gate -> reserved dispatch -> adapter -> audit`.

See [architecture](docs/ARCHITECTURE.md), [contracts](docs/CONTRACTS.md), [evidence and limitations](docs/EVIDENCE.md), and [demo walkthrough](docs/DEMO.md).

## Boundaries

No MCP wire protocol, network listener, authenticated principal, persistent grants/audit, cryptographic authority, distributed budget, or sandbox isolation. In-process Python code can mutate grants/tools; trusted callers only. Fixture admission is deliberately available locally and is not an authorization service.

This is an interview laboratory with fixture execution. It is not a production service or an accepted release of its source project. CI results and local measurements are separate evidence.

## Provenance

The implementation is a fresh, standalone educational distillation of inspected private runtime contracts. No private source files, customer data, credentials, topology, or private project identifiers are included. The private source manifest is retained outside this public repository. No license is assigned to the original private sources; this repository grants no rights to them.

## Interview extension

Describe the failure boundary, run the denial/adversarial tests, and explain what new evidence would be needed before production use. Start with a durable audit/identity boundary, then add provider integration and measured operational behavior.
