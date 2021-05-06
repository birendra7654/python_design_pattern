from enum import Enum
from typing import List


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Product:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size


# Specification
class Specification:
    def is_satisfied(self, item: Product):
        pass

    def __and__(self, other):
        return AndSpecification(self, other)

    def __or__(self, other):
        return OrSpecification(self, other)


class Filter:
    def filter(self, item: Product, spec: Specification):
        pass


class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item: Product):
        return item.color == self.color


class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item: Product):
        return item.size == self.size


class AndSpecification(Specification):
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item: Product):
        return all(map(
            lambda spec: spec.is_satisfied(item), self.args
        ))


class OrSpecification(Specification):
    def __init__(self, *args: Specification):
        self.args = args

    def is_satisfied(self, item: Product):
        return any(map(
            lambda spec: spec.is_satisfied(item), self.args
        ))


class BetterFilter(Filter):
    def filter(self, items: List[Product], spec: Specification):
        for item in items:
            if spec.is_satisfied(item):
                yield item


if __name__ == '__main__':
    apple = Product("Apple", Color.GREEN, Size.SMALL)
    tree = Product("tree", Color.GREEN, Size.LARGE)
    house = Product("House", Color.BLUE, Size.LARGE)

    products = [apple, tree, house]

    bf = BetterFilter()
    print("Green product (new): ")
    for p in bf.filter(products, ColorSpecification(Color.GREEN)):
        print(f" - {p.name} is green")

    print("Large products")
    large_spec = SizeSpecification(Size.LARGE)
    for p in bf.filter(products, large_spec):
        print(f' - {p.name} is large')

    print("large and blue items")
    # large_blue_spec = AndSpecification(large_spec, ColorSpecification(Color.BLUE))
    large_and_blue_spec = large_spec & ColorSpecification(Color.BLUE)
    for p in bf.filter(products, large_and_blue_spec):
        print(f" - {p.name} is blue and large")

    print("large or blue items")
    large_or_blue_spec = large_spec | ColorSpecification(Color.BLUE)
    for p in bf.filter(products, large_or_blue_spec):
        print(f" - {p.name} is {p.size} or {p.color}")