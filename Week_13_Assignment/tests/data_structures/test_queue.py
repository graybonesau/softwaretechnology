import unittest
import time
from modules.data_structures.queue import Queue


class TestQueue(unittest.TestCase):
    def test_enqueue_dequeue(self):
        q = Queue()
        for i in range(1000):
            q.enqueue(i)
        self.assertEqual(q.size(), 1000)
        for i in range(1000):
            v = q.dequeue()
            self.assertEqual(v, i)
        self.assertTrue(q.is_empty())

    def test_peek_and_exceptions(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.dequeue()
        with self.assertRaises(IndexError):
            q.peek()
        q.enqueue(42)
        self.assertEqual(q.peek(), 42)
        self.assertEqual(q.size(), 1)

    def test_benchmark(self):
        q = Queue()
        start = time.time()
        n = 10 ** 6
        for i in range(n):
            q.enqueue(i)
        for i in range(n):
            q.dequeue()
        elapsed = time.time() - start
        print(f"The queue benchmark of enqueuing and dequeuing {n:,} items took {elapsed:.4f} seconds.")


if __name__ == "__main__":
    unittest.main()