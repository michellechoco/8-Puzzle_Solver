from puzzle import EightPuzzle, find_tile
from main import check_valid_board
import time
from turtle import *

BOARD_SIZE = 3
GRID_LENGTH = 75
LETTER_FONT = ('Verdana', 30, 'normal')
NUM_FONT = ('Verdana', 40, 'normal')

# grid positions
x_goal = [-222.5, -222.5+GRID_LENGTH, -222.5+GRID_LENGTH*2]
x_puzzle = [67.5, 67.5+GRID_LENGTH, 67.5+GRID_LENGTH*2]
y = [55, 55-GRID_LENGTH, 55-GRID_LENGTH*2]

def draw_arrow(t, direction: str):
    t.showturtle()
    if direction == 'RIGHT':
        angle = 0
    if direction == 'UP':
        angle = 90
    if direction == 'LEFT':
        angle = 180
    if direction == 'DOWN':
        angle = 270

    t.setheading(angle)
    t.pendown()
    t.fd(50)
    t.penup()
    t.bk(10)
    t.setheading(90 + angle)
    t.fd(11)
    t.setheading(135 + angle)
    t.pendown()
    t.bk(15)
    t.setheading(45 + angle)
    t.bk(15)
    t.penup()
    t.hideturtle()

def draw_board(t, goal_board=False):
    t.showturtle()
    if goal_board:
        t.goto(-260, -100)
    else:
        t.goto(30, -100)

    t.seth(0)
    t.pendown()

    sign = 1
    for _ in range(2):
        for _ in range(BOARD_SIZE):
            t.fd(GRID_LENGTH * BOARD_SIZE)
            t.left(sign * 90)
            t.fd(GRID_LENGTH)
            t.left(sign * 90)
            sign *= -1

        t.fd(GRID_LENGTH * BOARD_SIZE)
        if BOARD_SIZE % 2 != 0:
            t.left(90)
        else:
            t.right(90)
        sign *= -1
    t.penup()
    t.hideturtle()

def fill_board(t, board, goal_board=False):
    if goal_board:
        x = x_goal
    else:
        x = x_puzzle

    for row in (range(BOARD_SIZE)):
        for col in (range(BOARD_SIZE)):
            num = str(board[row][col])
            if num == '0':
                continue
            t.goto(x[col], y[row])   
            t.write(num, align="center", font=NUM_FONT)

def main():
    # creating the turtles
    t_grid = Turtle()
    t_goal = Turtle()
    t_puzzle = Turtle()
    t_arrow = Turtle()

    # screen config
    screen = Screen()
    screen.bgcolor("white")

    # turtle config
    t_arrow.pensize(6)
    t_arrow.color("violet")
    t_grid.hideturtle()
    t_goal.hideturtle()
    t_puzzle.hideturtle()
    t_arrow. hideturtle()

    t_grid.penup()
    t_goal.penup()
    t_puzzle.penup()
    t_arrow.penup()

    print("From left to right and top to bottom, enter the goal board one number at a time (with 0 as the blank): ")
    goal_board = [[int(input()) for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

    print("From left to right and top to bottom, enter the puzzle one number at a time (with 0 as the blank): ")
    initial_board = [[int(input()) for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

    if not check_valid_board(goal_board):
        print("Invalid goal board")
        return
    elif not check_valid_board(initial_board):
        print("Invalid puzzle")
        return
    
    t_grid.goto(-147.5, 135)
    t_grid.pendown()
    t_grid.write("Goal", align="center", font=LETTER_FONT)
    t_grid.penup()
    draw_board(t_grid, goal_board=True)
    fill_board(t_goal, goal_board, goal_board=True)

    t_grid.goto(142.5, 135)
    t_grid.pendown()
    t_grid.write("Puzzle", align="center", font=LETTER_FONT)
    t_grid.penup()
    draw_board(t_grid)
    fill_board(t_puzzle, initial_board)

    puzzle = EightPuzzle(puzzle = initial_board, goal_board = goal_board)
    solution_path, directions, num_steps = puzzle.solve()

    if not solution_path:
        print("This puzzle is not solvable!")
        return
    
    index = 0
    curr_board = puzzle
    while(True):
        user = input("For the best next step, enter 'next': ").lower()
        if user == 'next':

            blank_row, blank_col = find_tile(curr_board.adj_matrix, 0)
            t_arrow.goto(x_puzzle[blank_col], y[blank_row]+30)
            draw_arrow(t_arrow, directions[index])

            time.sleep(2.5)
            t_arrow.clear()
            t_puzzle.clear()
            curr_board = solution_path[index]
            fill_board(t_puzzle, curr_board.adj_matrix)
            
            if index == len(solution_path) - 1:
                if num_steps == 1: 
                    print("Solved in " + str(num_steps) + " step")
                else:
                    print("Solved in " + str(num_steps) + " steps")
                break
            index += 1
        else:
            print("Byee")
            break
            
    screen.exitonclick()

if __name__ == "__main__":
    main()