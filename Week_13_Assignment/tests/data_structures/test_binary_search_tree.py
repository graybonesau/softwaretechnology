import unittest
import time
import random
from modules.data_structures.binary_search_tree import BinarySearchTree


class TestBinarySearchTree(unittest.TestCase):
    def test_insert_and_search(self):
        bst = BinarySearchTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.insert(v)
        self.assertEqual(bst.size(), 7)
        for v in [5, 3, 8, 1, 4, 7, 9]:
            self.assertTrue(bst.search(v))
        self.assertFalse(bst.search(0))
        self.assertFalse(bst.search(6))

    def test_duplicates_ignored(self):
        bst = BinarySearchTree()
        for _ in range(5):
            bst.insert(10)
        self.assertEqual(bst.size(), 1)

    def test_delete(self):
        bst = BinarySearchTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.insert(v)
        self.assertTrue(bst.delete(1))
        self.assertFalse(bst.search(1))
        self.assertEqual(bst.size(), 6)
        self.assertTrue(bst.delete(3))
        self.assertFalse(bst.search(3))
        self.assertEqual(bst.size(), 5)
        self.assertTrue(bst.delete(8))
        self.assertFalse(bst.search(8))
        self.assertEqual(bst.size(), 4)
        self.assertTrue(bst.delete(5))
        self.assertFalse(bst.search(5))
        self.assertEqual(bst.size(), 3)

    def test_delete_nonexistent(self):
        bst = BinarySearchTree()
        for v in [5, 3, 8]:
            bst.insert(v)
        self.assertFalse(bst.delete(99))
        self.assertEqual(bst.size(), 3)

    def test_traversals(self):
        bst = BinarySearchTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.insert(v)
        self.assertEqual(bst.inorder(),   [1, 3, 4, 5, 7, 8, 9])
        self.assertEqual(bst.preorder(),  [5, 3, 1, 4, 8, 7, 9])
        self.assertEqual(bst.postorder(), [1, 4, 3, 7, 9, 8, 5])

    def test_height(self):
        bst = BinarySearchTree()
        self.assertEqual(bst.height(), 0)
        bst.insert(5)
        self.assertEqual(bst.height(), 1)
        for v in [3, 8, 1]:
            bst.insert(v)
        self.assertEqual(bst.height(), 3)

    def test_empty(self):
        bst = BinarySearchTree()
        self.assertTrue(bst.is_empty())
        self.assertEqual(bst.size(), 0)
        self.assertFalse(bst.search(1))
        self.assertFalse(bst.delete(1))
        self.assertEqual(bst.inorder(),   [])
        self.assertEqual(bst.preorder(),  [])
        self.assertEqual(bst.postorder(), [])

    def test_benchmark(self):
        bst = BinarySearchTree()
        n = 10 ** 6
        values = random.sample(range(10 ** 6), n)
        start = time.time()
        for v in values:
            bst.insert(v)
        for v in values:
            bst.search(v)
        for v in values:
            bst.delete(v)
        elapsed = time.time() - start
        print(f"The binary search tree benchmark of inserting, searching, and deleting {n:,} items took {elapsed:.4f} seconds.")


if __name__ == "__main__":
    unittest.main()