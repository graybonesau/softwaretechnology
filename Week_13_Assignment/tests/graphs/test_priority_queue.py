import unittest
import time

from modules.graphs.priority_queue import (
    PriorityQueue,
    Event,
)


def _noop_draw(heap, highlight_indices=None, active_event=None):
    pass


def _noop_wait(ms):
    pass


def make_queue(events):
    """
    Build a queue from (time, description) tuples.
    """
    queue = PriorityQueue()

    for t, desc in events:
        queue.insert(
            Event(t, desc),
            _noop_draw,
            _noop_wait,
        )

    return queue


class TestPriorityQueue(unittest.TestCase):

    def test_insert_single_event(self):

        queue = make_queue([
            (5, "Test Event")
        ])

        self.assertEqual(len(queue.heap), 1)
        self.assertEqual(queue.heap[0].time, 5)

    def test_extract_returns_earliest_event(self):

        queue = make_queue([
            (10, "Late"),
            (2, "Early"),
            (7, "Middle"),
        ])

        event = queue.extract_min(
            _noop_draw,
            _noop_wait,
        )

        self.assertEqual(event.time, 2)
        self.assertEqual(event.description, "Early")

    def test_heap_property_after_insertions(self):

        queue = make_queue([
            (9, "A"),
            (3, "B"),
            (6, "C"),
            (1, "D"),
            (12, "E"),
        ])

        for i in range(len(queue.heap)):

            left = 2 * i + 1
            right = 2 * i + 2

            if left < len(queue.heap):
                self.assertLessEqual(
                    queue.heap[i].time,
                    queue.heap[left].time,
                )

            if right < len(queue.heap):
                self.assertLessEqual(
                    queue.heap[i].time,
                    queue.heap[right].time,
                )

    def test_extracts_in_sorted_order(self):

        queue = make_queue([
            (8, "A"),
            (1, "B"),
            (5, "C"),
            (3, "D"),
            (10, "E"),
        ])

        extracted_times = []

        while not queue.is_empty():

            event = queue.extract_min(
                _noop_draw,
                _noop_wait,
            )

            extracted_times.append(event.time)

        self.assertEqual(
            extracted_times,
            sorted(extracted_times),
        )

    def test_duplicate_times(self):

        queue = make_queue([
            (5, "A"),
            (5, "B"),
            (5, "C"),
        ])

        extracted = []

        while not queue.is_empty():

            event = queue.extract_min(
                _noop_draw,
                _noop_wait,
            )

            extracted.append(event.time)

        self.assertEqual(extracted, [5, 5, 5])

    def test_extract_empty_queue(self):

        queue = PriorityQueue()

        result = queue.extract_min(
            _noop_draw,
            _noop_wait,
        )

        self.assertIsNone(result)

    def test_is_empty(self):

        queue = PriorityQueue()

        self.assertTrue(queue.is_empty())

        queue.insert(
            Event(1, "Hello"),
            _noop_draw,
            _noop_wait,
        )

        self.assertFalse(queue.is_empty())

    def test_event_descriptions_preserved(self):

        queue = make_queue([
            (4, "Spawn Enemy"),
            (2, "Play Sound"),
            (9, "Boss Appears"),
        ])

        descriptions = []

        while not queue.is_empty():

            event = queue.extract_min(
                _noop_draw,
                _noop_wait,
            )

            descriptions.append(event.description)

        self.assertEqual(
            descriptions,
            [
                "Play Sound",
                "Spawn Enemy",
                "Boss Appears",
            ]
        )

    def test_large_event_queue(self):

        queue = PriorityQueue()

        for i in range(1000, 0, -1):

            queue.insert(
                Event(i, f"Event {i}"),
                _noop_draw,
                _noop_wait,
            )

        last_time = -1

        while not queue.is_empty():

            event = queue.extract_min(
                _noop_draw,
                _noop_wait,
            )

            self.assertGreaterEqual(
                event.time,
                last_time,
            )

            last_time = event.time

    def test_benchmark(self):

        queue = PriorityQueue()

        size = 1000000

        start = time.time()

        for i in range(size, 0, -1):

            queue.insert(
                Event(i, f"Event {i}"),
                _noop_draw,
                _noop_wait,
            )

        while not queue.is_empty():

            queue.extract_min(
                _noop_draw,
                _noop_wait,
            )

        elapsed = time.time() - start

        print(f"The priority queue benchmark of processing {size:,} events took {elapsed:.4f} seconds.")


if __name__ == "__main__":
    unittest.main()