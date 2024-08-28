import numpy
import numpy as np
from enum import Enum


class StackOfMaxNElements:
    def __init__(self, max_number_of_elements):
        self.max_number_of_elements = max_number_of_elements
        self.elements = []

    def push(self, element):
        self.elements.append(element)
        if len(self.elements) > self.max_number_of_elements:
            self.elements.pop(0)

    def pop(self):
        if len(self.elements) > 0:
            return self.elements.pop()
        return None


class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


class Board:
    def __init__(self, size):
        self.values = np.zeros((size, size), dtype=int)
        self.size = size
        starting_points = np.random.choice(self.size * self.size, 2, replace=False)
        starting_values = np.random.choice([2, 4], 2)
        self.values[int(starting_points[0] / self.size)][starting_points[0] % self.size] = starting_values[0]
        self.values[int(starting_points[1] / self.size)][starting_points[1] % self.size] = starting_values[1]
        self.score = 0

    def shift_board_left(self, matrix):
        copy = np.copy(matrix)
        for row in matrix:
            # sum same numbers
            last_left = -1
            for i in range(0, len(row)):
                if row[i] != 0:
                    if last_left != -1:
                        if row[i] == row[last_left]:
                            row[last_left] += row[i]
                            self.score += row[last_left]
                            row[i] = 0
                            last_left = -1
                        else:
                            last_left = i
                    else:
                        last_left = i

            # shift left
            position = 0
            for i in range(0, len(row)):
                if row[i] != 0:
                    row[position] = row[i]
                    position += 1
            for i in range(position, len(row)):
                row[i] = 0
        return not np.array_equal(copy, matrix)

    def shift_board_up(self, matrix):
        tmp = matrix.transpose()
        return self.shift_board_left(tmp)

    def shift_board_right(self, matrix):
        tmp = np.flip(matrix, 1)
        return self.shift_board_left(tmp)

    def shift_board_down(self, matrix):
        tmp = np.flip(matrix.transpose(), 1)
        return self.shift_board_left(tmp)

    def is_the_move_possible(self):
        copy = np.copy(self.values)
        tmp = self.score
        if self.shift_board_left(copy):
            self.score = tmp
            return True
        if self.shift_board_right(copy):
            self.score = tmp
            return True
        if self.shift_board_up(copy):
            self.score = tmp
            return True
        if self.shift_board_down(copy):
            self.score = tmp
            return True
        return False

    def insert_new_2_or_4(self):
        num_zeros = (self.values == 0).sum()
        insert = np.random.choice(([2, 4]), 1, p=[0.7, 0.3])
        position = np.random.randint(0, num_zeros)
        counter = 0
        for row in self.values:
            for i in range(0, len(row)):
                if row[i] == 0:
                    if counter == position:
                        row[i] = insert
                        return
                    counter += 1

    def make_a_move(self, direction):
        copy = numpy.copy(self.values)
        if direction == Direction.LEFT:
            return self.shift_board_left(self.values)
        elif direction == Direction.UP:
            return self.shift_board_up(self.values)
        elif direction == Direction.RIGHT:
            return self.shift_board_right(self.values)
        elif direction == Direction.DOWN:
            return self.shift_board_down(self.values)

    def contains_2048_or_greater(self):
        number_of_ge_2048 = (self.values >= 2048).sum()
        if number_of_ge_2048 > 0:
            return True
        return False
