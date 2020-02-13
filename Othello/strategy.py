#Reilly McBride 1/10/17

import random
import numpy as np
import math

#### Othello Shell
#### P. White 2016-2018


EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'

# To refer to neighbor squares we can add a direction to a square.
#N, S, E, W = -10, 10, 1, -1
#NE, SE, NW, SW = N + E, S + E, N + W, S + W
#DIRECTIONS = (N, NE, E, SE, S, SW, W, NW)
DIRECTIONS = {'N':-10, 'S':10, 'E':1, 'W':-1, 'NE':-9, 'SE':11, 'NW':-11, 'SW':9}

PLAYERS = {BLACK: "Black", WHITE: "White"}

HistoryTable = {}
for i in range(11, 89):
    if i != OUTER:
       HistoryTable[i] = 0


########## ########## ########## ########## ########## ##########
# The strategy class for your AI
# You must implement this class
# and the method best_strategy
# Do not tamper with the init method's parameters, or best_strategy's parameters
# But you can change anything inside this you want otherwise
#############################################################

class Node():
    def __init__(self, state):
        self.state = state
        self.score = -100
        self.move = 100
        self.valid_moves = -1
    def __lt__(self, other):
        return self.score < other.score

class Strategy():
    def __init__(self):
        pass

    def get_starting_board(self):
        """Create a new board with the initial black and white positions filled."""
        return('???????????........??........??........??...o@...??...@o...??........??........??........???????????')

    def get_pretty_board(self, board):
        """Get a string representation of the board."""
        edge_count = 0
        str = ""
        for i in range(11, 89):
            if board[i] == '?':
                edge_count += 1
            if edge_count == 2:
                str += "\n"
                edge_count = 0
            if board[i] != '?':
                str += board[i] + " "
        return str

    def opponent(self, player):
        """Get player's opponent."""
        if player == WHITE:
            return BLACK
        if player == BLACK:
            return WHITE

    def find_match(self, board, player, square, direction):
        """
        Find a square that forms a match with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        """
        opponent = self.opponent(player)
        ind = square + direction
        square_value = board[ind]
        if board[ind] is not opponent:
            return None
        while (square_value == opponent):
            ind = ind + direction
            square_value = board[ind]
        if square_value == player:
            return ind
        else:
            return None

    def is_move_valid(self, board, player, move):
        """Is this a legal move for the player?"""
        return move in self.get_valid_moves(board, player)

    def flip_squares(self, board, player, start_square, end_square, direction):
        board = board[:start_square] + player + board[start_square + 1:]
        ind = start_square + direction
        square_value = board[ind]
        opponent = self.opponent(player)
        while (square_value == opponent):
            board = board[:ind] + player + board[ind + 1:]
            ind = ind + direction
            square_value = board[ind]

        return board

    def make_move(self, board, player, move):
        """Update the board to reflect the move by the specified player."""
        # returns a new board/string
        new_board = board
        for key in DIRECTIONS.keys():
            end_square = self.find_match(new_board, player, move, DIRECTIONS[key])
            if end_square != None:
                new_board = self.flip_squares(new_board, player, move, end_square, DIRECTIONS[key])
        return new_board

    def get_valid_moves(self, board, player):
        """Get a list of all legal moves for player."""
        valid_moves = []
        for i in range(11, 89):  # can change later if looping over question marks negatively impacts
            if board[i] is EMPTY:
                for key in DIRECTIONS.keys():
                    if self.find_match(board, player, i, DIRECTIONS[key]) != None:
                        valid_moves.append(i)
                        break
        #print(valid_moves)
        return valid_moves

    def has_any_valid_moves(self, board, player):
        """Can player make any moves?"""
        return len(self.get_valid_moves(board, player)) != 0

    def next_player(self, board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        player = None
        if prev_player == BLACK:
            player = WHITE
            if len(self.get_valid_moves(board, player)) == 0:
                player = prev_player
        if prev_player == WHITE:
            player = BLACK
            if len(self.get_valid_moves(board, player)) == 0:
                player = prev_player
        if len(self.get_valid_moves(board, player)) == 0:
            return None
        return player

    def score(self, board, player=BLACK):
        """Compute player's score (number of player's pieces minus opponent's)."""
        b = 0
        w = 0
        for i in range(11, 89):
            if board[i] == BLACK:
                b += 1
            if board[i] == WHITE:
                w += 1
        return b - w


    def convert_to_int(self, board):
        new_board = []
        for i in range(100):
            if board[i] == ".":
                new_board.append(0)
            if board[i] == "o":
                new_board.append(-1)
            if board[i] == "@":
                new_board.append(1)
            if board[i] == '?':
                new_board.append(0)
        #print(new_board)
        return new_board

    def better_score(self, board, player = BLACK):
        matrix_state = self.convert_to_int(board)
        weight_matrix = [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 120, 20, 20, 5, 5, 20, 20, 120, 0,
                0, 20, -40, -5, -5, -5, -5, -40, 20, 0,
                0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
                0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
                0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
                0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
                0, 20, -40, -5, -5, -5, -5, -40, 20, 0,
                0, 120, 20, 20, 5, 5, 20, 20, 120, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ]
        scored = np.dot(matrix_state, weight_matrix)
        #print(scored)
        score = np.sum(scored)
        #print(score)
        return score

    def game_over(self, board, player):
        """Return true if player and opponent have no valid moves"""
        return self.next_player(board, player) == None

    ### Monitoring players

    class IllegalMoveError(Exception):
        def __init__(self, player, move, board):
            self.player = player
            self.move = move
            self.board = board

        def __str__(self):
            return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

    ################ strategies #################

    def minmax_search(self, node, player, depth):
        # determine best move for player recursively
        # it may return a move, or a search node, depending on your design
        # feel free to adjust the parameters
        best = {BLACK: max, WHITE: min}
        board = node.state
        if depth == 0:
            node.score = self.better_score(board)
            return node
        moves = self.get_valid_moves(board, player)
        children = []
        for move in moves:
            new_board = self.make_move(board, player, move)
            new_player = self.next_player(new_board, player)
            if new_player == None:
                child = Node(new_board)
                child.move = move
                child.score = 1000 * self.score(new_board)
                children.append(child)
            else:
                child = Node(new_board)
                child.move = move
                child.score = self.minmax_search(child, new_player, depth = depth - 1).score
                children.append(child)
        winner = best[player](children)
        node.score = winner.score
        return winner

    def minmax_strategy(self, board, player, depth=3):
        # calls minmax_search
        # feel free to adjust the parameters
        # returns an integer move
        node_result = self.minmax_search(Node(board), player, depth)
        return node_result.move

    def alphabeta(self, node, player, depth, alpha, beta):
        global HistoryTable
        best = {BLACK: max, WHITE: min}
        mult = {BLACK: 1, WHITE: -1}
        board = node.state
        if depth == 0:
            node.score = self.better_score(board)
            return node
        moves = self.get_valid_moves(board, player)
        #print(moves)
        moves = sorted(moves, key = lambda x: HistoryTable[x])
        #sprint(moves)
        children = []
        for move in moves:
            new_board = self.make_move(board, player, move)
            new_player = self.next_player(new_board, player)
            child = Node(new_board)
            if new_player == None:
                child.valid_moves = moves
                child.move = move
                child.score = 10000000000 * self.score(new_board)
                children.append(child)
            else:
                child.valid_moves = moves
                child.move = move
                temp = self.alphabeta(child, new_player, depth - 1, alpha, beta)
                child.score = temp.score - (mult[player] * len(temp.valid_moves)) + random.random()
                children.append(child)
            if player == BLACK:
                alpha = max(alpha, child.score)
            if player == WHITE:
                beta = min(beta, child.score)
            if alpha >= beta:
                #HistoryTable[child.move] = HistoryTable[child.move] + 2 ** depth
                break

        winner = best[player](children)
        best_move = winner.move
        HistoryTable[best_move] = HistoryTable[best_move] + 2**depth
        node.score = winner.score
        return winner

    def alphabeta_strategy(self, board, player, depth=5):
        beta = float("inf")
        alpha = -beta
        node_result = self.alphabeta(Node(board), player, depth, alpha, beta)
        return node_result.move

    def random_strategy(self, board, player):
        return random.choice(self.get_valid_moves(board, player))

    def best_strategy(self, board, player, best_move, still_running):
        ## THIS IS the public function you must implement
        ## Run your best search in a loop and update best_move.value
        board = ''.join(board)
        depth = 1
        while (True):
            ## doing random in a loop is pointless but it's just an example
            best_move.value = self.minmax_strategy(board, player, depth)
            depth += 1

    standard_strategy = minmax_strategy


###############################################
# The main game-playing code
# You can probably run this without modification
################################################
import time
from multiprocessing import Value, Process
import os, signal

silent = False


#################################################
# StandardPlayer runs a single game
# it calls Strategy.standard_strategy(board, player)
#################################################
class StandardPlayer():
    def __init__(self):
        pass

    def play(self):
        ### create 2 opponent objects and one referee to play the game
        ### these could all be from separate files
        ref = Strategy()
        black = Strategy()
        white = Strategy()

        print("Playing Standard Game")
        board = ref.get_starting_board()
        player = BLACK
        strategy = {BLACK: black.alphabeta_strategy, WHITE: white.alphabeta_strategy}
        print(ref.get_pretty_board(board))

        while player is not None:
            move = strategy[player](board, player)
            print("Player %s chooses %i" % (player, move))
            board = ref.make_move(board, player, move)
            print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board) > 0 else "White"))


#################################################
# ParallelPlayer simulated tournament play
# With parallel processes and time limits
# this may not work on Windows, because, Windows is lame
# This calls Strategy.best_strategy(board, player, best_shared, running)
##################################################
class ParallelPlayer():
    def __init__(self, time_limit=5):
        self.black = Strategy()
        self.white = Strategy()
        self.time_limit = time_limit

    def play(self):
        ref = Strategy()
        print("play")
        board = ref.get_starting_board()
        player = BLACK

        print("Playing Parallel Game")
        strategy = lambda who: self.black.best_strategy if who == BLACK else self.white.best_strategy
        while player is not None:
            best_shared = Value("i", -99)
            best_shared.value = -99
            running = Value("i", 1)

            p = Process(target=strategy(player), args=(board, player, best_shared, running))
            # start the subprocess
            t1 = time.time()
            p.start()
            # run the subprocess for time_limit
            p.join(self.time_limit)
            # warn that we're about to stop and wait
            running.value = 0
            time.sleep(0.01)
            # kill the process
            p.terminate()
            time.sleep(0.01)
            # really REALLY kill the process
            if p.is_alive(): os.kill(p.pid, signal.SIGKILL)
            # see the best move it found
            move = best_shared.value
            if not silent: print("move = %i , time = %4.2f" % (move, time.time() - t1))
            if not silent: print(board, ref.get_valid_moves(board, player))
            # make the move
            board = ref.make_move(board, player, move)
            if not silent: print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board) > 0 else "White"))


if __name__ == "__main__":
    #game =  ParallelPlayer(2)
    game = StandardPlayer()
    game.play()