from enum import Enum
from math import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'

    class Factory:
        @staticmethod
        def new_cartesian_point(x, y):
            return Point(x, y)

        def new_polar_point(self, rho, theta):
            return Point(rho * sin(theta), rho * cos(theta))

    factory = Factory()


# take out factory methods to a separate class
class PointFactory:
    @staticmethod
    def new_cartesian_point(x, y):
        return Point(x, y)

    @staticmethod
    def new_polar_point(rho, theta):
        return Point(rho * sin(theta), rho * cos(theta))


if __name__ == '__main__':
    p2 = PointFactory.new_cartesian_point(1, 2)
    # or you can expose factory through the type
    p3 = Point.Factory.new_cartesian_point(5, 6)
    p4 = Point.factory.new_cartesian_point(7, 8)
    print(p2, p3, p4)
