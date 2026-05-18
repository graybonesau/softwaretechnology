import unittest
import time

from modules.graphs.grid_path_counter import CountGridPaths


class TestCountGridPaths(unittest.TestCase):

    def test_1x1(self):
        self.assertEqual(CountGridPaths(1, 1), 1)

    def test_2x2(self):
        self.assertEqual(CountGridPaths(2, 2), 2)

    def test_3x3(self):
        self.assertEqual(CountGridPaths(3, 3), 6)

    def test_single_row(self):
        self.assertEqual(CountGridPaths(1, 10), 1)

    def test_single_column(self):
        self.assertEqual(CountGridPaths(10, 1), 1)

    def test_known_values(self):
        cases = [
            (2, 3, 3),
            (3, 2, 3),
            (4, 4, 20),
            (5, 5, 70),
        ]

        for r, c, expected in cases:
            self.assertEqual(CountGridPaths(r, c), expected)

    def test_step_fn_called(self):

        calls = []

        def step_fn(dp, r, c):
            calls.append((r, c))

        CountGridPaths(3, 3, step_fn=step_fn)

        self.assertEqual(len(calls), 9)
        self.assertEqual(calls[-1], (2, 2))

    def test_step_fn_final_value(self):

        seen = []

        def step_fn(dp, r, c):
            seen.append(dp[r][c])

        CountGridPaths(3, 3, step_fn=step_fn)

        self.assertEqual(seen[-1], 6)

    def test_benchmark(self):

        size = 1000

        start = time.time()

        result = CountGridPaths(size, size)

        elapsed = time.time() - start

        print(f"The grid path counter benchmark of traversing a {size*size:,} cell grid took {elapsed:.4f} seconds.")


if __name__ == "__main__":
    unittest.main()