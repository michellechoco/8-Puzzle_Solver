import math

class EightPuzzle:

    def __init__(self, puzzle: list, goal_board: list):
        self.h_score = 0       # heuristic value
        self.depth = 0         # search depth of current instance
        self.parent = None     # parent node in search path
        self.adj_matrix = puzzle.copy()
        self.goal_board = goal_board.copy()
        self.board_size = len(self.adj_matrix)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj_matrix == other.adj_matrix

    def __str__(self):

        def int_len(num: int):
            if num > 0:
                length = int(math.log10(num)) + 1
            elif num == 0:
                length = 1
            return length

        largest_num = self.board_size ** 2 - 1
        longest_length = int_len(largest_num)

        board_str = ''
        for i in range(self.board_size):
            for j in range(self.board_size):
                board_str += ' '*(longest_length - int_len(self.adj_matrix[i][j]) + 1)
                board_str += str(self.adj_matrix[i][j])
            board_str += '\r\n'
        return board_str

    def clone(self):
        clone_puzzle = []
        for i in range(self.board_size):
            clone_puzzle.append(self.adj_matrix[i][:])
        clone_goal_board = self.goal_board.copy()
        p = EightPuzzle(clone_puzzle, clone_goal_board)
        return p

    def swap(self, pos_a, pos_b):
        """Swaps the values at the specified coordinates"""
        row_a, col_a = pos_a
        row_b, col_b = pos_b
        temp = self.adj_matrix[row_a][col_a]
        self.adj_matrix[row_a][col_a] = self.adj_matrix[row_b][col_b]
        self.adj_matrix[row_b][col_b] = temp

    def get_neighbors(self):
        """Returns neighbor boards"""
        # get row and column of the blank tile
        blank_row, blank_col = find_tile(self.adj_matrix, 0)
        neighbor_tiles = []
        
        # find which tiles can swap with the blank
        if blank_row > 0:
            neighbor_tiles.append((blank_row - 1, blank_col))
        if blank_col > 0:
            neighbor_tiles.append((blank_row, blank_col - 1))
        if blank_row < self.board_size - 1:
            neighbor_tiles.append((blank_row + 1, blank_col))
        if blank_col < self.board_size - 1:
            neighbor_tiles.append((blank_row, blank_col + 1))

        def swap_and_clone(blank_pos, neighbor_pos):
            neighbor = self.clone()
            neighbor.swap(blank_pos, neighbor_pos)
            neighbor.depth = self.depth + 1
            neighbor.parent = self
            return neighbor

        neighbor_boards = map(lambda neighbor_pos: swap_and_clone((blank_row, blank_col), neighbor_pos), neighbor_tiles)
        return neighbor_boards

    def solution_path(self, path):
        if self.parent == None:
            return path
        else:
            path.append(self)
            return self.parent.solution_path(path)

    def solve(self):
        """Performs A* search for goal state.
        Uses manhattan distance as heuristic.
        """
        def is_solved(puzzle):
            return puzzle.adj_matrix == self.goal_board

        if is_solved(self):
            return self.format_solution([self], self.depth)   # already solved! 
        
        if not self.is_solvable():
            return self.format_solution([], 0)

        self.h_score = h_manhattan(self)
        open = [self]
        closed = []

        while open:
            curr_board = open.pop(0)

            curr_neighbors = curr_board.get_neighbors()
            for neighbor in curr_neighbors:

                if (is_solved(neighbor)):
                    return self.format_solution(neighbor.solution_path([]), neighbor.depth)

                neighbor.h_score = h_manhattan(neighbor)
                neighbor_f_score = neighbor.depth + neighbor.h_score

                if neighbor not in open and neighbor not in closed:
                    open.append(neighbor)

                elif neighbor in open:
                    open_index = open.index(neighbor)
                    open_neighbor = open[open_index]

                    # if the version of neighbor within open has a higher f score, replace it with the current version
                    if neighbor_f_score < open_neighbor.depth + open_neighbor.h_score:
                        open_neighbor.depth = neighbor.depth
                        open_neighbor.h_score = neighbor.h_score
                        open_neighbor.parent = neighbor.parent

                elif neighbor in closed:
                    closed_index = closed.index(neighbor)
                    closed_neighbor = closed[closed_index]

                    # if the version of neighbor within closed has a higher f score, remove neighbor from closed and place in open
                    if neighbor_f_score < closed_neighbor.depth + closed_neighbor.h_score:
                        closed.remove(neighbor)
                        open.append(neighbor)

            closed.append(curr_board)
            open = sorted(open, key=lambda puzzle: puzzle.h_score + puzzle.depth)

        # if finished state not found, return failure
        return self.format_solution([], 0)
    
    def format_solution(self, solution, num_moves):
        directions = []

        if not solution or self in solution:    # if there is no solution or the puzzle is already solved
            return solution, directions, num_moves
        
        solution.reverse()
        
        def direction_moved(initial_state, next_state):
            i_row, i_col = find_tile(initial_state.adj_matrix, 0)
            n_row, n_col = find_tile(next_state.adj_matrix, 0)

            if i_row > n_row:
                return "UP"
            if i_row < n_row:
                return "DOWN"
            if i_col > n_col:
                return "LEFT"
            if i_col < n_col:
                return "RIGHT"
        
        directions.append(direction_moved(self, solution[0]))
        for i in range(len(solution) - 1):
            directions.append(direction_moved(solution[i], solution[i + 1]))
        
        return solution, directions, num_moves

    def is_solvable(self):
        
        def count_inversions(state: list):
            inversions = 0
            for i in range(len(state)):
                for j in range(i, len(state)):
                    curr_val = state[i]
                    compare_val = state[j]
                    if curr_val > compare_val:
                        inversions += 1
            return inversions

        # flattening the 2D lists 
        initial_state = sum(self.adj_matrix, [])
        goal_state = sum(self.goal_board, [])

        # removing blank tiles
        initial_state.remove(0)
        goal_state.remove(0)

        initial_state_inversions = count_inversions(initial_state)
        goal_state_inversions = count_inversions(goal_state)
        
        return initial_state_inversions % 2 == goal_state_inversions % 2 

def find_tile(matrix: list, value: int):
    """returns the row, col coordinates of the specified tile
        in the matrix"""
    board_size = len(matrix)
    if value < 0 or value > board_size ** 2 - 1:
        raise Exception("Value out of range")

    for row in range(board_size):
        for col in range(board_size):
            if matrix[row][col] == value:
                return row, col

def h_manhattan(curr_board: EightPuzzle):
    h = 0
    for i in range(curr_board.board_size ** 2 - 1):
        curr_x, curr_y = find_tile(curr_board.adj_matrix, i)
        goal_x, goal_y = find_tile(curr_board.goal_board, i)
        h += abs(curr_x - goal_x) + abs(curr_y - goal_y)
    return h