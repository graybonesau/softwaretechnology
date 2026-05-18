import unittest
import time
from modules.data_structures.linked_list import LinkedList


class TestLinkedList(unittest.TestCase):
    def test_append_popfront_benchmark(self):
        linkedlist = LinkedList()
        n = 10 ** 6
        start = time.time()
        for i in range(n):
            linkedlist.append(i)
        for i in range(n):
            linkedlist.pop_front()
        elapsed = time.time() - start
        print(f"The linked list benchmark of appending and popping {n:,} items took {elapsed:.4f} seconds.")
        self.assertTrue(linkedlist.is_empty())


if __name__ == "__main__":
    unittest.main()