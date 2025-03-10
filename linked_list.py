class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def get_length(self):
        return self.size

    def prepend(self, data):
        head_node = Node(data)
        head_node.next = self.head
        self.head = head_node
        self.size += 1

    def append(self, data):
        current = self.head
        if current:
            while current.next:
                current = current.next
            current.next = Node(data)
        else:
            self.head = Node(data)

        self.size += 1
    
    def search(self, target):
        current = self.head
        i = 0

        while current:
            if current.data == target:
                return i, current, True
            i += 1
            current = current.next

        return -1, None, False
    
    def display(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def insertAfter(self, index, data):
        if index == 0:
            self.prepend(data)
            return
        current = self.head
        pos = 0
        while current and pos < index - 1:
            current = current.next
            pos += 1
        if not current:
            print('index out of bounds')
            return
        newNode = Node(data)

    def removeNode()