from pysudoku.table import Table


class SudokuGame:

    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty
        self.table = Table()
        self.populateTable()

    def check(self):
        return self.table.check()
