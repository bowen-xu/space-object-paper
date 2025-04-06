import numpy as np

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