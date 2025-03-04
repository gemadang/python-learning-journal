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