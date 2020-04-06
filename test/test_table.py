import unittest
from pysudoku.table import Table


class TestTable(unittest.TestCase):

    def setUp(self):
        self.table1 = Table()

    def test_table_assign(self):
        self.table1[0, 0] = 9
        self.assertEqual(self.table1[0, 0], 9)
        self.table1[0, 0] = 1
        self.assertEqual(self.table1[0, 0], 1)
        self.table1[1, 1] = 5
        self.assertEqual(self.table1[1, 1], 5)

    def test_table_key_value_error(self):
        with self.assertRaises(ValueError):
            self.table1[-1, -1] = 5
        
        with self.assertRaises(ValueError):
            self.table1[9, 9] = 5

        with self.assertRaises(ValueError):
            self.table1["1", 2] = 5

    def test_table_key_error(self):
        with self.assertRaises(KeyError):
            self.table1[1] = 2
        
        with self.assertRaises(KeyError):
            self.table1['string']

    def test_table_val_error(self):
        with self.assertRaises(ValueError):
            self.table1[0, 0] = 0

        with self.assertRaises(ValueError):
            self.table1[0, 0] = 10

    def test_translate_positions(self):
        self.assertEqual(self.table1.translate_positions(0, 0), (0, 0, 0, 0))
        self.assertEqual(self.table1.translate_positions(5, 5), (1, 1, 2, 2))
        self.assertEqual(self.table1.translate_positions(0, 3), (0, 1, 0, 0))
        self.assertEqual(self.table1.translate_positions(8, 8), (2, 2, 2, 2))
