from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.title = "Root"
        self.canvas = Canvas(height=height, width=width)
        self.canvas.pack()
        self.isRunning = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()
        return

    def wait_for_close(self) -> None:
        self.isRunning = True
        while self.isRunning:
            self.redraw()
        return

    def close(self) -> None:
        self.isRunning = False

    def draw_line(self, line: "Line", fillC: str = "black") -> None:
        line.draw(self.canvas, fillC)
        return


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self.__add__(other, self)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        return self.__sub__(other, self)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Point(self.x / other, self.y / other)
        else:
            raise Exception("Only can divide by a number")

    def __repr__(self) -> str:
        return f"Point: ({self.x},{self.y})"


class Line:
    def __init__(self, p1: Point, p2: Point, tag: str = None) -> None:
        self.p1 = p1
        self.p2 = p2
        self.tag = tag

    def draw(self, canv: Canvas, fillC: str):
        canv.create_line(
            self.p1.x,
            self.p1.y,
            self.p2.x,
            self.p2.y,
            fill=fillC,
            width=2,
            tags=self.tag,
        )
