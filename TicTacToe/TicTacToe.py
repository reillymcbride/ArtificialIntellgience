#Reilly McBride
#13 December 2017

import collections

class Node:
    def __init__(self, current_state):
        self.state = current_state
        self.score = -2
        self.children = []

def score(value):
    if value == 'X':
        return 1
    if value == 'O':
        return -1

def goal_test_with_score(game):
    board = game.state
    center = board[4]
    if center != '.':
        if board[0] == center and board[8] == center:
            #print(str(center) + "won!!")
            return score(center)
        if board[2] == center and board[6] == center:
            #print(str(center) + "won!!")
            return score(center)

    for i in range(3):
        col_head = board[i]
        if col_head != '.':
            if board[i + 3] == col_head and board[i + 6] == col_head:
                #print(str(col_head) + "won!!")
                return score(col_head)
    for i in (0,3,6):
        row_head = board[i]
        if row_head != '.':
            if board[i + 1] == row_head and board[i + 2] == row_head:
                #print(str(row_head) + "won!!")
                return score(row_head)

    if '.' not in board:
        #print("Tie!")
        return 0

    return None

def get_next_player(player):
    if player == 'X':
        return 'O'
    if player == 'O':
        return 'X'

def find_valid_moves(state):
    indices = set()
    board = state[0]
    for i in range(len(board)):
        if board[i] == '.':
            indices.add(i)
    return indices

def make_move(state, square):
    board = state[0]
    player = state[1]
    if square < 8:
        # board[:square] + player + board[square+1:]
        new_state = board[0:square] + player + board[(square + 1):len(board)]
    elif square == 8:
        new_state = board[0:square] + player
    return [new_state, player]

def display(board):
    print(board[:3])
    print(board[3:6])
    print(board[6:])

def gen_children(state, player):
    list = []
    for i in range(9):
        if state[i] == '.':
            temp = state[0:i] + player + state[i+1:]
            list.append(Node(temp))
    return list

def minimax(node, player):
    sc = goal_test_with_score(node)
    if sc != None:
        node.score = sc
        return node
    node.children = gen_children(node.state, player)
    if player == 'X':
        for c in node.children:
            c.score = minimax(c, 'O').score
        temp = max(node.children, key = lambda x: x.score)
        return temp
    if player == 'O':
        for c in node.children:
            c.score = minimax(c, 'X').score
        temp = min(node.children, key = lambda x: x.score)
        return temp

def interpret_score(score):
    if score == 1:
        print("X won!")
    if score == -1:
        print("O won!")
    if score == 0:
        print("Tie!")

def play_game(start):
    board = Node(start)
    while goal_test_with_score(board) == None:
        human_move = int(input("Your turn! Where do you want to place an O? Enter an integer 0-8"))
        board.state = board.state[0:human_move] + 'O' + board.state[human_move + 1:]
        display(board.state)
        print()
        print("My turn!")
        board.state = (minimax(board, 'X')).state
        display(board.state)
        print()
    print()
    sc = goal_test_with_score(board)
    interpret_score(sc)

def solve(state):
    final_boards = set()
    games = []
    fringe = collections.deque()
    fringe.appendleft(state)
    while fringe:
        thing = fringe.popleft()
        if goal_test_with_score(thing[0]) != None:
            display(thing[0])
            final_boards.add(thing[0])
            games.append(thing[0])
            continue
            #return thing
        children = find_valid_moves(thing)
        for index in children:
            new_state = make_move(thing, index)
            fringe.appendleft(new_state)
            new_state[1] = get_next_player(new_state[1])

    print("Final Boards: " + str(len(final_boards)))
    print("Games: " + str(len(games)))

if __name__ == "__main__":
    initial = '.........'
    #player = 'X'
    #solve([initial, player])
    print("Let's play tic tac toe! You're O, and go first!")
    print("Here's how the board is set up: ")
    display("012345678")
    play_game(initial)
