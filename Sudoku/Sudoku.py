#Reilly McBride
#12/6/17

#two heuristics: 1) MRV on squares, or MRV on units (select unit that has one number w/ one possible square, and assign it

import random
from matplotlib import pyplot as plt
import math
import sys
from time import time
global COUNT #node_counter
global INITIAL

sys.setrecursionlimit(5000)

def goal_test(state):
    for key in state.keys():
        if len(state[key]) != 1:
            return False
    return True

def get_next_unassigned_var(state): #chooses a square
    vals = []
    for key in state.keys():
        if len(state[key]) != 1:
            vals.append(key)
    vals.sort(key = lambda x: len(state.get(x)) + random.random()) #sort the keys based on the length of their corresp. sets
    return vals[0] #returns the dict key

def get_sorted_values(state, var): #sorts value in a col to be looped through, var is set
    col = list(state.get(var))
    random.shuffle(col)
    return col
    #could also sort based on which num occurs the least in its peer set:

    #temp = {}
    #col = list(state.get(var)) #list of possible values that the square could take on
    #for val in col:
    #    count = 0
    #    for pal in peers[var]:
    #        if val in state[pal]:
    #            count += 1
    #   temp[val] = count
    #col.sort(key = lambda x: temp[x] + random.random())
    #return col

def assign_two(state):
    for i in range(9):
        freq = 0
        s = ''
        val = ''
        for square in units[i]: #first 9 objects of units are rows
            if chr(i) in state[square]:
                freq += 1
                s += square
                val += chr(i)
        if freq == 1:
            assign(state, s, val, peers)


def assign(state, var, value, peer_set): #var is square, value is value, state is dictionary w/ squares as keys and available values as values
    state[var] = value
    for friend in peer_set[var]:
        size_init = len(state[friend])
        state[friend] = state[friend].replace(value, '')
        size_fin = len(state[friend])
        if size_init != size_fin and size_fin == 1:
            assign(state, friend, state[friend], peer_set)
        if len(state[friend]) == 0:
            return False

#make a separate method that looks at rows/cols/squares, and if theres a value thats only an
#option for one square, call assign for that value in that square

def csp(board, peer_set):
    global COUNT
    global INITIAL
    #queens, board = state
    state = board.copy()
    if COUNT > 15 *len(state):
        state, COUNT = INITIAL, 0
    if goal_test(state):
        return state
    COUNT += 1
    var = get_next_unassigned_var(state) #square
    for val in get_sorted_values(state, var): #value for square
        new_state = state.copy()
        assign_result = assign(new_state, var, val, peer_set)
        if assign_result == False: continue
        assign_two(new_state)
        #call secondary assign method w/ MRV unit heuristic
        result = csp(new_state, peers)
        if result is not False:
            return result
    return False


def all_pairs(A,B):
    return {x+y for x in A for y in B}

def all_pairs_list(A,B):
    return [x+y for x in A for y in B]

def generate_units(rows, cols):
    units = []
    for letter in rows:
        units.append(all_pairs(letter, cols)) #rows

    for number in cols:
        units.append(all_pairs(rows, number)) #cols

    for rowdex in range(0, 7, 3):
        for coldex in range(0, 7, 3):
            r = rows[rowdex:rowdex + 3]
            c = cols[coldex:coldex + 3]
            units.append(all_pairs(r, c))

    return units

def gen_peers(square, units):
    buddies = set()
    for unit in units:
        if square in unit:
            buddies = buddies | unit
    buddies.remove(square)
    return buddies

def gen_state(initial, squares, peers): #the list
    str = "123456789"
    temp = {i: str for i in squares}
    for i in range(81): #loop through the string
        if initial[i] is not '.':
            assign(temp, squares[i], initial[i], peers)
    return temp

def display(state):
    for i in range(9):
        str = ''
        for j in range(9):
            str += state[squares_list[j*9 + i]] + " "
        print(str)

if __name__ == "__main__":
    #string = input("Sudoku board string: ")
    rows = 'ABCDEFGHI'
    cols = '123456789'
    squares = all_pairs(rows, cols) #works!!
    squares_list = all_pairs_list(rows, cols)
    units = generate_units(rows, cols) #works!!
    peers = {} #works yayy

    for square in squares:
        peers[square] = gen_peers(square, units)

    f = open("puzzles.txt", 'r')
    l = f.read().splitlines()

    x_vals = []
    y_vals = []

    for i in l:
        temp = i.split(',')
        number = temp[0]
        string = temp[1]
        x_vals.append(number)

        global INITIAL
        INITIAL = gen_state(string, squares_list, peers)

        global COUNT
        tic = time()
        COUNT = 0
        sol = csp(INITIAL, peers)
        toc = time()
        y_vals.append(toc-tic)
        print(number + " " + string)
        #print(sol)
        display(sol)
        print(COUNT)
        print("Time: %5.4f" % (toc - tic))
        print()

    plt.plot(x_vals, y_vals, color='r', linewidth=2.0)
    plt.xlabel("Number Puzzle (Approx Difficulty)")
    plt.ylabel("Time")

    plt.show()















