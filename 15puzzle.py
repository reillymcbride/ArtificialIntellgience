# Reilly McBride 9/6/17
# White Period 5

# 15puzzle

import random
import collections
from time import time
import heapq


BLANK = '.'
GOAL_STATE = "ABCDEFGHIJKLMNO."
GOAL_INDEXES = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, BLANK: 15}
SIZE = 4
DICTIONARY = {0: [1, 4], 1: [0, 2, 5], 2: [1, 6, 3], 3: [2, 7], 4: [0, 5, 8], 5: [1, 4, 6, 9], 6: [2, 5, 7, 10],
                7: [3, 6, 11], 8: [4, 9, 12], 9: [5, 8, 10, 13], 10: [6, 9, 11, 14], 11: [7, 10, 15], 12: [8, 13],
                13: [12, 9, 14], 14: [13, 10, 15], 15: [11, 14]}
NODES_CREATED = 0

class Node:
    def __init__(self, state, parent, depth):
        self.state = state
        self.parent = parent
        self.children = []
        self.depth = depth
        if parent is None:
            self.ancestors = set()
        else:
            self.ancestors = parent.ancestors.copy()
            self.ancestors.add(parent.state)
        global NODES_CREATED
        NODES_CREATED += 1


def make_move(str, dir, index):
    ind = index
    char = str[dir]
    string1 = str.replace(char, BLANK)
    string2 = string1[:index] + char + string1[index + 1:]

    return string2


def swap(i, j, str, changeI, changeJ):
    char = get_ij(str, changeI, changeJ)  # character in place you want to move 0 to
    string1 = set_ij(str, changeI, changeJ, "BLANK")  # put 0 in above char's place
    string2 = set_ij(string1, i, j, char)  # put char in 0's old place
    return string2


def goal_test(str):
    return str == GOAL_STATE


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
    # print(i)
    print("Puzzle: " + path2[0])
    print("LENGTH = " + str(len(path2)))
    return path2

def path_no_print(node):
    path = []
    curr = node
    path.append(curr.state)

    while curr.parent:
        path.append(curr.parent.state)
        curr = curr.parent

    path2 = path[::-1]
    # for i in path2:
    # print(i)

    return path2

def n2ij(index):
    return index // 4, index % 4

def BFS(root):
    queue = collections.deque()
    queue.append(root)
    visited = set()
    while queue:
        child = queue.popleft()
        if (goal_test(child.state)):
            #ath(child)
            return child
        index = child.state.index(BLANK)
        depth = child.depth + 1
        dict = DICTIONARY
        for i in dict[index]:
            grandkidstate = make_move(child.state, i, index)
            if grandkidstate not in visited:
                grandkid = Node(make_move(child.state, i, index), child, depth)
                queue.append(grandkid)
                visited.add(grandkidstate)
    return none

def h(s, d):
    total = 0
    length = len(GOAL_INDEXES)
    for i in range(length):
        goalindex = GOAL_INDEXES[s[i]]
        total += abs((goalindex//4) - (i//4)) + abs((goalindex%4) - (i%4))
    return total + d + random.random()


def greedy(root):
    queue = []
    heapq.heappush(queue, (h(root.state, 0), root))
    visited = set()
    while queue:
        popped = heapq.heappop(queue)
        child = popped[1]
        if (goal_test(child.state)):
            #path(child)
            return child

        index = child.state.index(BLANK)
        dict = DICTIONARY
        depth = child.depth + 1

        for i in dict[index]:
            grandkidstate = (make_move(child.state, i, index))
            if grandkidstate not in visited:
                grandkid = Node(grandkidstate, child, depth)
                heapq.heappush(queue, (h(grandkidstate, depth), grandkid))
                visited.add(grandkidstate)

    return None

def DFS(root):
    visited = set()
    stack = collections.deque()
    stack.append(root)
    while stack:
        parent = stack.pop()
        visited.add(parent.state)
        if (goal_test(parent.state)):
            #path(parent)
            return parent
        index = parent.state.index(BLANK)
        dict = DICTIONARY
        depth = parent.depth + 1
        for i in dict[index]:
            grandkidstate = (make_move(parent.state, i, index))
            if grandkidstate not in visited:
                grandkid = Node(grandkidstate, parent, depth)
                stack.append(grandkid)

    return None

def K_DFS(root, level):
    stack = collections.deque()
    stack.append(root)
    node_depth = 0
    while node_depth <= level and stack:
        parent = stack.pop()
        node_depth = parent.depth + 1
        if (goal_test(parent.state)):
            #path(parent)
            return parent
        index = parent.state.index(BLANK)
        dict = DICTIONARY
        if (node_depth < level):
            for i in dict[index]:
                childstate = make_move(parent.state, i, index)
                if childstate not in parent.ancestors:
                    child = Node(childstate, parent, node_depth)
                    stack.append(child)
    return None

        #if not stack or node_depth > level:
         #   print("Impossible to solve.")

def ID_DFS(root, level):
    global NODES_CREATED
    for i in range(1, level):
        NODES_CREATED = 0
        sol = K_DFS(root, i)
        if sol:
            return sol

def BD_BFS(root):
    goal_node = Node(GOAL_STATE, None, 0)
    visited_root = set() #set of strings
    dict_root = {} #maps strings to nodes
    visited_goal = set()
    dict_goal = {}
    queue_root = collections.deque()
    queue_root.append(root)
    queue_goal = collections.deque()
    queue_goal.append(goal_node)

    visited_goal.add(GOAL_STATE)
    dict_goal[GOAL_STATE] = goal_node
    visited_root.add(root.state)
    dict_root[root.state] = root

    while queue_root and queue_goal:
        parent_root = queue_root.popleft()
        parent_goal = queue_goal.popleft()

        depth = parent_root.depth + 1

        index_root = parent_root.state.index(BLANK)
        index_goal = parent_goal.state.index(BLANK)

        dict = DICTIONARY
        for i in dict[index_goal]:
            child_goal_state = make_move(parent_goal.state, i, index_goal)
            if child_goal_state not in visited_goal:
                child_goal = Node(child_goal_state, parent_goal, depth)
                if child_goal_state in visited_root:
                    return child_goal, dict_root[child_goal_state]
                    #length = len(child_goal.ancestors) + len(dict_root[child_goal_state].ancestors)
                    #print("Puzzle: " + str(root.state))
                    #print("Length: " + str(length))
                    #return
                queue_goal.append(child_goal)
                visited_goal.add(child_goal_state)
                dict_goal[child_goal_state] = child_goal

        for i in dict[index_root]:
            child_root_state = make_move(parent_root.state, i, index_root)
            if child_root_state not in visited_root:
                child_root = Node(child_root_state, parent_root, depth)
                if child_root_state in visited_goal:
                    return child_root, dict_goal[child_root_state]
                    #length = len(child_root.ancestors) + len(dict_goal[child_root_state].ancestors)
                    #print("Puzzle: " + str(root.state))
                    #print("Length: " + str(length))
                    #eturn
                queue_root.append(child_root)
                visited_root.add(child_root_state)
                dict_root[child_root_state] = child_root

    return None


def testString():
    dict = DICTIONARY
    temp = GOAL_STATE
    for i in range(0, 5):
        index = temp.index(BLANK)
        temp = make_move(temp, random.choice(dict[index]), index)

    return temp

def test_method(f, args, verbose = 1):
    global NODES_CREATED
    NODES_CREATED = 0

    tic = time()
    sol = f(*args)
    toc = time()

    if verbose == 1:
        print("\n------Testing %s ------- \n" % f.__name__)
        if sol is not None:
            print("Solution Found")
            print("Node count: %i" % NODES_CREATED)
            print("Length: %i steps, Time: %5.4f" % (sol.depth, toc-tic))
            path(sol) #wont work for BD_BFS
        else:
            print("Unsolvable")

    elif verbose == 0:
        if f is BD_BFS:
            depth = sol[0].depth + sol[1].depth
        else:
            depth = sol.depth
        if sol is not None:
            print("Solved. %10s %8i Nodes\t %4i Steps\t %5.5f secs\t %6.0f N/s" % (f.__name__, NODES_CREATED, depth, toc-tic,NODES_CREATED / (toc-tic)))
        else:
            print("Unsolv. %10s %8i Nodes\t %4i Steps\t %5.5f secs\t %6.0f N/s" % (f.__name__, NODES_CREATED, 0, toc-tic, NODES_CREATED / (toc-tic)))


if __name__ == "__main__":
    string = testString()
    f = open("testcases.txt", 'r')
    l = f.read().splitlines()
    #string = testString()

    for i in l:
        curr = i
        root = Node(i, None, 0)
        print("\n---->Solving ", root.state)
        test_method(BFS, (root,), 0)
        test_method(BD_BFS, (root,), 0)
        # test_method(K_DFS, (root, 22), 0)
        test_method(ID_DFS, (root, 23), 0)
        test_method(greedy, (root,), 0)

