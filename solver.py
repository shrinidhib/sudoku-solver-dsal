def present_in_row(sudoku_board,row,num):
    for r in range(9):
        if sudoku_board[row][r]==num:
            return True
    return False

def present_in_col(sudoku_board,col,num):
    for r in range(9):
        if sudoku_board[r][col]==num:
            return True
    return False

def present_in_box(sudoku_board,rstart,cstart,num):
    for r in range(3):
        for c in range(3):
            if sudoku_board[r+rstart][c+cstart]==num:
                return True
    return False

def has_to_be_filled(sudoku_board):
    for r in range(9):
        for c in range(9):
            if sudoku_board[r][c]==0:
                return (r,c)
    return False

def is_valid(sudoku_board,row,col,num):
    return not(present_in_row(sudoku_board,row,num)) and not(present_in_col(sudoku_board,col,num)) and not(present_in_box(sudoku_board,row-row%3,col-col%3,num))


def solver(sudoku_board):
    coord=has_to_be_filled(sudoku_board)
    if coord==False:
        return True
    else:
        row,col=coord
    for i in range(1,10):
        if is_valid(sudoku_board,row,col,i):
            sudoku_board[row][col]=i
            if solver(sudoku_board):
                return True
            sudoku_board[row][col]=0
    return False


