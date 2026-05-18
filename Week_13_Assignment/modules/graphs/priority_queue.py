from dataclasses import dataclass


@dataclass(order=True)
class Event:
    time: int
    description: str


class PriorityQueue:

    def __init__(self):
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

    def insert(self, event, draw_fn=None, wait_fn=None):

        self.heap.append(event)

        if draw_fn:
            draw_fn(self.heap, [len(self.heap) - 1], None)

        if wait_fn:
            wait_fn(250)

        self._heapify_up(len(self.heap) - 1, draw_fn, wait_fn)

    def extract_min(self, draw_fn=None, wait_fn=None):

        if not self.heap:
            return None

        root = self.heap[0]

        self.heap[0] = self.heap[-1]
        self.heap.pop()

        if self.heap:

            if draw_fn:
                draw_fn(self.heap, [0], root)

            if wait_fn:
                wait_fn(250)

            self._heapify_down(0, draw_fn, wait_fn)

        return root

    def _heapify_up(self, index, draw_fn=None, wait_fn=None):

        while index > 0:

            parent = (index - 1) // 2

            if self.heap[parent].time > self.heap[index].time:

                self.heap[parent], self.heap[index] = (
                    self.heap[index],
                    self.heap[parent],
                )

                if draw_fn:
                    draw_fn(self.heap, [parent, index], None)

                if wait_fn:
                    wait_fn(350)

                index = parent

            else:
                break

    def _heapify_down(self, index, draw_fn=None, wait_fn=None):

        n = len(self.heap)

        while True:

            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if (
                left < n and
                self.heap[left].time < self.heap[smallest].time
            ):
                smallest = left

            if (
                right < n and
                self.heap[right].time < self.heap[smallest].time
            ):
                smallest = right

            if smallest != index:

                self.heap[index], self.heap[smallest] = (
                    self.heap[smallest],
                    self.heap[index],
                )

                if draw_fn:
                    draw_fn(self.heap, [index, smallest], None)

                if wait_fn:
                    wait_fn(350)

                index = smallest

            else:
                break