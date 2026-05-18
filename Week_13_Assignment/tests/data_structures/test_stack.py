import unittest
import time
from modules.data_structures.stack import Stack


class TestStack(unittest.TestCase):
    def test_push_pop(self):
        s = Stack()
        for i in range(1000):
            s.push(i)
        self.assertEqual(s.size(), 1000)
        for i in reversed(range(1000)):
            v = s.pop()
        self.assertEqual(v, i)
        self.assertTrue(s.is_empty())

    def test_peek_and_exceptions(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.pop()
        with self.assertRaises(IndexError):
            s.peek()
        s.push(42)
        self.assertEqual(s.peek(), 42)
        self.assertEqual(s.size(), 1)

    def test_benchmark(self):
        s = Stack()
        start = time.time()
        n = 10 ** 6
        for i in range(n):
            s.push(i)
        for i in range(n):
            s.pop()
        elapsed = time.time() - start
        print(f"The stack benchmark of pushing and popping {n:,} items took {elapsed:.4f} seconds.")


if __name__ == "__main__":
    unittest.main()