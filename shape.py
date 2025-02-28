class Shape:
    def __init__(self, edges):
        self.edges = None
        self.area = None

    def calculate_area(self):
        raise NotImplementedError("Subclasses must implement calcualteArea")


class Triangle(Shape):
    def __init__(self, base, height):
        self.edges = 3
        self.base = base
        self.height = height

    def calculate_area(self):
        return (self.base * self.height)/2
    
    def edges(self):
        return self.edges

class Rectangle(Shape):
    def __init__(self, base, height):
        self.edges = 4
        self.base = base
        self.height = height

    def calculate_area(self):
        return self.base * self.height
    
    def edges(self):
        return self.edges
        
class Circle(Shape):
    def __init__(self, radius):
        self.edges = 0
        self.radius = radius

    def calculate_area(self):
        return 3.14 * self.radius * self.radius
    
    def edges(self):
        return self.edges

shapes = [Triangle(2,1), Rectangle(4,5), Circle(5)]

for shape in shapes:
    print(shape.calculate_area())