from enum import Enum


class SudokuSolver:
    class State(Enum):
        ITERATE = 1
        GUESS = 2
        BACKTRACK = 3

    rows = [{0, 1, 2, 3, 4, 5, 6, 7, 8}, {9, 10, 11, 12, 13, 14, 15, 16, 17}, {18, 19, 20, 21, 22, 23, 24, 25, 26},
            {27, 28, 29, 30, 31, 32, 33, 34, 35}, {36, 37, 38, 39, 40, 41, 42, 43, 44},
            {45, 46, 47, 48, 49, 50, 51, 52, 53}, {54, 55, 56, 57, 58, 59, 60, 61, 62},
            {63, 64, 65, 66, 67, 68, 69, 70, 71}, {72, 73, 74, 75, 76, 77, 78, 79, 80}]
    columns = [{0, 9, 18, 27, 36, 45, 54, 63, 72}, {1, 10, 19, 28, 37, 46, 55, 64, 73},
               {2, 11, 20, 29, 38, 47, 56, 65, 74}, {3, 12, 21, 30, 39, 48, 57, 66, 75},
               {4, 13, 22, 31, 40, 49, 58, 67, 76}, {5, 14, 23, 32, 41, 50, 59, 68, 77},
               {6, 15, 24, 33, 42, 51, 60, 69, 78}, {7, 16, 25, 34, 43, 52, 61, 70, 79},
               {8, 17, 26, 35, 44, 53, 62, 71, 80}]
    boxes = [{0, 1, 2, 9, 10, 11, 18, 19, 20}, {3, 4, 5, 12, 13, 14, 21, 22, 23}, {6, 7, 8, 15, 16, 17, 24, 25, 26},
             {27, 28, 29, 36, 37, 38, 45, 46, 47}, {30, 31, 32, 39, 40, 41, 48, 49, 50},
             {33, 34, 35, 42, 43, 44, 51, 52, 53}, {54, 55, 56, 63, 64, 65, 72, 73, 74},
             {57, 58, 59, 66, 67, 68, 75, 76, 77}, {60, 61, 62, 69, 70, 71, 78, 79, 80}]

    possible_nums = []
    solved_nums = 0
    numbers_list = []
    changed_stack = []
    guessed_pairs = []
    guess_flag = False

    poss_nums_of_guessed = []

    def set_possible_nums(self):
        for i in range(0, 81):
            if self.numbers_list[i] != 0:
                self.solved_nums += 1
                self.possible_nums.append(set([self.numbers_list[i]]))
                continue
            myset = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            neigs = self.get_neighbours(i)
            for neig in neigs:
                if self.numbers_list[neig] == 0:
                    continue
                myset.discard(self.numbers_list[neig])

            self.possible_nums.append(myset)
            if len(myset) == 0:
                print("This sudoku is impossible")
                exit(1)
            if len(myset) == 1:
                self.solved_nums += 1
                for num in myset:
                    break
                self.numbers_list[i] = num

    def iterate_numbers(self):
        changed = False
        for i in range(0, 81):
            if self.numbers_list[i] != 0:
                continue
            myset = self.possible_nums[i]
            old_len = len(myset)
            neigs = self.get_neighbours(i)
            for neig in neigs:
                if self.numbers_list[neig] == 0:
                    continue
                myset.discard(self.numbers_list[neig])
            new_len = len(myset)
            if new_len != old_len:
                changed = True
                if self.guess_flag:
                    self.changed_stack[-1].add(i)

            if new_len == 0:
                return self.State.BACKTRACK

            if new_len == 1:
                if self.numbers_list[i] == 0:
                    self.solved_nums += 1
                for num in myset:
                    break
                self.numbers_list[i] = num
                continue

        if changed:
            return self.State.ITERATE
        else:

            return self.State.GUESS

    def get_number_to_guess(self):
        min = 9
        pos = -1
        for i in range(0, 81):
            if len(self.possible_nums[i]) < min and len(self.possible_nums[i]) > 1:
                min = len(self.possible_nums[i])
                pos = i

        return pos

    def __init__(self, file="sudoku.txt"):
        self.numbers_list = self.read_sudoku_from_file(file)
        self.set_possible_nums()
        self.state = self.State.ITERATE

    def iterate(self):

        self.state = self.iterate_numbers()

    def guess(self):

        num = self.get_number_to_guess()
        if num == -1:
            print("Seems like all numbers all solved already?!")
            exit(1)
        if self.guess_flag:
            self.changed_stack[-1].add(num)
        self.guess_flag = True

        myset = self.possible_nums[num]
        for guessing_num in myset:
            break

        self.guessed_pairs.append((num, guessing_num))
        self.changed_stack.append(set())
        self.solved_nums += 1
        self.numbers_list[num] = guessing_num
        self.possible_nums[num].discard(guessing_num)
        self.poss_nums_of_guessed.append(self.possible_nums[num].copy())
        self.possible_nums[num] = set([guessing_num])
        self.state = self.State.ITERATE

    def backtr(self):
        if len(self.changed_stack) == 0:
            print("Sudoku is impossible to solve")
            exit(1)

        numbers_to_back = self.changed_stack.pop()
        guess_pair = self.guessed_pairs.pop()
        self.possible_nums[guess_pair[0]] = self.poss_nums_of_guessed.pop()
        myset = self.possible_nums[guess_pair[0]]
        if len(myset) == 0:
            self.numbers_list[guess_pair[0]] = 0
            self.solved_nums -= 1
        else:
            for n in myset:
                break
            myset.discard(n)
            self.poss_nums_of_guessed.append(myset)
            self.possible_nums[guess_pair[0]] = set([n])
            self.numbers_list[guess_pair[0]] = n
            self.guessed_pairs.append((guess_pair[0], n))
            self.changed_stack.append(set())

        for i in numbers_to_back:
            if self.numbers_list[i] != 0:
                self.numbers_list[i] = 0
                self.solved_nums -= 1
            self.possible_nums[i] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.guess_flag = len(self.changed_stack) != 0
        self.state = self.iterate_numbers()

    def get_row(self, num):
        myset = self.rows[num // 9].copy()
        myset.discard(num)
        return myset

    def get_column(self, num):
        col_num = num % 9
        myset = self.columns[col_num].copy()
        myset.discard(num)
        return myset

    def get_box(self, num):
        row_num = num // 27
        col_num = (num % 9) // 3
        box_num = row_num * 3 + col_num
        myset = self.boxes[box_num].copy()
        myset.discard(num)
        return myset

    def get_neighbours(self, num):
        myset = self.get_row(num)
        myset = myset.union(self.get_column(num))
        myset = myset.union(self.get_box(num))
        return myset

    def read_sudoku_from_file(self, file):
        myfile = open(file)
        my_string = myfile.read()
        numbers = [int(i) for i in my_string.split() if i.isdigit()]
        return numbers

    def solve_sudoku(self):
        while True:
            func = self.state_dict.get(self.state)
            func(self)
            if self.solved_nums == 81:
                break

        return self.numbers_list.copy()

    def print_sudoku(self):
        for start in range(0, 81, 9):
            print(self.numbers_list[start:start + 9])

    state_dict = { State.ITERATE: iterate, State.GUESS: guess, State.BACKTRACK: backtr}

    def get_row_t(num):
        start = (num // 9) * 9
        my_set = set(range(start, start + 9))
        my_set.discard(num)
        return my_set

    def get_column_t(num):
        start = num % 9
        my_set = set(range(start, 81, 9))
        my_set.discard(num)
        return my_set

    def get_box_t(num):
        row_num = num // 27
        col_num = (num % 9) // 3
        start_num = 27 * row_num + 3 * col_num
        my_set = set()
        for i in range(0, 3):
            for j in range(0, 3):
                new_num = start_num + j
                my_set.add(new_num)
            start_num += 9
        my_set.discard(num)
        return my_set


if __name__ == "__main__":
    myfile = open("sudoku.txt", 'w')
    test_sudoku = "5 6 0  7 2 0  0 0 0 " \
                  "0 9 0  0 0 6  0 0 0 " \
                  "0 0 0  0 0 0  8 0 0 " \
                  "" \
                  "0 0 4  8 0 0  6 0 0 " \
                  "0 0 0  0 0 0  0 0 9 " \
                  "0 0 0  0 6 0  0 5 0 " \
                  "" \
                  "0 0 0  1 7 8  4 0 0 " \
                  "0 5 0  0 4 0  0 7 0 " \
                  "4 0 3  0 0 0  0 0 0 "
    myfile.write(test_sudoku)
    test_solution = [5, 6, 8, 7, 2, 4, 1, 9, 3,
                     1, 9, 7, 3, 8, 6, 5, 2, 4,
                     3, 4, 2, 5, 1, 9, 8, 6, 7,
                     7, 3, 4, 8, 9, 5, 6, 1, 2,
                     6, 8, 5, 2, 3, 1, 7, 4, 9,
                     2, 1, 9, 4, 6, 7, 3, 5, 8,
                     9, 2, 6, 1, 7, 8, 4, 3, 5,
                     8, 5, 1, 9, 4, 3, 2, 7, 6,
                     4, 7, 3, 6, 5, 2, 9, 8, 1]

    myfile.close()
    my_sudoku = SudokuSolver()
    assert test_solution == my_sudoku.solve_sudoku()
    my_sudoku.print_sudoku()