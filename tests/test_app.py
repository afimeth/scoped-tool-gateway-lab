import concurrent.futures, unittest
from app import Gateway, Denied

class Tests(unittest.TestCase):
    def setUp(self):
        self.now = 10
        self.g = Gateway(lambda: self.now)
        self.token = self.g.admit_fixture('uppercase')
    def test_allowed(self): self.assertEqual(self.g.call(self.token, 'uppercase', {'text': 'abc'}), {'text': 'ABC'})
    def test_scope(self):
        with self.assertRaisesRegex(Denied, 'TOOL_SCOPE'): self.g.call(self.token, 'shell', {'text': 'abc'})
    def test_unknown(self):
        with self.assertRaisesRegex(Denied, 'UNKNOWN_GRANT'): self.g.call('unknown', 'uppercase', {'text': 'x'})
    def test_expired(self):
        self.now = 40
        with self.assertRaisesRegex(Denied, 'EXPIRED'): self.g.call(self.token, 'uppercase', {'text': 'x'})
    def test_replay(self):
        self.g.call(self.token, 'uppercase', {'text': 'x'})
        with self.assertRaisesRegex(Denied, 'BUDGET'): self.g.call(self.token, 'uppercase', {'text': 'x'})
    def test_args_deny_before_effect(self):
        for args in ({}, {'text': 1}, {'text': 'x', 'command': 'x'}, {'text': 'x' * 4097}):
            with self.assertRaisesRegex(Denied, 'ARGS_INVALID'): self.g.call(self.token, 'uppercase', args)
        self.assertEqual(self.g.grants[self.token].remaining, 1)
    def test_invalid_grants(self):
        for ttl, budget in ((0, 1), (301, 1), (30, True), (30, 0), (float('nan'), 1)):
            with self.assertRaises(Denied): self.g.admit_fixture('uppercase', ttl, budget)
    def test_failure_consumes_budget(self):
        def fail(args): raise RuntimeError('fixture')
        self.g.tools['uppercase'] = fail
        with self.assertRaises(RuntimeError): self.g.call(self.token, 'uppercase', {'text': 'x'})
        with self.assertRaises(Denied): self.g.call(self.token, 'uppercase', {'text': 'x'})
        self.assertEqual(self.g.audit[-2]['status'], 'OUTCOME_UNKNOWN')
    def test_concurrent_budget(self):
        def invoke(_):
            try: self.g.call(self.token, 'uppercase', {'text': 'x'}); return True
            except Denied: return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            self.assertEqual(sum(pool.map(invoke, range(20))), 1)
