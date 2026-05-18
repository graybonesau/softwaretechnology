class Stack:
    def __init__(self):
        self._data = []

    def push(self, val):
        self._data.append(val)

    def pop(self):
        if not self.is_empty():
            return self._data.pop()
        raise IndexError("IndexError: Attempting to pop from an empty stack.")

    def peek(self):
        if not self.is_empty():
            return self._data[-1]
        raise IndexError("IndexError: Attempting to peek from an empty stack.")

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def __repr__(self):
        return f"Stack({self._data})"