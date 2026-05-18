import unittest
import time
import random
from modules.sorting.bubble_sort import BubbleSort


def _noop_draw(arr, compare, swap, sorted_up_to):
    pass

def _noop_wait(ms):
    pass

def _noop_events():
    return True

def run_sort(array):
    BubbleSort(array, _noop_draw, _noop_wait, _noop_events)
    return array


class TestBubbleSort(unittest.TestCase):
    def test_sorts_random(self):
        arr = [random.randint(0, 1000) for _ in range(200)]
        expected = sorted(arr)
        result = run_sort(arr)
        self.assertEqual(result, expected)

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
        BubbleSort(arr, _noop_draw, _noop_wait, _noop_events)
        self.assertIs(arr, original_ref)
        self.assertEqual(arr, [1, 2, 3])

    def test_abort_mid_sort(self):
        call_count = 0
        def abort_after_5():
            nonlocal call_count
            call_count += 1
            return call_count <= 5

        arr = [random.randint(0, 100) for _ in range(20)]
        result = BubbleSort(arr, _noop_draw, _noop_wait, abort_after_5)
        self.assertFalse(result)
        self.assertEqual(len(arr), 20)

    def test_benchmark(self):
        n = 10000
        arr = [random.randint(0, 10000) for _ in range(n)]
        start = time.time()
        run_sort(arr)
        elapsed = time.time() - start
        self.assertEqual(arr, sorted(arr))
        print(f"The bubble sort benchmark of sorting {n:,} items took {elapsed:.4f} seconds.")


if __name__ == "__main__":
    unittest.main()