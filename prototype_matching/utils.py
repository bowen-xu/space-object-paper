from typing import Callable
import numpy as np
import random
import math
    
def virtual(func: Callable):
    def wrapper(*args, **kwargs):
        raise NotImplementedError(
            f"Function {func.__qualname__} is virtual and is not implemented yet.")
    return wrapper

def gaussian(x, mu, sigma):
    return np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))

def generate_sample(locs: list[tuple[int, int]], size: int, distortion: int=1, padding=True) -> np.ndarray:
    """
    生成样本
    """
    if padding:
        _size = int(np.ceil(size/2))
    else:
        _size = size
    sample = np.zeros((_size, _size), dtype=int)
    for loc in locs:
        x, y = loc
        x += random.randint(-distortion, distortion)
        x = max(0, min(size-1, x))
        y += random.randint(-distortion, distortion)
        y = max(0, min(size-1, y))
        sample[y, x] = 1
    # padding the sample
    if padding:
        padding = (size-_size)//2
        padding2 = size-_size - padding
        sample = np.pad(sample, [(padding, padding2), (padding, padding2)], mode='constant', constant_values=0)
    return sample

def gbellmf(x, a, b, c):
    """
    Generalized Bell function

    Parameters:
    x (numpy array): Input variable.
    a (float): Controls the width of the function.
    b (float): Controls the shape of the function.
    c (float): Controls the center position of the function.

    Returns:
    numpy array: Output values of the generalized Bell function.
    """
    return 1 / (1 + np.abs((x - c) / a) ** (2 * b))

def circle_diff(src: tuple[float, float], tgt: tuple[float, float]):
    # mapping the [-1, 1) value to a circle ring in a 2D plane, represented by vectors
    x, y = src
    theta_x = (x+1)*math.pi
    _x = math.cos(theta_x)
    _y = math.sin(theta_x)
    x_vector1 = np.array((_x, _y))
    theta_x = (y+1)*math.pi
    _x = math.cos(theta_x)
    _y = math.sin(theta_x)
    y_vector1 = np.array((_x, _y))

    x, y = tgt
    theta_x = (x+1)*math.pi
    _x = math.cos(theta_x)
    _y = math.sin(theta_x)
    x_vector2 = np.array((_x, _y))
    theta_x = (y+1)*math.pi
    _x = math.cos(theta_x)
    _y = math.sin(theta_x)
    y_vector2 = np.array((_x, _y))

    # compute the distances in randians
    theta_x = math.acos((np.dot(x_vector1, x_vector2)/(np.linalg.norm(x_vector1)*np.linalg.norm(x_vector2))).clip(-1, 1))
    theta_y = math.acos((np.dot(y_vector1, y_vector2)/(np.linalg.norm(y_vector1)*np.linalg.norm(y_vector2))).clip(-1, 1))

    dx = tgt[0] - src[0]
    dy = tgt[1] - src[1]
    if dy < 0 and dy > -1:
        theta_y = -theta_y
    if dx < 0 and dx > -1:
        theta_x = -theta_x
    # mapping the radians back to [0, 1]
    x_dist = theta_x/math.pi
    y_dist = theta_y/math.pi

    return (x_dist, y_dist)


if __name__ == "__main__":
    if True:
        samples = []
        for _ in range(16):
            sample = generate_sample([(5, 2), (2, 8), (8, 8)], 11, 1, padding=False)
            samples.append(sample)
        import matplotlib.pyplot as plt
        plt.figure()
        for i, sample in enumerate(samples):
            plt.subplot(4, 4, i+1)
            plt.axis('off')
            plt.imshow(sample, aspect='equal')
        # plt.suptitle("Examples")
        plt.tight_layout()
        plt.savefig("figs/examples.png")
        plt.show()
    l1 = tuple(np.array((5,2))/11)
    l2 = tuple(np.array((-10, 8))/11)
    d = circle_diff(l2, l1)
    print(d)
