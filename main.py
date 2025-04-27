import graphics as g
from math import floor

def main():
    screen_width = 800
    screen_height = 600
    win = g.Window(screen_width, screen_height)
    start_x = 10
    start_y = 10
    cell_size_x = 20
    cell_size_y = 20
    num_rows = floor((screen_height - 2*start_y)/cell_size_y)
    num_cols = floor((screen_width - 2*start_x)/cell_size_x)

    maze = g.Maze(
        start_x, start_y, 
        num_rows, num_cols, 
        cell_size_x, cell_size_y, 
        win, seed=0
    )

    maze._break_entrance_and_exit()

    print("Generating maze...")
    maze._break_walls_r(0,0)

    maze._reset_cells_visited()

    maze.solve()

    print("Done.")
    win.wait_for_close()

main()