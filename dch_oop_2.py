import math

class Circle:
    def __init__(self, radius=None, diameter=None):
        if radius is not None:
            self._radius = radius
        elif diameter is not None:
            self._radius = diameter / 2
        else:
            raise ValueError("Provide radius or diameter")

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def diameter(self):
        return self._radius * 2

    @diameter.setter
    def diameter(self, value):
        self._radius = value / 2

    def area(self):
        return math.pi * self._radius ** 2

    def __str__(self):
        return f"Circle(radius={self._radius})"

    def __add__(self, other):
        if isinstance(other, Circle):
            return Circle(radius=self.radius + other.radius)
        return NotImplemented

    def __gt__(self, other):
        return self.radius > other.radius

    def __eq__(self, other):
        return self.radius == other.radius

    def __lt__(self, other):
        return self.radius < other.radius


# Example
c1 = Circle(radius=3)
c2 = Circle(diameter=10)

print(c1)
print(c2.radius)
print(c1.area())

c3 = c1 + c2
print(c3)

print(c2 > c1)
print(c1 == c2)

circles = [c1, c2, c3]
circles.sort()

for c in circles:
    print(c)
