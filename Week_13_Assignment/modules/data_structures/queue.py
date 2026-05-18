class Queue:
    _MIN_CAPACITY = 8

    def __init__(self):
        self._data = [None] * self._MIN_CAPACITY
        self._head = 0
        self._size = 0

    def _capacity(self):
        return len(self._data)

    def _resize(self, new_cap):
        """Copy live elements into a fresh array of size new_cap."""
        old = self._data
        self._data = [None] * new_cap
        for i in range(self._size):
            self._data[i] = old[(self._head + i) % len(old)]
        self._head = 0

    def enqueue(self, val):
        if self._size == self._capacity():
            self._resize(self._capacity() * 2)
        tail = (self._head + self._size) % self._capacity()
        self._data[tail] = val
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("IndexError: Attempting to dequeue from an empty queue.")
        val = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % self._capacity()
        self._size -= 1
        if 0 < self._size <= self._capacity() // 4:
            self._resize(max(self._capacity() // 2, self._MIN_CAPACITY))
        return val

    def peek(self):
        if self.is_empty():
            raise IndexError("IndexError: Attempting to peek from an empty queue.")
        return self._data[self._head]

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def __repr__(self):
        items = [self._data[(self._head + i) % self._capacity()]
                 for i in range(self._size)]
        return f"Queue({items})"

    def __iter__(self):
        for i in range(self._size):
            yield self._data[(self._head + i) % self._capacity()]