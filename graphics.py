import datetime
from tkinter import Tk, BOTH, Canvas
from time import sleep
from random import seed, choice

class Window:
    def __init__(self, width, height):
        self.__tk = Tk()
        self.__tk.title("Maze Solver")
        self.__canvas = Canvas(self.__tk, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__is_running = False
        self.__tk.protocol("WM_DELETE_WINDOW", self.close)
        
    def redraw(self):
        self.__tk.update_idletasks()
        self.__tk.update()
    
    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)
    
    def get_canvas(self):
        return self.__canvas
    
    def close(self):
        self.__is_running = False    

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, fill_color):
        self._id = canvas.create_line(self.p1.x, self.p1.y,
                           self.p2.x, self.p2.y,
                           fill = fill_color, width = 2)
    
    def get_id(self):
        return self._id

class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        self.__win = win
        self.visited = False

    def draw(self, fill_color="black"):
        self.__p1 = Point(self.__x1, self.__y1)
        self.__p2 = Point(self.__x2, self.__y1)
        self.__p3 = Point(self.__x2, self.__y2)
        self.__p4 = Point(self.__x1, self.__y2)
        if self.has_top_wall:
            self.__l1 = Line(self.__p1, self.__p2)
            self.__l1.draw(self.__win.get_canvas(), fill_color)
        if self.has_right_wall:
            self.__l2 = Line(self.__p2, self.__p3)
            self.__l2.draw(self.__win.get_canvas(), fill_color)
        if self.has_bottom_wall:
            self.__l3 = Line(self.__p3, self.__p4)
            self.__l3.draw(self.__win.get_canvas(), fill_color)
        if self.has_left_wall:
            self.__l4 = Line(self.__p4, self.__p1)
            self.__l4.draw(self.__win.get_canvas(), fill_color)
        
    def draw_move(self, to_cell, undo=False):
        self.__m1x = (self.__x1 + self.__x2)/2
        self.__m1y = (self.__y1 + self.__y2)/2
        self.__m2x = (to_cell.__x1 + to_cell.__x2)/2
        self.__m2y = (to_cell.__y1 + to_cell.__y2)/2
        self.__m1 = Point(self.__m1x, self.__m1y)
        self.__m2 = Point(self.__m2x, self.__m2y)
        self.__l1 = Line(self.__m1, self.__m2)
        if undo:
            self.__l1.draw(self.__win.get_canvas(), "grey")
        else:
            self.__l1.draw(self.__win.get_canvas(), "red")
    
    def get_id_top(self):
        return self.__l1.get_id()
    
    def get_id_right(self):
        return self.__l2.get_id()
    
    def get_id_bottom(self):
        return self.__l3.get_id()
    
    def get_id_left(self):
        return self.__l4.get_id()

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed:
            self.seed = seed(seed)

        self._create_cells()
    
    def _create_cells(self):
        print("Generating grid...")
        self._cells = []
        for i in range(self.num_cols):
            cols = []
            for j in range(self.num_rows):
                cols.append(Cell(
                    self.x1 + i*self.cell_size_x,
                    self.y1 + j*self.cell_size_y,
                    self.x1 + i*self.cell_size_x + self.cell_size_x,
                    self.y1 + j*self.cell_size_y + self.cell_size_y,
                    self.win
                ))
            self._cells.append(cols)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cells(i, j)
    
    def _draw_cells(self, i ,j):
        if self.win:
            self._cells[i][j].draw()
            self._animate()
    
    def _animate(self):
        self.win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self):
        print("Creating entry and exit...")
        self._cells[0][0].has_top_wall = False
        self._cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = False
        if self.win:
            canvas = self.win.get_canvas()
            canvas.delete(self._cells[0][0].get_id_top())
            canvas.delete(self._cells[self.num_cols-1][self.num_rows-1].get_id_bottom())
        
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            #check top
            if (j - 1 >= 0) and not self._cells[i][j-1].visited:
                to_visit.append((i,j-1))
            #check right
            if (i + 1 < self.num_cols) and not self._cells[i+1][j].visited:
                to_visit.append((i+1,j))
            #check bottom
            if (j + 1 < self.num_rows) and not self._cells[i][j+1].visited:
                to_visit.append((i,j+1))
            #check left
            if (i - 1 >= 0) and not self._cells[i-1][j].visited:
                to_visit.append((i-1,j))
            if len(to_visit) == 0:
                if self.win:
                    canvas = self.win.get_canvas()
                    canvas.delete(self._cells[i][j].get_id_top())
                    canvas.delete(self._cells[i][j].get_id_right())
                    canvas.delete(self._cells[i][j].get_id_bottom())
                    canvas.delete(self._cells[i][j].get_id_left())
                    self._draw_cells(i,j)
                    return
            else:
                rand_dir = choice(to_visit)
                l, m = rand_dir[0], rand_dir[1]
                if l > i:
                    self._cells[i][j].has_right_wall = False
                    self._cells[l][m].has_left_wall = False
                elif l < i:
                    self._cells[i][j].has_left_wall = False
                    self._cells[l][m].has_right_wall = False
                elif m > j:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[l][m].has_top_wall = False
                elif m < j:
                    self._cells[i][j].has_top_wall = False
                    self._cells[l][m].has_bottom_wall = False
                self._break_walls_r(l, m)
        
    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False      

        

        