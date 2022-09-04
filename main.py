class Cell:
    def __init__(self, num, set):
        self.num = num
        self.set = set

    def add_to_set(self, num):
        self.set.append(num)


puzzle = [
    [0, 9, 6, 5, 0, 4, 0, 7, 1],
    [0, 2, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 4, 0, 9, 0, 6, 2, 3],
    [0, 0, 3, 0, 6, 0, 0, 8, 0],
    [0, 0, 8, 0, 5, 0, 4, 0, 0],
    [9, 0, 0, 4, 0, 0, 0, 0, 5],
    [7, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 1, 0, 7, 5, 3, 4, 9],
    [2, 3, 0, 0, 4, 8, 1, 0, 7]
]


def sudoku_solver(puzzle):
    print_puzzle(puzzle)
    points_mat = create_points_mat(puzzle)
    points_mat = canidate_killing(points_mat)

    if not valid_grid(points_mat):
        raise SyntaxError

    points_mat = negative_start(points_mat)

    i = 0
    j = 0

    while i < 9 and j < 9:
        if points_mat[j][i].num == 0:
            start_index = 0
            while True:
                points_mat[j][i].num = find_valid_num(points_mat, i, j, start_index)
                if points_mat[j][i].num == 0:
                    prev = backtrack(i, j, points_mat)
                    i, j = prev[0], prev[1]
                    start_index = points_mat[j][i].set.index(points_mat[j][i].num) + 1
                else:
                    break
        next = next_index(i, j)
        i, j = next[0], next[1]

    points_mat = positive_end(points_mat)

    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            puzzle[i][j] = points_mat[j][i].num

    print_puzzle(puzzle)

    return puzzle


def canidate_killing(points_mat):
    # row_killing:
    for i in range(len(points_mat)):
        for num in range(1, 10):
            total_count = 0
            save_index = (-1, -1)
            for j in range(len(points_mat)):
                set_count = points_mat[j][i].set.count(num)
                total_count += set_count

                if set_count == 1 and total_count == 1:
                    save_index = (j, i)

                elif total_count > 1:
                    break
            if total_count == 1:
                points_mat = mat_cleaning(points_mat, num, save_index)

        # colom_killing:
        for j in range(len(points_mat)):
            for num in range(1, 10):
                total_count = 0
                save_index = (-1, -1)
                for i in range(len(points_mat)):
                    set_count = points_mat[j][i].set.count(num)
                    total_count += set_count

                    if set_count == 1 and total_count == 1:
                        save_index = (j, i)

                    elif total_count > 1:
                        break
                if total_count == 1:
                    points_mat = mat_cleaning(points_mat, num, save_index)

        # box_killing:
        for j in range(0, 7, 3):
            for i in range(0, 7, 3):
                # box has been chosen
                for num in range(1, 10):
                    total_count = 0
                    save_index = (-1, -1)

                    # searching in a box:
                    for j_box in range(3):
                        for i_box in range(3):
                            set_count = points_mat[j + j_box][i + i_box].set.count(num)
                            total_count += set_count

                            if set_count == 1 and total_count == 1:
                                save_index = (j + j_box, i + i_box)

                            elif total_count > 1:
                                break
                        if total_count > 1:
                            break

                    if total_count == 1:
                        points_mat = mat_cleaning(points_mat, num, save_index)

    return points_mat


def mat_cleaning(points_mat, num, save_index):
    points_mat[save_index[0]][save_index[1]].num = num
    points_mat[save_index[0]][save_index[1]].set = []

    points_mat = row_cleaning(points_mat, num, save_index[1])
    points_mat = colom_cleaning(points_mat, num, save_index[0])
    points_mat = box_cleaning(points_mat, num, save_index[0], save_index[1])
    return points_mat


def row_cleaning(points_mat, num, row):
    for j in range(len(points_mat)):
        if num in points_mat[j][row].set:
            points_mat[j][row].set.remove(num)
    return points_mat


def colom_cleaning(points_mat, num, colom):
    for i in range(len(points_mat)):
        if num in points_mat[colom][i].set:
            points_mat[colom][i].set.remove(num)
    return points_mat


def box_cleaning(points_mat, num, j, i):
    i_box = (i // 3) * 3
    j_box = (j // 3) * 3

    for i_ in range(i_box, i_box + 3):
        for j_ in range(j_box, j_box + 3):
            if num in points_mat[j_][i_].set:
                points_mat[j_][i_].set.remove(num)
    return points_mat


def create_points_mat(puzzle):
    points_mat = []
    for i in range(len(puzzle)):
        temp_list = []
        for j in range(len(puzzle)):
            temp_list.append(Cell(puzzle[j][i], []))
        points_mat.append(temp_list)

    for i in range(len(points_mat)):
        for j in range(len(points_mat)):
            if points_mat[j][i].num == 0:
                point = points_mat[j][i]
                for num in range(1, 10):
                    if valid_num(points_mat, i, j, num):
                        point.add_to_set(num)
    return points_mat


def find_valid_num(points_mat, i, j, start_index):
    for index in range(start_index, len(points_mat[j][i].set)):
        if valid_num(points_mat, i, j, points_mat[j][i].set[index]):
            return points_mat[j][i].set[index]
    return 0


def next_index(i, j):
    if j < 8:
        j += 1
    else:
        j = 0
        i += 1
    return [i, j]


def backtrack(i, j, mat):
    while True:
        prev = prev_index(i, j)
        i, j = prev[0], prev[1]

        if mat[j][i].num >= 0:
            break
    return [i, j]


def prev_index(i, j):
    if j > 0:
        j -= 1
    else:
        j = 8
        i -= 1
    return [i, j]


def valid_num(mat, i, j, num):
    if valid_row(mat, j, num) and valid_colom(mat, i, num) and valid_box(mat, j, i, num):
        return True
    return False


def valid_row(mat, row, num):
    for i in range(len(mat[row])):
        if abs(mat[row][i].num) == num:
            return False
    return True


def valid_colom(mat, colom, num):
    for j in range(len(mat[colom])):
        if abs(mat[j][colom].num) == num:
            return False
    return True


def valid_box(mat, i, j, num):
    i_check = (i // 3) * 3
    j_check = (j // 3) * 3

    for i_ in range(i_check, i_check + 3):
        for j_ in range(j_check, j_check + 3):
            if abs(mat[i_][j_].num) == num:
                return False
    return True


def negative_start(mat):
    for i in range(len(mat)):
        for j in range(len(mat)):
            mat[j][i].num *= -1
    return mat


def positive_end(mat):
    for i in range(len(mat)):
        for j in range(len(mat)):
            mat[j][i].num = abs(mat[j][i].num)
    return mat


def print_arrays(mat):
    for i in range(len(mat)):
        print(f'{mat[i]},')
    print()


def valid_grid(mat):
    try:
        if len(mat) != 9:
            return False
        for i in range(len(mat)):
            if len(mat[i]) != 9:
                return False
            for j in range(len(mat)):
                if mat[j][i].num < 0 or mat[j][i].num > 9:
                    return False
                if mat[j][i].num != 0:
                    save_num = mat[j][i].num
                    mat[j][i].num = 0
                    if not valid_num(mat, i, j, save_num):
                        return False
                    mat[j][i].num = save_num


    except:
        return False
    else:
        return True

def print_puzzle(mat):
    for i in range(len(mat)):
        for j in range(len(mat)):
            if j % 3 == 0:
                print("|",end="")
            if mat[i][j]!=0:
                print(f'{mat[i][j]}|', end ="")
            else:
                print(f' |',end ="")

            if (j+1)%3==0:
                print(" ",end="")
        print()
        if (i+1)%3==0:
            print()
    print("_"*100)


sudoku_solver(puzzle)
input()

