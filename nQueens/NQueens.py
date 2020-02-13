#Reilly McBride


import collections
import random
from time import time
import math
from matplotlib import pyplot as plt
global n
global nodes_created

class Board:
    def __init__(self, queens, parent, closed, cols):
        global nodes_created
        nodes_created += 1
        self.queens = queens
        self.count = len(queens)
        self.parent = parent
        self.closed = closed
        self.cols = cols

def display(board):
    print()
    for r in range(n):
        temp = "|"
        for c in range(n):
            if (r,c) in board.queens:
                temp += "Q |"
            else:
                temp += "__|"
        print(temp)

def addClosed(closed, queen):
    x,y = queen #queen is a tuple of coordinates
    for var in range(0, n): #add new coordinate pairs to show where a new queen can't be
        closed.add((var, y))
        closed.add((x, var))
        closed.add((var, y+(var-x)))
        closed.add((var, y-(var-x)))
    return closed

def score(child, parent):
    return -1 * len(addClosed(parent.closed.copy(), child))

def gen_children(parent, columns):
    global n
    #col = random.choice(columns)
    min_open = n
    children = []
    for c in columns:
        childs = [(c, y) for y in range(n) if (c, y) not in parent.closed] #pick the column that has the least open spaces
        temp_min = len(childs)
        if temp_min <= min_open:
            min_open = temp_min
            children = childs

    children.sort(key = lambda n: score(n, parent) + random.random())
    return children

def run_iter():
    global n
    c = []
    for x in range(n):
        c.append(x)
    node = Board(set(), None, set(), c)
    fringe = collections.deque()
    fringe.append(node)
    while fringe:
        thing = fringe.pop()
        if thing.count == n: #if it has n queens, its a solution!
            return thing
        cols = thing.cols
        children = gen_children(thing, cols)
        for child in children:
            col_temp = cols.copy()
            col_temp.remove(child[0])
            queens = thing.queens.copy() #add all the queens on the parent board to this board
            queens.add(child) #add a tuple of coordinates for a new queen on the board from the children list
            closed = thing.closed.copy() #the closed set is a copy of the old closed set
            addClosed(closed, child) #add more closed coordinates based on the new queen you just added
            fringe.append(Board(queens, thing, closed, col_temp)) #add a new board that has the parameters you just defined
    return None


if __name__ == "__main__":
    #plt.subplot(number of rows, number of cols, plot you're curr on)
    global nodes_created
    global n
    #n = int(input("Number of queens?"))
    x_vals = []
    y_vals = []
    time_vals = []
    for x in range(5, 202, 10): #do odds 5 through 101
        nodes_created = 0
        n = x
        x_vals.append(x)
        print(x)
        tic = time()
        run_iter()
        toc = time()
        #t = "Time: %5.4f" % (toc - tic)
        t = toc-tic
        y_vals.append(math.log10(nodes_created))
        time_vals.append(t)
        print(nodes_created)
        print(t)
    plt.subplot(2, 1, 1)
    plt.plot(x_vals, y_vals, color = 'r', linewidth = 2.0)
    plt.xlabel("n queens")
    plt.ylabel("nodes")

    plt.subplot(2, 1, 2)
    plt.plot(x_vals, time_vals, color='r', linewidth=2.0)
    plt.xlabel("n queens")
    plt.ylabel("time (s)")

    plt.show()

    #display(run_iter())

