class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None
        self._tail = None
        self._size = 0

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._size

    def append(self, value):
        new_node = Node(value)
        if self._tail is None:
            self.head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def pop_front(self):
        if self.is_empty():
            raise IndexError("IndexError: Attempting to pop from an empty linked list.")
        val = self.head.value
        self.head = self.head.next
        if self.head is None:
            self._tail = None
        self._size -= 1
        return val

    def insert(self, value, position=None):
        new_node = Node(value)

        if position is None or position <= 0 or self.head is None:
            new_node.next = self.head
            self.head = new_node
            if self._tail is None:
                self._tail = new_node
            self._size += 1
            return

        current = self.head
        index = 0

        while current.next and index < position - 1:
            current = current.next
            index += 1

        new_node.next = current.next
        current.next = new_node
        if new_node.next is None:
            self._tail = new_node
        self._size += 1

    def delete(self, value=None, position=None):
        if self.is_empty():
            raise IndexError("IndexError: Attempting to delete from an empty linked list.")

        if position == 0 or (position is None and self.head.value == value):
            removed = self.head
            self.head = self.head.next
            if self.head is None:
                self._tail = None
            self._size -= 1
            return removed.value

        current = self.head
        prev = None
        idx = 0

        while current:
            if (position is not None and idx == position) or \
               (value is not None and current.value == value):
                prev.next = current.next
                if current.next is None:
                    self._tail = prev
                self._size -= 1
                return current.value

            prev = current
            current = current.next
            idx += 1

        raise ValueError("ValueError: Value not found.")

    def reverse(self):
        prev = None
        current = self.head
        self._tail = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def to_list(self):
        out = []
        current = self.head
        while current:
            out.append(current.value)
            current = current.next
        return out

    def __repr__(self):
        return f"LinkedList({self.to_list()})"