import unittest
import time
import random
from modules.sorting.merge_sort import MergeSort


def _noop_draw(arr, compare, swap, sorted_up_to): pass
def _noop_wait(ms): pass
def _noop_events(): return True

def run_sort(array):
    MergeSort(array, _noop_draw, _noop_wait, _noop_events)
    return array


class TestMergeSort(unittest.TestCase):
    def test_sorts_random(self):
        arr = [random.randint(0, 1000) for _ in range(200)]
        self.assertEqual(run_sort(arr), sorted(arr))

    def test_already_sorted(self):
        arr = list(range(50))
        self.assertEqual(run_sort(arr), list(range(50)))

    def test_reverse_sorted(self):
        arr = list(range(100, 0, -1))
        self.assertEqual(run_sort(arr), list(range(1, 101)))

    def test_single_element(self):
        self.assertEqual(run_sort([42]), [42])

    def test_empty(self):
        self.assertEqual(run_sort([]), [])

    def test_duplicates(self):
        arr = [5, 3, 5, 1, 3, 2, 1]
        self.assertEqual(run_sort(arr), sorted(arr))

    def test_all_identical(self):
        self.assertEqual(run_sort([7] * 50), [7] * 50)

    def test_two_elements(self):
        self.assertEqual(run_sort([2, 1]), [1, 2])
        self.assertEqual(run_sort([1, 2]), [1, 2])

    def test_negative_values(self):
        arr = [random.randint(-500, 500) for _ in range(100)]
        self.assertEqual(run_sort(arr), sorted(arr))

    def test_mutates_in_place(self):
        arr = [3, 1, 2]
        original_ref = arr
        MergeSort(arr, _noop_draw, _noop_wait, _noop_events)
        self.assertIs(arr, original_ref)
        self.assertEqual(arr, [1, 2, 3])

    def test_stable(self):
        arr = [(v, i) for i, v in enumerate([3, 1, 4, 1, 5, 9, 2, 6, 5])]
        keys = [x[0] for x in arr]
        MergeSort(keys, _noop_draw, _noop_wait, _noop_events)
        self.assertEqual(keys, sorted([3, 1, 4, 1, 5, 9, 2, 6, 5]))

    def test_abort_mid_sort(self):
        call_count = 0
        def abort_after_5():
            nonlocal call_count
            call_count += 1
            return call_count <= 5

        arr = [random.randint(0, 100) for _ in range(20)]
        result = MergeSort(arr, _noop_draw, _noop_wait, abort_after_5)
        self.assertFalse(result)
        self.assertEqual(len(arr), 20)

    def test_benchmark(self):
        n = 10000
        arr = [random.randint(0, 10000) for _ in range(n)]
        expected = sorted(arr)
        start = time.time()
        run_sort(arr)
        elapsed = time.time() - start
        self.assertEqual(arr, expected)
        print(f"The merge sort benchmark of sorting {n:,} items took {elapsed:.4f} seconds.")


if __name__ == "__main__":
    unittest.main()