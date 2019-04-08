import numpy as np

class cell:
    def __init__(self):
        self.val = 0
        self.current_domain = [1,2,3,4]
        self.length_domain = 4


def insert_val(board, i, j, v):
    if board[i][j].val == 0:
        board[i][j].val = v
        board[i][j].current_domain = []
        board[i][j].length_domain = 0
    return board

max_depth = 1000
#board
board = [[cell() for j in range(2)] for i in range(2)]

#initialize using function read from txt
prob = [[1,2,],
[0,0]]
for i in range(2):
    for j in range(2):
        insert_val(board, i, j, prob[i][j])

#checking all filled
def is_goal(b):
    for i in range(2):
        for j in range(2):
            val = b[i][j].val
            if val == 0:
                return False
    return True

#all diff check
def check_all_diff(b):
    dom = [1,2,3,4]
    for i in range(2):
        for j in range(2):
            val = b[i][j].val
            if val == 0:
                continue
            if val in dom:
                dom.remove(val)
            else:
                return False #repeated value
    return True

#constrain prop - checking ALL DIFF for now
def constrain_prop(b):
    flag = True
    flag = flag and check_all_diff(b)
    return flag

#backtracking search
def backtrack_search(board,n):
    if is_goal(board):
        return (True, board)
    if n == 0: #max_depth reached
        return (False, board)
    #pick a cell - baseline
    for i in range(2):
        for j in range(2):
            if board[i][j].val == 0:
                break #position of cell to be considered obtained
    #pick possible values and perform recursion
    for v in board[i][j].current_domain:
        b = insert_val(board, i, j, v)
        if constrain_prop(b):
            flag, b = backtrack_search(b, n-1)
            if flag:
                return (True, b)
    return (False, board)

def main():
    global board
    global max_depth
    flag, board = backtrack_search(board, max_depth)
    if flag:
        for i in range(2):
            for j in range(2):
                print board[i][j]

if __name__ == '__main__':
    main()
