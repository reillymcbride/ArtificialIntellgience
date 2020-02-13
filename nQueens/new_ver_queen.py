import random
from matplotlib import pyplot as plt
import math
import sys
from time import time
global COUNT #node_counter

#import numpy as np # could use for plot
#state = (list, dict)
#list is rows
#dictionary is col and values
# var = most restricted value

def initial_state(n):
    return([-1]*n, {i: set(range(n)) for i in range(n)})
    #starts with a list of rows all w/ value -1,  a dictionary with co1s 0 thru n with sets of 0 thru n available spaces in each col
    #the index of the list represents which column its in, the value is where the queen is in that column

def goal_test(state):
    if -1 in state[0]:
        return False
    return True

def get_next_unassigned_var(state): #chooses a col
    vals = []
    for key in state[1].keys():
        if state[0][key] == -1:
            vals.append(key)
    #print(vals)
    vals.sort(key = lambda x: len(state[1].get(x)) + random.random()) #sort the keys based on the length of their corresp. sets
    #print("key: " + str(vals[0]))
    return vals[0] #returns the dict key

def get_sorted_values(state, var): #sorts value in a col to be looped through, var is set
    col = list(state[1].get(var))
    #col.sort(key = lambda n: n)
    col.sort(key = lambda n: abs(n - len(state[1])/2))
    #print("col: " + str(col))
    return col

def assign(state, var, value): #var is col, value is row
    x, y = var, value
    state[0][var] = value #change it from original -1, so nothing else will be in that column
    #for each col, it'll take out 3 vals max
    size = len(state[1].keys())
    for col in state[1].keys():
        if col == var: continue
        state[1].get(col).discard(value) #nothing else should be in that row, so remove it for every column
        state[1].get(col).discard(value + abs(col-var))
        state[1].get(col).discard(value - abs(col - var))
        if len(state[1].get(col)) == 0:
            return False


def csp(state):
    global COUNT
    queens, board = state #queens is the list, board is the dictionary
    #print(queens, board)
    if COUNT > 15*len(queens): # random restart!
        (queens, board), COUNT = initial_state(len(queens)), 0
    if goal_test(state):
        #print("success!")
        return state
    COUNT += 1
    var = get_next_unassigned_var(state) #dict key
    for val in get_sorted_values(state, var):
        #print("dict key: " + str(var))
        #print("testing ", val, " in ", state[1])
        new_state = (list(queens), {i: set(board[i]) for i in board}) #same list and dict as started w/
        assign_result = assign(new_state, var, val)
        #print("assres = " , assign_result)
        if assign_result == False: continue #if assign returns False (meaning one col is empty) go to the next val
        result = csp(new_state)
        if result is not False:
            return result
    #print("MAJOR FAIL")
    return False

def display(state):
    if state is None:
        print("No solution")
        return
    print()
    temp = state[0]
    queens = []
    for i in range(len(temp)):
        queens.append((temp[i], i))

    for r in range(len(queens)):
        temp = "|"
        for c in range(len(queens)):
            if (r,c) in queens:
                temp += "Q |"
            else:
                temp += "__|"
        print(temp)

if __name__ == "__main__":
    #plt.subplot(number of rows, number of cols, plot you're curr on)
    #n = int(input("Number of queens?"))
    global COUNT
    x_vals = []
    y_vals = []
    time_vals = []
    for x in range(4, 201): #do odds 5 through 101
        x_vals.append(x)
        print(x)
        tic = time()
        size = x
        COUNT = 0
        sol = csp(initial_state(size))
        toc = time()
       # display(sol)
        #t = "Time: %5.4f" % (toc - tic)
        t = toc-tic
        #y_vals.append(math.log10(COUNT))
        y_vals.append(COUNT)
        time_vals.append(t)
        print(COUNT)
        print(t)
    plt.subplot(2, 1, 1)
    plt.plot(x_vals, y_vals, color = 'r', linewidth = 2.0)
    plt.xlabel("N Queens (Board Size)")
    #plt.ylabel("Nodes log 10)")
    plt.ylabel("Nodes")

    plt.subplot(2, 1, 2)
    plt.plot(x_vals, time_vals, color='r', linewidth=2.0)
    plt.xlabel("N Queens")
    plt.ylabel("Time (s)")

    plt.show()


