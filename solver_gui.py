import tkinter as tk
import time
from class_square import Square


# TODO
# Move through tiles with arrowkeys
# Use entry.bind
# create function that changes entry widget accordingly

# TODO
# Change item colours to look nicer

# TODO
# Change window into a class

def grid_full(grid):
    for row in grid:
        for square in row:
            if square.return_num() == 0:
                return False
    return True


def test_number(y, x, n, grid):
    for xx in range(0, 9):
        if grid[y][xx].return_num() == n:
            return False

    for yy in range(0, 9):
        if grid[yy][x].return_num() == n:
            return False

    x0 = (x // 3) * 3
    y0 = (y // 3) * 3

    for j in range(0, 3):
        for k in range(0, 3):
            if grid[y0 + j][x0 + k].return_num() == n:
                return False

    return True


def solve(grid, layout, root):
    square = least_possibilities(grid)

    for num in square.return_possible():
        square.change_num(num)
        cordinates = square.return_cordinates()
        change_num(cordinates[0], cordinates[1], num, layout)
        change_colour(cordinates[0], cordinates[1], layout, root, "green")
        root.update()

        if grid_full(grid):
            return

        get_possibilities(grid)

        solve(grid, layout, root)

        if grid_full(grid):
            return

        else:
            square.change_num(0)
            change_num(cordinates[0], cordinates[1], 0, layout)
            change_colour(cordinates[0], cordinates[1], layout, root, "red")
            root.update()


def make_grid(grid):
    squares = []
    for y in range(9):
        squares.append([])
        for x in range(9):
            square = Square(grid[y][x], y, x)
            squares[y].append(square)

    return squares


def get_possibilities(grid):
    for row in grid:
        for square in row:
            if square.is_zero():
                for n in range(1, 10):
                    cordinates = square.return_cordinates()
                    x = cordinates[0]
                    y = cordinates[1]
                    if n not in square.return_possible():
                        if test_number(x, y, n, grid):
                            square.add_possible(n)
                    else:
                        if not test_number(x, y, n, grid):
                            square.remove_possible(n)


def least_possibilities(grid):
    the_square = None

    least = 10

    for row in grid:
        for square in row:
            if square.return_num() == 0 and square.number_of_possibilities() < least:
                the_square = square
                least = square.number_of_possibilities()

    return the_square


def solver(layout, root, info_label, empty_btn, start_button):
    empty_btn.config(state='disabled')
    start_button.config(state='disabled')

    grid = []
    if get_values_from_gui(grid, layout, info_label):

        square_grid = make_grid(grid)

        if not grid_full(square_grid):
            info_label.config(text="SOLVING")

            get_possibilities(square_grid)
            solve(square_grid, layout, root)

            if grid_full(square_grid):
                ready_text = "SOLUTION"

            else:
                ready_text = "No solution"

        else:
            ready_text = "No empty places!"

        info_label.config(text=ready_text)

    empty_btn.config(state='normal')
    start_button.config(state='normal')


def create_empty_grid(root):
    grid = []
    for r in range(9):
        row = []
        for c in range(9):
            entry = tk.Entry(root, justify='center', font=('Verdana', 20), width=2)
            entry.insert(-1, '0')
            row.append(entry)
        grid.append(row)

    return grid


def change_num(y, x, new, layout):
    layout[y][x].delete(0, 'end')
    layout[y][x].insert(-1, new)


def change_colour(y, x, layout, root, color):
    layout[y][x].config(bg=color)
    root.update()
    time.sleep(0.04)

    reset_colour(y, x, layout)


def reset_colour(y, x, layout):
    if (y in (0, 1, 2, 6, 7, 8) and x in (3, 4, 5) or
            (y in (3, 4, 5) and x in (0, 1, 2, 6, 7, 8))):
        layout[y][x].config(bg='light blue')
    else:
        layout[y][x].config(bg="white")


def get_values_from_gui(grid, layout, info_label):
    valid = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    for c in range(9):
        row = []
        for r in range(9):
            number = layout[c][r].get()
            if number in valid:
                row.append(int(number))
            else:
                info_label.config(text="Invalid grid")
                layout[c][r].config(bg="red")
                return False

        grid.append(row)

    return True


def empty_board(layout):
    for i in range(9):
        for j in range(9):
            change_num(i, j, '0', layout)
            reset_colour(i, j, layout)


def fill_with_example(example, layout):
    for i in range(9):
        for j in range(9):
            change_num(i, j, str(example[i][j]), layout)
            reset_colour(i, j, layout)


def main():
    root = tk.Tk()
    root.title("SUDOKU SOLVER")
    root.config(bg="#49637A")
    root.geometry("360x425")
    root.resizable(0, 0)

    layout = create_empty_grid(root)

    start_button = tk.Button(root, text="START", bg="#497A5D", font=('Verdana', 14),
                             command=lambda: solver(layout, root, info_label, empty, start_button))
    start_button.grid(row=0, column=0, columnspan=4, sticky='w', padx=1, pady=1)

    info_label = tk.Label(text="press start", font=('Verdana', 12), bg='#49637A')
    info_label.grid(row=0, column=4, columnspan=6, sticky='w', padx=1, pady=1)

    empty = tk.Button(root, text="EMPTY", bg="#497A8D", font=('Verdana', 14),
                      command=lambda: empty_board(layout))
    empty.grid(row=0, column=8, columnspan=4, sticky='e')


    for c in range(9):
        for r in range(9):
            reset_colour(c, r, layout)
            layout[c][r].grid(row=c + 1, column=r + 1, padx=1, pady=1)

    example = [[0, 0, 0, 3, 0, 7, 0, 0, 0],
               [0, 0, 5, 0, 0, 9, 0, 7, 0],
               [0, 0, 0, 0, 0, 4, 0, 0, 2],
               [0, 8, 0, 0, 0, 0, 0, 2, 0],
               [0, 0, 0, 0, 0, 0, 6, 0, 0],
               [4, 1, 0, 8, 0, 0, 0, 0, 5],
               [6, 0, 9, 0, 0, 1, 0, 0, 4],
               [7, 0, 0, 2, 0, 0, 0, 0, 0],
               [8, 3, 0, 0, 9, 0, 1, 0, 0]]

    example_hard_btn = tk.Button(root, text="Example sudoku", bg="#497A5D", font=('Verdana', 14),
                                 command=lambda: fill_with_example(example, layout))

    example_hard_btn.grid(row=12, column=0, columnspan=6, sticky="w")

    root.mainloop()


if __name__ == '__main__':
    main()
