class DoubleLinkedList:
    def __init__(self, data=None):
        self.end = EndNode()
        self.head = None
        self.tail = None
        if data:
            self.extend(data)
        self.current = self.end

    def extend(self, buttons):
        for button in buttons:
            if self.head is None:
                self.head = button
                self.tail = self.head
            else:
                self.tail.next = button
                self.tail.next.prev = self.tail
                self.tail = self.tail.next
        self.tail.next = self.end
        self.head.prev = self.tail.next
        self.end.next = self.head
        self.end.prev = self.tail

    def __iter__(self):
        return self

    def __next__(self):
        self.current = self.current.next
        if isinstance(self.current, EndNode):
            raise StopIteration
        return self.current


class EndNode:
    def __init__(self):
        self.next = None
        self.prev = None
