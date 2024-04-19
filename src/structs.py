from graphics import Line,Point,Window
import random

class Cell:
    def __init__(
        self,
        corner_points: list[Point],
        win: Window,
        walls: list[bool] = [True, True, True, True],
        visited: bool = False,
        tag: str = None,
    ) -> None:
        """
        walls: L,R,U,D, Default all false
        corner_points: 2 points
        """
        if len(walls) != 4:
            raise Exception("Ay yo wrong walls")
        self.walls = walls.copy()

        if len(corner_points) != 2:
            raise Exception("Give 2 corner points pls")
        self._SW = Point(
            min(corner_points[0].x, corner_points[1].x),
            min(corner_points[0].y, corner_points[1].y),
        )
        self._NE = Point(
            max(corner_points[0].x, corner_points[1].x),
            max(corner_points[0].y, corner_points[1].y),
        )
        self._SE = Point(self._NE.x, self._SW.y)
        self._NW = Point(self._SW.x, self._NE.y)

        self._win = win
        self.tag = tag
        self.visited = visited

    def draw(self) -> None:
        lineL = Line(self._SW, self._NW, ["Cell", self.tag, self.tag + "_L"])
        lineR = Line(self._SE, self._NE, ["Cell", self.tag, self.tag + "_R"])
        lineU = Line(self._NE, self._NW, ["Cell", self.tag, self.tag + "_U"])
        lineD = Line(self._SE, self._SW, ["Cell", self.tag, self.tag + "_D"])
        lines = [lineL, lineR, lineU, lineD]
        for line, state in zip(lines, self.walls):
            if state:
                self._win.draw_line(line)
        return

    def draw_move(self, to_cell: "Cell", undo: bool = False) -> None:
        center1 = (self._SW + self._NE) / 2
        center2 = (to_cell._SW + to_cell._NE) / 2
        lc = Line(center1, center2)
        clr = "red" if undo else "gray"
        lc.draw(self._win.canvas, clr)
        return

class Maze:
    def __init__(
        self,
        x1: float | int,
        y1: float | int,
        num_rows: int,
        num_cols: int,
        cell_size_x: float | int,
        cell_size_y: float | int,
        win: Window,
        seed: int = None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(self.num_rows // 2, self.num_cols // 2)
        self._redraw_cells()
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells: list[list[Cell]] = [
            [None for i in range(self.num_cols)] for j in range(self.num_rows)
        ]
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j] = Cell(
                    [
                        Point(
                            self.x1 + j * self.cell_size_x,
                            self.y1 + i * self.cell_size_y,
                        ),
                        Point(
                            self.x1 + (j + 1) * self.cell_size_x,
                            self.y1 + (i + 1) * self.cell_size_y,
                        ),
                    ],
                    self.win,
                    tag=f"{i}, {j}",
                )
        self._redraw_cells()

    def _redraw_cells(self):
        self.win.canvas.delete("Cell")
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

    def _redraw_cell(self, i: int, j: int):
        self.win.canvas.delete(f"{i}, {j}")
        self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int):
        cell: Cell = self._cells[i][j]
        cell.draw()
        self._animate()

    def _animate(self):
        self.win.redraw()
        # sleep(0.05)

    def _break_entrance_and_exit(self):
        entry: Cell = self._cells[0][0]
        entry.walls = [False, True, True, True]
        self._redraw_cell(0, 0)

        ext: Cell = self._cells[-1][-1]
        ext.walls = [True, False, True, True]
        self._redraw_cell(self.num_rows - 1, self.num_cols - 1)

    def _break_walls_r(self, i: int, j: int):

        self._cells[i][j].visited = True

        while True:

            dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]]
            possible_ij = [
                [d[0], d[1]]
                for d in dirs
                if i + d[0] >= 0
                and i + d[0] < self.num_rows
                and j + d[1] >= 0
                and j + d[1] < self.num_cols
            ]
            valid_ij = [
                poss
                for poss in possible_ij
                if not self._cells[i + poss[0]][j + poss[1]].visited
            ]

            if len(valid_ij) == 0:
                self._redraw_cell(i, j)
                return
            direc = random.randint(0, len(valid_ij) - 1)

            currcell = self._cells[i][j]
            nextcell = self._cells[i + valid_ij[direc][0]][j + valid_ij[direc][1]]

            if valid_ij[direc] == [-1, 0]:
                currcell.walls[3] = False
                nextcell.walls[2] = False
            elif valid_ij[direc] == [1, 0]:
                currcell.walls[2] = False
                nextcell.walls[3] = False
            elif valid_ij[direc] == [0, -1]:
                currcell.walls[0] = False
                nextcell.walls[1] = False
            elif valid_ij[direc] == [0, 1]:
                currcell.walls[1] = False
                nextcell.walls[0] = False
            self._break_walls_r(i + valid_ij[direc][0], j + valid_ij[direc][1])

    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False

    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, i: int, j: int) -> bool:

        curcell = self._cells[i][j]
        curcell.visited = True

        if i == (self.num_rows - 1) and j == (self.num_cols - 1):
            return True

        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        wall_lookup = {
            (1, 0): 2,
            (-1, 0): 3,
            (0, 1): 1,
            (0, -1): 0,
        }

        possible_ij = [
            [d[0], d[1]]
            for d in dirs
            if i + d[0] >= 0
            and i + d[0] < self.num_rows
            and j + d[1] >= 0
            and j + d[1] < self.num_cols
            and not self._cells[i + d[0]][j + d[1]].visited
            and curcell.walls[wall_lookup[d]] == False
        ]
        if len(possible_ij) == 0:
            return False
        found = False
        for ij in possible_ij:
            newx, newy = i + ij[0], j + ij[1]
            nextcell = self._cells[newx][newy]
            answer = self._solve_r(newx, newy)
            found = found or answer
            curcell.draw_move(nextcell, answer)
        return found
