'''
Part 1: Stack Elevator Drop Ride Simulation
Create a class ElevatorRide:

Use a stack to simulate guests entering an elevator ride.

Guests board one at a time and exit in reverse order (the last person in is the first out).
'''
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class ElevatorRide:
    def __init__(self):
        self.head = None
        self.size = 0

    def board_guest(self, guest_name): #adds a guest.
        guest = Node(guest_name)
        guest.next = self.head
        self.head = guest
        self.size += 1

    def start_ride(self, capacity): #simulates the ride, displaying guest names as they exit.
        current = self.head
        if not current:
            print('No guests in elevator')
        
        while current and capacity > 0:
            print(current.data, end=" -> ")
            current = current.next
            capacity -= 1

        print("Null")
        self.head = current

'''
Part 2: Queue Roller Coaster Ride Simulation
Create a class RollerCoasterRide:

Use a queue to manage guests waiting for the roller coaster.

Guests enter the queue and exit in the same order they arrived (first in, first out).
'''
class RollerCoasterRide:
    def __init__(self):
        self.rollerCoasterQueue = []

    def join_queue(self, guest_name): # adds a guest to the line.
        self.rollerCoasterQueue.append(guest_name)

    def start_ride(self, capacity): # simulates loading and running the coaster, displaying guest names as they board.
        if len(self.rollerCoasterQueue) == 0:
            print('No guests in roller coaster')
        
        i = 0

        while i < len(self.rollerCoasterQueue) and capacity > 0:
            print(self.rollerCoasterQueue[i], end=" -> ")
            i += 1
            capacity -= 1

        print("Null")
        #empty rollercoaster
        if i < len(self.rollerCoasterQueue):
            self.rollerCoasterQueue = self.rollerCoasterQueue[i:]
        else:
            self.rollerCoasterQueue = []
 


'''
Part 3: Priority Queue VIP Guest Management
Create a class VIPRide:

Use a priority queue to manage guests based on priority levels (e.g., VIP or Fast Pass holders).

Guests with higher priority board the ride before others.

'''
import heapq
class VIPRide:
    def __init__(self):
        self.heap = []
        
    def add_guest(self, guest_name, priority): #adds a guest with their priority (lower number indicates higher priority).
        heapq.heappush(self.heap, (priority, guest_name))

    def start_ride(self, capacity): #simulates the ride, displaying guest names as they board based on priority.
        if len(self.heap) == 0:
            print('No guests in VIPRide')
        
        while len(self.heap) > 0 and capacity > 0:
            vip = heapq.heappop(self.heap)[1]
            print(vip, end=" -> ")
            capacity -= 1

        print("Null")

if __name__ == "__main__":
    print('elevator')
    elevator = ElevatorRide()
    elevator.board_guest("Geri")
    elevator.board_guest("Irfan")
    elevator.board_guest("Farhana")
    elevator.board_guest("Sam")
    elevator.start_ride(3)

    print('rollercoaster')
    rollercoaster = RollerCoasterRide()
    rollercoaster.join_queue("Geri")
    rollercoaster.join_queue("Irfan")
    rollercoaster.join_queue("Farhana")
    rollercoaster.join_queue("Sam")
    rollercoaster.start_ride(4)

    print('vip')
    vip = VIPRide()
    vip.add_guest("Geri", 4)
    vip.add_guest("Irfan", 3)
    vip.add_guest("Farhana", 4)
    vip.add_guest("Sam", 3)
    vip.add_guest("Tofunmi", 5)
    vip.start_ride(5)
