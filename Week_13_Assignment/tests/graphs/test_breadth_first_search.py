import unittest
import time
from modules.graphs.breadth_first_search import BreadthFirstSearch


def _noop_draw(visited, frontier, current): pass
def _noop_wait(ms): pass
def _noop_events(): return True

def run_bfs(graph, start):
    visited_order = []
    def tracking_draw(visited, frontier, current):
        if current is not None:
            visited_order.append(current)
    BreadthFirstSearch(graph, start, tracking_draw, _noop_wait, _noop_events)
    return visited_order


SIMPLE = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E'],
}

LINEAR = {
    'A': ['B'],
    'B': ['A', 'C'],
    'C': ['B', 'D'],
    'D': ['C'],
}

DISCONNECTED = {
    'A': ['B'],
    'B': ['A'],
    'C': ['D'],
    'D': ['C'],
}


class TestBreadthFirstSearch(unittest.TestCase):
    def test_visits_all_connected_nodes(self):
        order = run_bfs(SIMPLE, 'A')
        self.assertEqual(set(order), set(SIMPLE.keys()))

    def test_start_node_visited_first(self):
        for start in SIMPLE:
            order = run_bfs(SIMPLE, start)
            self.assertEqual(order[0], start)

    def test_bfs_order_respects_levels(self):
        order = run_bfs(SIMPLE, 'A')
        self.assertEqual(order[0], 'A')
        self.assertIn(order[1], {'B', 'C'})
        self.assertIn(order[2], {'B', 'C'})
        for node in order[3:]:
            self.assertIn(node, {'D', 'E', 'F'})

    def test_linear_graph_order(self):
        order = run_bfs(LINEAR, 'A')
        self.assertEqual(order, ['A', 'B', 'C', 'D'])

    def test_single_node(self):
        graph = {'A': []}
        order = run_bfs(graph, 'A')
        self.assertEqual(order, ['A'])

    def test_no_node_visited_twice(self):
        order = run_bfs(SIMPLE, 'A')
        self.assertEqual(len(order), len(set(order)))

    def test_disconnected_graph_only_visits_component(self):
        order = run_bfs(DISCONNECTED, 'A')
        self.assertEqual(set(order), {'A', 'B'})
        self.assertNotIn('C', order)
        self.assertNotIn('D', order)

    def test_abort_mid_search(self):
        call_count = 0
        def abort_after_2():
            nonlocal call_count
            call_count += 1
            return call_count <= 2

        result = BreadthFirstSearch(SIMPLE, 'A', _noop_draw, _noop_wait, abort_after_2)
        self.assertFalse(result)

    def test_returns_true_on_completion(self):
        result = BreadthFirstSearch(SIMPLE, 'A', _noop_draw, _noop_wait, _noop_events)
        self.assertTrue(result)

    def test_benchmark(self):
        size  = 1000
        graph = {}
        for r in range(size):
            for c in range(size):
                node      = (r, c)
                neighbors = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < size and 0 <= nc < size:
                        neighbors.append((nr, nc))
                graph[node] = neighbors
        start = time.time()
        BreadthFirstSearch(graph, (0, 0), _noop_draw, _noop_wait, _noop_events)
        elapsed = time.time() - start
        print(f"The breadth first search benchmark of traversing a {size*size:,} node grid took {elapsed:.4f} seconds.")


if __name__ == "__main__":
    unittest.main()