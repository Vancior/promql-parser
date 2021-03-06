import unittest

from promql_ast import recur_add_label
from yacc import parser


class MyTestCase(unittest.TestCase):
    def test_a(self):
        root = parser.parse('cpu')
        recur_add_label(root, 'userId', '"3"')
        return self.assertEqual(str(root), 'cpu{userId="3"}')

    def test_b(self):
        root = parser.parse('cpu{cluster="C-123"}[5m]')
        recur_add_label(root, 'userId', '"3"')
        return self.assertEqual(str(root), 'cpu{cluster="C-123",userId="3"}[5m]')

    def test_c(self):
        root = parser.parse('count(instance_cpu_time_ns) by (app)')
        recur_add_label(root, 'userId', '"3"')
        return self.assertEqual(str(root), 'count(instance_cpu_time_ns{userId="3"})by(app)')

    def test_d(self):
        root = parser.parse('100 - avg(irate(node_cpu_seconds_total{jmode="idle"}[5m])) by (instance) * 100')
        recur_add_label(root, 'userId', '"3"')
        return self.assertEqual(str(root),
                                '100-avg(irate(node_cpu_seconds_total{jmode="idle",userId="3"}[5m]))by(instance)*100')

    def test_e(self):
        root = parser.parse('topk(3, sum(rate(instance_cpu_time_ns[5m])) by (app, proc))')
        recur_add_label(root, 'userId', '"3"')
        return self.assertEqual(str(root), 'topk(3,sum(rate(instance_cpu_time_ns{userId="3"}[5m]))by(app,proc))')


if __name__ == '__main__':
    unittest.main()
