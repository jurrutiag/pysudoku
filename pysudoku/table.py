import numpy as np
from itertools import chain, product


class Table:
    def __init__(self, magnitude=3):
        self.magnitude = magnitude
        self.cols = magnitude ** 2
        self.rows = self.cols

        self.values = np.random.randint(1, 10, size=(self.rows, self.cols))

    def __getitem__(self, key):
        x, y = self.key_verification(key)
        return self.values[x, y]

    def __setitem__(self, key, item):
        x, y = self.key_verification(key)
        val = self.val_verification(item)
        self.values[x, y] = val

    def __str__(self):
        return str(self.values)

    @property
    def blocks(self):
        return (self.values[i: i + 3, j: j + 3] for i, j in product(range(0, 9, 3), repeat=2))

    def check(self):
        col_sums = (np.sum(self.values[:, col]) for col in range(self.cols))
        row_sums = (np.sum(self.values[row, :]) for row in range(self.rows))
        square_sums = (np.sum(block) for block in self.blocks)
        
        if any(num_sum != 9 for num_sum in chain(col_sums, row_sums, square_sums)):
            return False

    def key_verification(self, key):
        if not isinstance(key, tuple) or len(key) != 2:
            raise KeyError("Key must be a tuple (x, y)")

        x, y = key

        if not isinstance(x, (float, int)) or not isinstance(y, (float, int)):
            raise ValueError("x and y must be numbers")

        if x >= self.rows or y >= self.cols or x < 0 or y < 0:
            raise ValueError("x and y must be in range 0 to 8")

        return x, y

    def val_verification(self, item):
        if item < 1 or item > 9:
            raise ValueError("Value assigned must be in range from 1 to 9")

        return item
