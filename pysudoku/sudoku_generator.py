from pygenal.structure import GeneticAlgorithm, Individual
from pygenal import selection
from pysudoku.table import Table
from itertools import chain
import numpy as np
import copy


class SudokuIndividual(Individual):
    MODEL = Table


    def evaluateFitness(self):
        cols_different = sum(len(set(self.model.values[:, col])) for col in range(self.model.cols))
        rows_different = sum(len(set(self.model.values[row, :])) for row in range(self.model.rows))
        squares_different = sum(len(set(block.flatten())) for block in self.model.blocks)

        self.fitness = (cols_different + rows_different + squares_different) / (3 * 81)

    def mutate(self):
        for _ in range(np.random.randint(1, 5)):
            if np.random.random() < 0.3:
                mut_num = np.random.randint(0, self.model.rows)
                if len(set(self.model.values[mut_num, :])) < self.model.cols:
                    self.model.values[mut_num, np.random.randint(0, self.model.cols)] = np.random.randint(1, self.model.maxval + 1)

            if np.random.random() < 0.3:
                mut_num = np.random.randint(0, self.model.rows)
                if len(set(self.model.values[:, mut_num])) < self.model.rows:
                    self.model.values[np.random.randint(0, self.model.cols), mut_num] = np.random.randint(1, self.model.maxval + 1)

            if np.random.random() < 0.3:
                mut_num = np.random.randint(0, self.model.rows)
                if len(set(list(self.model.blocks)[mut_num].flatten())) < self.model.cols:
                    self.model.changeBlockVal(mut_num, np.random.randint(0, self.model.magnitude), np.random.randint(0, self.model.magnitude), np.random.randint(1, self.model.maxval + 1))


    def __str__(self):
        return str(self.model.values)


class SudokuGenAl(GeneticAlgorithm):
    INDIVIDUAL = SudokuIndividual
    SELECTION = selection.Chain([
        selection.Elitism(parents_percentage=0.05),
        selection.Rank(probability=0.5, parents_percentage=0.75),
        selection.Random(parents_percentage=0.19),
        selection.NewRandom(parents_percentage=0.01),
    ], parents_percentage=0.5)

    def crossover(self, ind1, ind2):
        amount_of_changes = np.random.randint(5, 21)
        
        ch1_vals = ind1.model.values.copy()
        ch2_vals = ind2.model.values.copy()

        x_range = ind1.model.rows
        y_range = ind1.model.cols

        for _ in range(amount_of_changes):
            choice_num = np.random.randint(0, x_range)

            if (choice := np.random.choice(3, size=1)) == 0:
                # Change rows
                ch1_vals[0:choice_num, :] = ind1.model[0:choice_num, :]
                ch2_vals[0:choice_num, :] = ind2.model[0:choice_num, :]

                ch1_vals[choice_num:, :] = ind2.model[choice_num:, :]
                ch2_vals[choice_num:, :] = ind1.model[choice_num:, :]
            
            elif choice == 1:
                # Change cols
                ch1_vals[:, 0:choice_num] = ind1.model[:, 0:choice_num]
                ch2_vals[:, 0:choice_num] = ind2.model[:, 0:choice_num]

                ch1_vals[:, choice_num:] = ind2.model[:, choice_num:]
                ch2_vals[:, choice_num:] = ind1.model[:, choice_num:]

            elif choice == 2:
                ch1_vals = [*list(ind1.model.blocks)[:choice_num], *list(ind2.model.blocks)[choice_num:]]
                ch2_vals = [*list(ind2.model.blocks)[:choice_num], *list(ind1.model.blocks)[choice_num:]]

                ch1_vals = np.block([[i for i in j] for j in np.array(ch1_vals).reshape(3, 3, 3, 3)])
                ch2_vals = np.block([[i for i in j] for j in np.array(ch2_vals).reshape(3, 3, 3, 3)])

            # ind1_x, ind1_y = np.random.randint(0, x_range), np.random.randint(0, y_range)
            # ind2_x, ind2_y = np.random.randint(0, x_range), np.random.randint(0, y_range)

            # ch1_vals[ind1_x, ind1_y] = ind2.model[ind2_x, ind2_y]
            # ch2_vals[ind2_x, ind2_y] = ind1.model[ind1_x, ind1_y]
        
        return SudokuIndividual(ch1_vals), SudokuIndividual(ch2_vals)

    def terminationCondition(self):
        return self.getBest().model.check()


if __name__ == "__main__":
    import logging
    import sys

    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    DATE_TIME_FORMAT = "%H:%M:%S"
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATE_TIME_FORMAT)

    sudoku_genal = SudokuGenAl(pop_size=100, mutation_prob=0.05, cross_prob=0.7)
    sudoku_genal.evolve()

    logging.shutdown()
