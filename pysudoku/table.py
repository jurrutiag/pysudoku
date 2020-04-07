import numpy as np
from itertools import chain, product


class Table:
    def __init__(self, values=None, magnitude=3):
        self.magnitude = magnitude
        self.cols = magnitude ** 2
        self.rows = self.cols
        self.maxval = self.cols

        if values is not None:
            self.values = values
        
        else:
            self.values = np.random.randint(1, 10, size=(self.rows, self.cols))

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, item):
        self.values[key] = item

    def __str__(self):
        return str(self.values)

    @property
    def blocks(self):
        return (self.values[i: i + 3, j: j + 3] for i, j in product(range(0, 9, 3), repeat=2))

    def changeBlockVal(self, blocknum, i, j, val):
        block_row = blocknum // 3
        block_col = blocknum % 3

        x_index = block_row * 3 + i
        y_index = block_col * 3 + j

        self.values[x_index, y_index] = val

    def getElementBlock(self, i, j):
        block_x = i // 3
        block_y = j // 3

        element_block = block_x * 3 + block_y

        return element_block

    def incorrectNumber(self):
        cols_incorrect = sum(len(set(self.values[:, col])) != self.values[:, col].size for col in range(self.cols))
        rows_incorrect = sum(len(set(self.values[row, :])) != self.values[row, :].size for row in range(self.rows))
        squares_incorrect = sum(len(set(block.flatten())) != block.size for block in self.blocks)

        return cols_incorrect + rows_incorrect + squares_incorrect

    def check(self):
        return self.incorrectNumber() == 0
