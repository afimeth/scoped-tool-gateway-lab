# Scoped Tool Gateway Lab

A small, runnable capability/evidence fixture for **AI Platform / Tool Infrastructure** review. Standard-library Python 3.11+; no API key, installation, or external service required.

## Run in under a minute

```sh
git clone https://github.com/afimeth/scoped-tool-gateway-lab.git
cd scoped-tool-gateway-lab
python -m unittest discover -s tests -v
python app.py
```

The demo uses synthetic inputs and prints JSON. Tests fail with a nonzero exit code. The runtime demo creates and removes a temporary SQLite database; other demos operate in memory.

## Headless click-to-run contract

`python app.py` is the runtime entrypoint. Treat it as the headless equivalent of a click-to-run action: one invocation applies the capability gate and returns machine-readable output/audit evidence.

No UI is required or shipped. A later UI may expose the same capability bindings, but authority, scope, expiry, budget, and audit semantics remain runtime concerns.

## What this demonstrates

Implemented a local capability-scoped tool gateway with expiry, atomic usage budgets, denial audit events, and concurrent replay tests.

Flow: `Fixture admission -> scope/expiry/argument/budget gate -> reserved dispatch -> adapter -> audit`.

See [architecture](docs/ARCHITECTURE.md), [contracts](docs/CONTRACTS.md), [evidence and limitations](docs/EVIDENCE.md), and [demo walkthrough](docs/DEMO.md).

## Boundaries

No MCP wire protocol, network listener, authenticated principal, persistent grants/audit, cryptographic authority, distributed budget, or sandbox isolation. In-process Python code can mutate grants/tools; trusted callers only. Fixture admission is deliberately available locally and is not an authorization service.

This is a fixture implementation, not a production service or an accepted release of its source project. CI results and local measurements are separate evidence.

## Provenance

The implementation is a fresh, standalone educational distillation of inspected private runtime contracts. No private source files, customer data, credentials, topology, or private project identifiers are included. The private source manifest is retained outside this public repository. No license is assigned to the original private sources; this repository grants no rights to them.

## Extension boundary

Describe the authority/failure boundary, run denial and replay tests, and state what additional evidence would be required before exposing the gateway to untrusted or remote callers.
