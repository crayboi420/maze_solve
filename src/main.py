from graphics import Window
from structs import Maze


def main():
    win = Window(800, 800)
    maze = Maze(
        x1=10,
        y1=10,
        num_rows=20,
        num_cols=20,
        cell_size_x=30,
        cell_size_y=30,
        win=win,
        # seed=18,
    )

    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
