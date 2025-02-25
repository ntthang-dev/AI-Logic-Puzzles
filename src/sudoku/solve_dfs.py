# solve_dfs.py

from utils import find_empty_cell, is_valid

def solve_dfs(board):
    empty_cell = find_empty_cell(board)

    if not empty_cell: 
        return True

    row, col = empty_cell
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_dfs(board):
                return True
            board[row][col] = 0 # Backtracking
    return False