# Reilly McBride 9/6/17
# White Period 5
# Note: When I ran this on repl.it (my computer died) it was about 14.5 seconds to solve all 32 sample puzzles.

# main: generate string, turn it into a node, run BFS

import random
import collections
from time import time


class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.children = []


def make_move(str, dir, index):  # gets the string of current state, pos to move to, index of 0
    ind = index
    # j = ind % 3
    # i = ind // 3 #integer division
    # jtwo = dir % 3
    # itwo = dir // 3

    char = str[dir]
    string1 = str.replace(char, '0')
    string2 = string1[:index] + char + string1[index + 1:]

    # string = swap(i, j, str, itwo, jtwo)

    # return string
    return string2
    # check if move is viable
    # add whatever move to visited states list


def swap(i, j, str, changeI, changeJ):
    char = get_ij(str, changeI, changeJ)  # character in place you want to move 0 to
    string1 = set_ij(str, changeI, changeJ, "0")  # put 0 in above char's place
    string2 = set_ij(string1, i, j, char)  # put char in 0's old place
    return string2


def goal_test(str):
    return str == '012345678'


def get_ij(str, i, j):
    return str[(i * 3) + j]  # returns the character


def set_ij(str, i, j, c):  # c is what you want to put in i,j
    index = (i * 3) + j
    newStr = str[:index] + c + str[index + 1:]
    return newStr


def path(node):
    path = []
    curr = node
    path.append(curr.state)

    while curr.parent:
        path.append(curr.parent.state)
        curr = curr.parent

    path2 = path[::-1]
    # for i in path2:
    #    print(i)
    print("Puzzle: " + path2[0])
    print("LENGTH = " + str(len(path2)))


def bfs(root):
    # make visited a SET -> constant time lookups
    # make fringe a deque() -> constant time updates

    queue = collections.deque()
    queue.append(root)
    visited = set()  # set of strings, not nodes (easier to hash a string than a node!)
    while queue:
        child = queue.popleft()
        if (goal_test(child.state)):
            path(child)
            return
        index = child.state.index('0')

        dict = {0: [1, 3], 1: [0, 2, 4], 2: [1, 5], 3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8], 6: [3, 7],
                7: [6, 4, 8], 8: [7, 5]}
        for i in dict[index]:
            grandkid = Node(make_move(child.state, i, index), child)
            if grandkid.state not in visited:
                queue.append(grandkid)
                visited.add(grandkid.state)

    if not queue:
        print("Impossible to solve.")


def randString():
    list = [i for i in range(0, 9)]
    random.shuffle(list)
    return ''.join(list)


if __name__ == "__main__":
    f = open("puzzles.txt", 'r')
    l = f.read().splitlines()

    tic = time()  # time at the beginning
    for i in l:
        curr = i
        root = Node(curr, None)
        bfs(root)
    toc = time()  # time after bfs is completed
    print("Execution time: %5.2f seconds" % (toc - tic))


