# References:
# https://gist.github.com/flatline/838202
# https://www.cs.princeton.edu/courses/archive/spr21/cos226/assignments/8puzzle/specification.php 
# https://stackoverflow.com/questions/36108269/does-8-puzzle-solvability-rules-work-for-any-goal-state 
# https://stackoverflow.com/questions/36118077/how-to-draw-a-9x9-grid-in-python

from puzzle import EightPuzzle

def check_valid_board(board):
    flat_board = sum(board, [])
    for i in range(len(flat_board)):
        if i not in flat_board:
            return False
    return True

goal_board = [[1,2,3,4,5],
              [6,7,8,9,10],
              [11,12,13,14,15],
              [16,17,18,19,20],
              [21,22,23,24,0]]

initial_board = [[1,2,3,4,5],
                 [6,7,8,9,10],
                 [11,12,13,14,15],
                 [16,17,18,0,20],
                 [21,22,23,19,24]]

def main():

    # board_size = input("Board size: ")
    # if board_size.isnumeric():
    #     board_size = int(board_size)
    # else:
    #     print("Invalid input: must enter an integer")

    # print("From left to right and top to bottom, enter the goal board one number at a time (with 0 as the blank): ")
    # goal_board = [[int(input()) for i in range(board_size)] for i in range(board_size)]

    # print("From left to right and top to bottom, enter the puzzle one number at a time (with 0 as the blank): ")
    # initial_board = [[int(input()) for i in range(board_size)] for i in range(board_size)]

    if not check_valid_board(goal_board):
        print("Invalid goal board")
        return
    elif not check_valid_board(initial_board):
        print("Invalid puzzle")
        return

    puzzle = EightPuzzle(puzzle = initial_board, goal_board = goal_board)
    print("Entered puzzle: \n" + puzzle.__str__())

    solution_path, directions, num_steps = puzzle.solve()

    if not solution_path:
        print("This puzzle is not solvable!")
        return

    wanted_soln = input("For a full solution, enter 'all'. For the best next step, enter 'next': ").lower()
    if wanted_soln == 'all':
        for step, direction in zip(solution_path, directions): 
            print(direction)
            print(step)
        if num_steps == 1: 
            print("Solved in " + str(num_steps) + " step")
        else:
            print("Solved in " + str(num_steps) + " steps")
    elif wanted_soln == 'next':
        index = 0
        print(directions[index])
        print(solution_path[index])

        if num_steps == 1: 
            print("Solved in " + str(num_steps) + " step")
            pass
        
        index += 1
        
        while(True):
            user = input("For the best next step, enter 'next': ").lower()
            if user == 'next':
                print(directions[index])
                print(solution_path[index])
                if index == len(solution_path) - 1:
                    print("Solved in " + str(num_steps) + " steps")
                    break
                index += 1
            else:
                print("Byee")
            
    else:
        print("Invalid input: check your spelling")

if __name__ == "__main__":
    main()