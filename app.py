"""Local tool boundary. Tokens represent fixture admission, not authenticated users."""
import json, threading, time, uuid
from dataclasses import dataclass

class Denied(ValueError): pass

@dataclass
class Grant:
    tool: str
    expires: float
    remaining: int

class Gateway:
    def __init__(self, clock=time.monotonic):
        self.clock = clock
        self.lock = threading.Lock()
        self.grants = {}
        self.tools = {'uppercase': lambda args: {'text': args['text'].upper()}}
        self.audit = []

    def admit_fixture(self, tool, ttl=30, budget=1):
        if tool not in self.tools or type(budget) is not int or budget < 1 or type(ttl) not in (int, float) or not 0 < ttl <= 300:
            raise Denied('GRANT_INVALID')
        token = uuid.uuid4().hex
        with self.lock: self.grants[token] = Grant(tool, self.clock() + ttl, budget)
        return token

    def call(self, token, tool, args):
        with self.lock:
            grant = self.grants.get(token)
            reason = None
            if grant is None: reason = 'UNKNOWN_GRANT'
            elif grant.tool != tool: reason = 'TOOL_SCOPE'
            elif self.clock() >= grant.expires: reason = 'EXPIRED'
            elif grant.remaining <= 0: reason = 'BUDGET_EXHAUSTED'
            elif not isinstance(args, dict) or set(args) != {'text'} or not isinstance(args['text'], str) or len(args['text']) > 4096: reason = 'ARGS_INVALID'
            if reason:
                self.audit.append({'status': 'DENIED', 'reason': reason})
                raise Denied(reason)
            grant.remaining -= 1  # Reserve before leaving the gate, even if adapter fails.
            self.audit.append({'status': 'DISPATCHED', 'tool': tool})
        try:
            result = self.tools[tool](args)
        except Exception:
            with self.lock: self.audit.append({'status': 'OUTCOME_UNKNOWN', 'tool': tool})
            raise
        with self.lock: self.audit.append({'status': 'ACKNOWLEDGED', 'tool': tool})
        return result

def demo():
    g = Gateway()
    token = g.admit_fixture('uppercase')
    result = g.call(token, 'uppercase', {'text': 'scoped tool invocation'})
    try: g.call(token, 'uppercase', {'text': 'retry'})
    except Denied as e: denied = str(e)
    return {'result': result, 'replay_denied': denied, 'audit': g.audit, 'authenticated_owner': False}

if __name__ == '__main__': print(json.dumps(demo(), indent=2))
