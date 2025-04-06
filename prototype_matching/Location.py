from random import uniform
from .utils import gbellmf, circle_diff
import math
import numpy as np


class Location:
    """
    位置概念
    """

    def __init__(self, center: tuple[float, float]) -> None:
        self.update(center, 0.1, 0.9)

    @staticmethod
    def randomly_initialize(center: tuple[float, float]):
        x, y = center
        return Location((uniform(x-0.5, x+0.5), uniform(y-0.5, y+0.5)))

    def activate(self):
        pass  # TODO

    def update(self, center: tuple[float, float], radius, sharpness):
        self.update_center(center)
        self.radius = radius
        self.sharpness = sharpness

    def update_center(self, center: tuple[float, float]):
        self.center = (center[0]+1) % 2-1, (center[1]+1) % 2-1

    def move(self, dx: float, dy: float):
        self.center = Location._move(self.center, dx, dy)

    @staticmethod
    def _move(point: tuple[float, float], dx: float, dy: float):
        return (point[0]+dx+1) % 2-1, (point[1]+dy+1) % 2-1

    def match(self, other: tuple[int, int]):
        # distance = math.sqrt((self.center[0]-other[0])**2 + (self.center[1]-other[1])**2)
        diff = circle_diff(self.center, other)
        distance = math.sqrt(diff[0]**2 + diff[1]**2)
        sharpness = self.sharpness*self.radius*20
        return gbellmf(distance, self.radius, sharpness, 0)
    
    def match_bias(self, other: tuple[int, int]):
        distance = np.linalg.norm(other)
        sharpness = self.sharpness*self.radius*20
        return gbellmf(distance, self.radius, sharpness, 0)
    
    def __iter__(self):
        return iter(self.center)

    def __repr__(self) -> str:
        return f"Location[{self.center}]"
    
    def __sub__(self, other: 'Location') -> tuple[int, int]:
        # return self.center[0]-other.center[0], self.center[1]-other.center[1]
        return circle_diff(other.center, self.center)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    loc = Location((0, 0))
    xs = np.linspace(-1, 1, 101)
    values = [loc.match((0, x)) for x in xs]
    plt.plot(xs, values)
    plt.show()
