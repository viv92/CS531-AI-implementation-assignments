import numpy as np
from copy import deepcopy
import random
from queue import PriorityQueue
import time
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#board
#board = np.zeros((4,4))
#visited list
vis = []
#results -
MAX_NODES_LIMIT = 100000
nodes_searched_md = 0
nodes_searched_my = 0
time_taken_mdheuristic = 0
time_taken_myheuristic = 0

#final board
final_board = np.zeros((4,4))

final_board[0][0] = 1
final_board[0][1] = 2
final_board[0][2] = 3
final_board[0][3] = 4
final_board[1][0] = 5
final_board[1][1] = 6
final_board[1][2] = 7
final_board[1][3] = 8
final_board[2][0] = 9
final_board[2][1] = 10
final_board[2][2] = 11
final_board[2][3] = 12
final_board[3][0] = 13
final_board[3][1] = 14
final_board[3][2] = 15
final_board[3][3] = 0


def Scramble(m):
    global final_board
    board_copy = deepcopy(final_board)
    actions = [(0, -1), (0, 1,), (-1, 0 ), (1, 0)]
    row = 3
    col = 3
    k = 0
    while k < m:
        r = random.randint(0, 3)
        i, j = actions[r]
        if row+i < 4 and col+j < 4 and row+i >= 0 and col+j >= 0:
            board_copy[row][col], board_copy[row+i][col+j] = board_copy[row+i][col+j], board_copy[row][col]
            row = row+i
            col = col+j
            k += 1
    return board_copy


#calculate heuristic - Manhattan distance
def MD(b):
    global time_taken_mdheuristic
    t1 = time.time()
    n = b.shape[0]
    h = 0
    for i in range(n):
        for j in range(n):
            num = int(b[i][j])
            #print "num: ", num
            if (num != ((i*n)+j+1)) and (num != 0):
                correct_row = (num-1) / n
                correct_col = (num-1) % n
                h += abs(correct_row - i) + abs(correct_col - j)
                #print "h: ", h
    t2 = time.time()
    time_taken_mdheuristic += (t2-t1)
    return h

#calculate heuristic - frobenius + manhattan
def MY(b):
    global time_taken_myheuristic
    global final_board
    t1 = time.time()
    dif = final_board - b
    #print "dif: ", dif
    frobenius_square = np.trace(np.matmul(dif, dif.transpose()))
    frobenius_norm = math.sqrt(frobenius_square)
    frobenius_norm_sigmoid = 1 / (1 + math.exp(-frobenius_norm/1024.0))
    frobenius_square_sigmoid = 1 / (1 + math.exp(-frobenius_square/1024.0))
    h2 = frobenius_norm_sigmoid

    n = b.shape[0]
    h = 0
    for i in range(n):
        for j in range(n):
            num = int(b[i][j])
            #print "num: ", num
            if (num != ((i*n)+j+1)) and (num != 0):
                correct_row = (num-1) / n
                correct_col = (num-1) % n
                h += abs(correct_row - i) + abs(correct_col - j)

    h += (1*h2)
    t2 = time.time()
    time_taken_myheuristic += (t2-t1)
    return h


def get_next_states(b):
    n = b.shape[0]
    #find zero
    row = 0
    col = 0
    for i in range(n):
        for j in range(n):
            if b[i][j] == 0:
                row = i
                col = j
                break

    # print "Row:", row
    # print "Col:", col
    #generate next states
    container = []
    actions = [(0, -1, 'L'), (0, 1, 'R'), (-1, 0 , 'U'), (1, 0, 'D')]
    for i, j, action in actions:
        if row+i < n and col+j < n and row+i >= 0 and col+j >= 0:
            board_copy = deepcopy(b)
            board_copy[row][col], board_copy[row+i][col+j] = board_copy[row+i][col+j], board_copy[row][col]
            # print "ac: ", action
            # print "bc:\n", board_copy
            container.append((board_copy, action))
    return container


def goal_test(b):
    global final_board
    return (np.all(b == final_board))

def FLS(f_limit, q, hfun):
    global vis
    global nodes_searched_md
    global nodes_searched_my
    if q.empty():
        return ("not found", f_limit, [])
    (f_score, g_score, current_board, action_sequence) = q.get()
    #print "current_board: \n", current_board
    vis.append(current_board)
    if hfun == MD:
        nodes_searched_md += 1
        if nodes_searched_md > MAX_NODES_LIMIT:
            return ("not found", f_limit, action_sequence)
    else:
        nodes_searched_my += 1
        if nodes_searched_my > MAX_NODES_LIMIT:
            return ("not found", f_limit, action_sequence)
    #print "action_sequence_yet: ", action_sequence
    #print "node name = ", node.name
    #print "node f_score = ", f_score
    if goal_test(current_board):
        return ("done", f_limit, action_sequence)
    if f_score > f_limit:
        return ("f_limit exceeded", f_score, action_sequence)

    m_limit = float('inf')
    msg = "not found"
    next_states = get_next_states(current_board)
    for next_board, action in next_states:

        #print "action: ", action
        #print "next_board:\n", next_board
        #check if state already encountered
        vis_flag = False
        for item in vis:
            if np.all(item == next_board):
                vis_flag = True
                break

        if not vis_flag:
            child_g_score = 1 + g_score
            child_f_score = child_g_score + hfun(next_board)
            #print "child_g_score: ", child_g_score
            #print "child_f_score: ", child_f_score
            action_seq = list(action_sequence)
            action_seq.append(action)
            q.put((child_f_score, child_g_score, next_board, action_seq))
            msg, lim, seq = FLS(f_limit, q, hfun)
            if msg == "done":
                #print "action_sequence2: ", action_sequence
                return (msg, f_limit, seq)
            if m_limit > lim:
                m_limit = lim

    return (msg, m_limit, action_sequence)


def idastar(board, hfun):
    global vis
    #initial f_limit
    g_score = 0
    f_score =  hfun(board) + g_score
    f_limit = f_score
    msg = "not done"
    while msg != "done" and msg != "not found":
        q = PriorityQueue()
        action_sequence = []
        q.put((f_score, g_score, board, action_sequence))
        msg, f_limit, seq = FLS(f_limit, q, hfun)
        #print "F:", f_limit, " msg: ", msg
        #print "final action sequence: ", seq
        #clean visits
        vis = []
    return (msg, seq)

def start_rbfs(board, depth):
    node = rbfs(board, depth, counter = 0, f_limit = 10000)
    print("I'm done here?")

def rbfs(board, depth, counter, f_limit):
    global vis
    #initial f_limit

    # print("F_value: ", f_limit)

    counter += 1

    if counter > depth:
        print("EXTERMINAAAAAAAATE.")
        return board, None

    if goal_test(board):
        return board, None

    q = []
    children = get_next_states(board)

    while len(children):

        for child in children:
            h1 = MY(child[0])
            h2 = MD(child[0])
            h_score = h1 + h2
            q.append((h_score, child[0]))

        q.sort()
        best_node = q[0]
        alternative = q[1]

        if best_node[0] > f_limit:
            return [], best_node

        result, best_node = rbfs(best_node[1], depth, counter, min(f_limit, alternative[0]))
        # q[0] = (best_node[0], best_node)

        if len(result) != 0:
            break

    return result, None

def main():
    global nodes_searched_md
    global nodes_searched_my
    global time_taken_mdheuristic
    global time_taken_myheuristic
    M = [10, 20, 30, 40, 50]
    gr_time_taken_md = []
    gr_time_taken_my = []
    gr_nodes_searched_md = []
    gr_nodes_searched_my = []
    gr_solution_length_md = []
    gr_solution_length_my = []
    gr_fr_time_taken_heuristic_md = []
    gr_fr_time_taken_heuristic_my = []
    gr_fr_solved_md = []
    gr_fr_solved_my = []
    N = 10
    for m in M:
        solution_length_md = 0
        solution_length_my = 0
        time_taken_md = 0
        time_taken_my = 0
        time_taken_mdheuristic = 0
        time_taken_myheuristic = 0
        nodes_searched_md = 0
        nodes_searched_my = 0
        fraction_solved_md = 0
        fraction_solved_my = 0
        for n in range(N):
            board = Scramble(m)
            #MD
            start_time = time.time()
            print("---------------------")
            start_rbfs(board, m+10)
            print("---------------------")
            msg, seq = idastar(board, MD)
            end_time = time.time()
            time_taken_md += (end_time - start_time)
            solution_length_md += len(seq)
            if msg == "done":
                fraction_solved_md += 1
            #MY
            start_time = time.time()
            msg, seq = idastar(board, MY)
            end_time = time.time()
            time_taken_my += (end_time - start_time)
            solution_length_my += len(seq)
            if msg == "done":
                fraction_solved_my += 1
        print("\nm = ", m)
        print("--MD--")
        time_taken_md /= float(fraction_solved_md)
        time_taken_mdheuristic /= float(fraction_solved_md)
        fraction_solved_md /= 10.0
        #solution_length_md *= fraction_solved_md
        #nodes_searched_md *= fraction_solved_md
        print("fraction of problems solved: ", (fraction_solved_md))
        print("average solution length: ", (solution_length_md))
        print("average number of nodes_searched: ", (nodes_searched_md))
        print("average time taken: ", (time_taken_md))
        print("average time spent on calculating heuristic: ", (time_taken_mdheuristic))
        print("fraction of time spent on calculating heuristic: ", (time_taken_mdheuristic/time_taken_md))
        gr_fr_solved_md.append(fraction_solved_md)
        gr_solution_length_md.append(solution_length_md)
        gr_nodes_searched_md.append(nodes_searched_md)
        gr_time_taken_md.append(time_taken_md)
        gr_fr_time_taken_heuristic_md.append(time_taken_mdheuristic/time_taken_md)

        print("--MY--")
        time_taken_my /= float(fraction_solved_my)
        time_taken_myheuristic /= float(fraction_solved_my)
        fraction_solved_my /= 10.0
        #solution_length_my *= fraction_solved_my
        #nodes_searched_my *= fraction_solved_my
        #time_taken_my *= fraction_solved_my
        #time_taken_myheuristic *= fraction_solved_my
        print("fraction of problems solved: ", (fraction_solved_my))
        print("average solution length: ", (solution_length_my))
        print("average number of nodes_searched: ", (nodes_searched_my))
        print("average time taken: ", (time_taken_my))
        print("average time spent on calculating heuristic: ", (time_taken_myheuristic))
        print("fraction of time spent on calculating heuristic: ", (time_taken_myheuristic/time_taken_my))
        gr_fr_solved_my.append(fraction_solved_my)
        gr_solution_length_my.append(solution_length_my)
        gr_nodes_searched_my.append(nodes_searched_my)
        gr_time_taken_my.append(time_taken_my)
        gr_fr_time_taken_heuristic_my.append(time_taken_myheuristic/time_taken_my)

    plt.figure()
    plt.plot(M, gr_fr_solved_md, label = "heuristic_MD",color='blue', linestyle='solid', linewidth = 1.5 )
    plt.plot(M, gr_fr_solved_my, label = "heuristic_MY",color='red', linestyle='solid', linewidth = 1.5 )
    plt.xlabel('M', fontsize=12)
    plt.ylabel('Fraction of problems solved')
    plt.title('Fraction of problems solved by Iterative Deepening A*', fontsize=11)
    plt.legend()
    plt.grid()
    # changingY-axis range
    #x1,x2,y1,y2 = plt.axis()
    plt.savefig("IDA_fraction_problems_solved.png", dpi = 300,bbox_inches="tight")

    plt.figure()
    plt.plot(M, gr_solution_length_md, label = "heuristic_MD",color='blue', linestyle='solid', linewidth = 1.5 )
    plt.plot(M, gr_solution_length_my, label = "heuristic_MY",color='red', linestyle='solid', linewidth = 1.5 )
    plt.xlabel('M', fontsize=12)
    plt.ylabel('Optimal solution length')
    plt.title('Optimal solution length (average) obtained by Iterative Deepening A*', fontsize=11)
    plt.legend()
    plt.grid()
    # changingY-axis range
    #x1,x2,y1,y2 = plt.axis()
    plt.savefig("IDA_solution_length.png", dpi = 300,bbox_inches="tight")

    plt.figure()
    plt.plot(M, gr_nodes_searched_md, label = "heuristic_MD",color='blue', linestyle='solid', linewidth = 1.5 )
    plt.plot(M, gr_nodes_searched_my, label = "heuristic_MY",color='red', linestyle='solid', linewidth = 1.5 )
    plt.xlabel('M', fontsize=12)
    plt.ylabel('Number of nodes searched')
    plt.title('Number of nodes searched (average) by Iterative Deepening A*', fontsize=11)
    plt.legend()
    plt.grid()
    # changingY-axis range
    #x1,x2,y1,y2 = plt.axis()
    plt.savefig("IDA_nodes_searched.png", dpi = 300,bbox_inches="tight")

    plt.figure()
    plt.plot(M, gr_time_taken_md, label = "heuristic_MD",color='blue', linestyle='solid', linewidth = 1.5 )
    plt.plot(M, gr_time_taken_my, label = "heuristic_MY",color='red', linestyle='solid', linewidth = 1.5 )
    plt.xlabel('M', fontsize=12)
    plt.ylabel('Time taken')
    plt.title('Time taken (average) to solve a problem by Iterative Deepening A*', fontsize=11)
    plt.legend()
    plt.grid()
    # changingY-axis range
    #x1,x2,y1,y2 = plt.axis()
    plt.savefig("IDA_time_taken.png", dpi = 300,bbox_inches="tight")

    plt.figure()
    plt.plot(M, gr_fr_time_taken_heuristic_md, label = "heuristic_MD",color='blue', linestyle='solid', linewidth = 1.5 )
    plt.plot(M, gr_fr_time_taken_heuristic_my, label = "heuristic_MY",color='red', linestyle='solid', linewidth = 1.5 )
    plt.xlabel('M', fontsize=12)
    plt.ylabel('Fraction of time spent on calculating heuristic')
    plt.title('Fraction of time spent on calculation heuristic by Iterative Deepening A*', fontsize=11)
    plt.legend()
    plt.grid()
    # changingY-axis range
    #x1,x2,y1,y2 = plt.axis()
    plt.savefig("IDA_fr_time_taken_heuristic.png", dpi = 300,bbox_inches="tight")

if __name__ == '__main__':
    main()
