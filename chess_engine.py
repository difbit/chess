#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import pprint
import time
import sys
from itertools import chain
import itertools
import pickle

tic = time.process_time()

CHECKLIST_ONE = [24, 35, 108, 119]
CHECKLIST_TWO = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                 36, 48, 60, 72, 84, 96, 109, 110, 111, 112,
                 113, 114, 115, 116, 117, 118, 95, 83, 71, 59,
                 47]

"""Use these two boards to play around"""

# The board representation
posiii = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,                  # 0-11
    0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0,                  # 12-23
    0, 0, 'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r', 0, 0,  # 24-35     # 26-33
    0, 0, 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 0, 0,  # 36-47     # 38-45
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  # 48-59     # 50-57
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  # 60-71     # 62-69
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  # 72-83     # 74-81
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  # 84-95     # 86-93
    0, 0, 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 0, 0,  # 96-107    # 98-105
    0, 0, 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R', 0, 0,  # 108-119   # 110-117
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,                  # 120-131
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0                   # 132-143
    ]

# The board for testing moves and functions of different pieces
posi = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,                  # 0-11
    0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0,                  # 12-23
    0, 0, 'r', '-', '-', '-', 'k', '-', '-', 'r', 0, 0,  # 24-35     # 26-33
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  # 36-47     # 38-45
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  # 48-59     # 50-57
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  # 60-71     # 62-69
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  # 72-83     # 74-81
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  # 84-95     # 86-93
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  # 96-107    # 98-105
    0, 0, 'R', '-', 'B', '-', 'K', '-', '-', 'R', 0, 0,  # 108-119   # 110-117
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,                  # 120-131
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0                   # 132-143
    ]

player_posi_white = {
    'a8': 26, 'b8': 27, 'c8': 28, 'd8': 29, 'e8': 30, 'f8': 31, 'g8': 32, 'h8': 33,
    'a7': 38, 'b7': 39, 'c7': 40, 'd7': 41, 'e7': 42, 'f7': 43, 'g7': 44, 'h7': 45,
    'a6': 50, 'b6': 51, 'c6': 52, 'd6': 53, 'e6': 54, 'f6': 55, 'g6': 56, 'h6': 57,
    'a5': 62, 'b5': 63, 'c5': 64, 'd5': 65, 'e5': 66, 'f5': 67, 'g5': 68, 'h5': 69,
    'a4': 74, 'b4': 75, 'c4': 76, 'd4': 77, 'e4': 78, 'f4': 79, 'g4': 80, 'h4': 81,
    'a3': 86, 'b3': 87, 'c3': 88, 'd3': 89, 'e3': 90, 'f3': 91, 'g3': 92, 'h3': 93,
    'a2': 98, 'b2': 99, 'c2': 100, 'd2': 101, 'e2': 102, 'f2': 103, 'g2': 104, 'h2': 105,
    'a1': 110, 'b1': 111, 'c1': 112, 'd1': 113, 'e1': 114, 'f1': 115, 'g1': 116, 'h1': 117,
}

player_posi_black = {
    'h1': 26, 'g1': 27, 'f1': 28, 'e1': 29, 'd1': 30, 'c1': 31, 'b1': 32, 'a1': 33,
    'h2': 38, 'g2': 39, 'f2': 40, 'e2': 41, 'd2': 42, 'c2': 43, 'b2': 44, 'a2': 45,
    'h3': 50, 'g3': 51, 'f3': 52, 'e3': 53, 'd3': 54, 'c3': 55, 'b3': 56, 'a3': 57,
    'h4': 62, 'g4': 63, 'f4': 64, 'e4': 65, 'd4': 66, 'c4': 67, 'b4': 68, 'a4': 69,
    'h5': 74, 'g5': 75, 'f5': 76, 'e5': 77, 'd5': 78, 'c5': 79, 'b5': 80, 'a5': 81,
    'h6': 86, 'g6': 87, 'f6': 88, 'e6': 89, 'd6': 90, 'c6': 91, 'b6': 92, 'a6': 93,
    'h7': 98, 'g7': 99, 'f7': 100, 'e7': 101, 'd7': 102, 'c7': 103, 'b7': 104, 'a7': 105,
    'h8': 110, 'g8': 111, 'f8': 112, 'e8': 113, 'd8': 114, 'c8': 115, 'b8': 116, 'a8': 117,
}

# Used for printing the board
def board_list_view(list):
    view = [list[i:i + 12] for i in range(0, 11, 12)]
    o = '\n'.join(map(str, view))
    view_2 = [list[i:i + 12] for i in range(12, 23, 12)]
    o_2 = '\n'.join(map(str, view_2))
    view_3 = [list[i:i + 12] for i in range(24, 117, 12)]
    o_3 = '\n'.join(map(str, view_3))
    view_4 = [list[i:i + 12] for i in range(120, 131, 12)]
    o_4 = '\n'.join(map(str, view_4))
    view_5 = [list[i:i + 12] for i in range(132, 143, 12)]
    o_5 = '\n'.join(map(str, view_5))
    good_board = '\t%s\n\t%s\n%s\n\t%s\n\t%s\n' % (o, o_2, o_3, o_4, o_5)
    return good_board


def board_view(list):
    view_string = ''
    for col in range(1, 13):
        view = [list[i:i + 12] for i in range(12 * (col - 1), (col * 12) - 1, 12)]
        view_string += '%s%s' % ('\n\t', ' '.join(str(v) for v in view[0]))
    result = view_string.replace('0', '|')
    return result


# Illegal positions for pieces
ZEROS = [i for i, x in enumerate(posi) if x == 0]

X, Y = 1, 12
moves = {
    "rook": [X, Y, -X, -Y],
    "knight": [Y+Y-X, Y+Y+X, X+X+Y, X+X-Y, -Y-Y+X, -Y-Y-X, -X-X-Y, -X-X+Y],
    "bishop": [X+Y, X-Y, -X+Y, -X-Y],
    "queen": [X, Y, -X, -Y, X+Y, X-Y, -X+Y, -X-Y],
    "king": [X, Y, -X, -Y, X+Y, X-Y, -X+Y, -X-Y, -X-X, X+X],  # Last two moves are for castling
    "pawn": [-Y, -Y-Y, -Y+X, -Y-X]
}


# The function for rotating the board; used when a move is made
# and it is other player's move.
# This now works like a mirror.
def rotate(BOARD):
    for SQUARE in range(0, 8):
        BOARD[26+SQUARE], BOARD[110+SQUARE] \
            = BOARD[110+SQUARE], BOARD[26+SQUARE]
    for SQUARE in range(0, 8):
        BOARD[38+SQUARE], BOARD[98+SQUARE] \
            = BOARD[98+SQUARE], BOARD[38+SQUARE]
    for SQUARE in range(0, 8):
        BOARD[50+SQUARE], BOARD[86+SQUARE] \
            = BOARD[86+SQUARE], BOARD[50+SQUARE]
    for SQUARE in range(0, 8):
        BOARD[62+SQUARE], BOARD[74+SQUARE] \
            = BOARD[74+SQUARE], BOARD[62+SQUARE]
    return BOARD


def first_rotation(BOARD):
    for SQUARE in range(0, 8):
        BOARD[26 + SQUARE], BOARD[117 - SQUARE] \
            = BOARD[117 - SQUARE], BOARD[26 + SQUARE]
    for SQUARE in range(0, 8):
        BOARD[38 + SQUARE], BOARD[105 - SQUARE] \
            = BOARD[105 - SQUARE], BOARD[38 + SQUARE]
    for SQUARE in range(0, 8):
        BOARD[50 + SQUARE], BOARD[93 - SQUARE] \
            = BOARD[93 - SQUARE], BOARD[50 + SQUARE]
    for SQUARE in range(0, 8):
        BOARD[62 + SQUARE], BOARD[81 - SQUARE] \
            = BOARD[81 - SQUARE], BOARD[62 + SQUARE]
    return BOARD


def rotate_move_list(move_list):
    for move in range(0, 8):
        move_list[move], move_list[64 - move] \
            = move_list[64 - move], move_list[move]
    for move in range(0, 8):
        move_list[38 + move], move_list[105 - move] \
            = move_list[105 - move], move_list[38 + move]
    for move in range(0, 8):
        move_list[50 + move], move_list[93 - move] \
            = move_list[93 - move], move_list[50 + move]
    for move in range(0, 8):
        move_list[62 + move], move_list[81 - move] \
            = move_list[81 - move], move_list[62 + move]
    return move_list



_pieces = {
    "king": 'K', "rook": 'R', "pawn": 'P',
    "knight": 'N', "queen": 'Q', "bishop": 'B'
    }


def lower_case(d):
    new = dict((k.lower(), v.lower()) for k,v in d.items())
    return new


def upper_case(d):
    new = dict((k, v.upper()) for k,v in d.items())
    return new


def upper_keys(d):
    new = dict((k.upper(), v) for k,v in d.items())
    return new


# Maybe will be used later
def low(d):
    new = dict((k.lower(), v) for k,v in d.items())
    return new


def save_list(target_list):
    with open('target_list', 'wb') as f:
        pickle.dump(target_list, f)


def open_list(target_list):
    with open('target_list', 'rb') as f:
        target_list = pickle.load(f)


class Evaluate(object):

    def __init__(self, position):
        self.position = position

    def evaluation_function(self):
        piece_values = {
            'B': 310, 'N': 300, 'P': 100, 'R': 500, 'Q': 900, 'K': 10000
        }

        sum = 0
        sum_1 = 0

        value_list = []

        for i in piece_values.keys():
            value_list.append(self.position.count(i)*piece_values[i])

        for i in value_list:
            sum += i

        del value_list [:]

        piece_values = low(piece_values)

        for i in piece_values.keys():
            value_list.append(self.position.count(i)*piece_values[i])

        for i in value_list:
            sum_1 += i
        black_pieces = False

        return sum - sum_1

    class board_object(object):

        def __init__(self, posi):
            self.posi = posi
            self.posi = list(self.posi)


def evaluation_function(positions):
    piece_values = {
        'B': 310, 'N': 300, 'P': 100, 'R': 500, 'Q': 900, 'K': 10000
    }

    for position in positions:
        sum = 0
        sum_1 = 0

        value_list = []

        for piece in piece_values.keys():
            value_list.append(position.count(piece)*piece_values[piece])

        for i in value_list:
            sum += i

        del value_list [:]

        piece_values = low(piece_values)

        for i in piece_values.keys():
            value_list.append(self.position.count(i)*piece_values[i])

        for i in value_list:
            sum_1 += i
        black_pieces = False

    return sum - sum_1




# This will be used for the evaluation function
def chess_engine():

    BOARD_LIST = []
    EVALUATIONS = []

    depth = 0
    #first_save = True
    #eval_1 = Evaluate(posi, False, 0, 0)
    BOARD_LIST.append(board_object(posi))
    EVALUATIONS.append(Evaluate(posi).evaluation_function())

    LIMIT = 50

    while depth < LIMIT:
        a_game.move_gen(posi)
        #print(board_view(posi))
        #if first_save:
        #    this_board = board_object(posi)
            #BOARD_LIST[1] = board_object(posi)
        BOARD_LIST.append(board_object(posi))
            #with open('posi', 'wb') as f:
            #    pickle.dump(posi, f)
        #eval_1.evaluation_function()
        EVALUATIONS.append(Evaluate(posi).evaluation_function())
        #    first_save = False
        #else:
        #    pass
        a_game.white_to_move = False
        rotate(posi)
        a_game.move_gen(posi)
        a_game.white_to_move = True
        rotate(posi)
        BOARD_LIST.append(board_object(posi))
        EVALUATIONS.append(Evaluate(posi).evaluation_function())
        depth += 1

    for i in range(0, LIMIT):
        print(EVALUATIONS[i])
    print(board_view(BOARD_LIST[LIMIT].posi))
    #Boards could be keys and evaluations values in dictionary


def capture_piece():
    if kings.check:
        PIECE = kings.piece


king_rook_move = {'K': {'ROOK_Q': False, 'ROOK_K': False, 'KING': False},
                  'k': {'ROOK_Q': False, 'ROOK_K': False, 'KING': False}}


def empty_squares(lst):
    for item in lst:
        if item != '-':
            return False
    return True


def get_piece_moves(posi, white_to_move, _pieces):
    """ The main function to search moves. Note that
     the position is always rotated before checking the
     available moves. """

    if white_to_move:
        _pieces = upper_case(_pieces)
    else:
        _pieces = lower_case(_pieces)

    positions = []
    OWN_PIECES = []

    for piece in _pieces:
        orig_posi = list(posi)
        OWN_PIECES = [i for i, x in enumerate(orig_posi)
                      if x == _pieces[piece]]
        mod_posi = list(orig_posi)
        if OWN_PIECES != []:
            for enum_piece in OWN_PIECES:
                # Count more moves for ranged pieces
                if _pieces[piece] in ['R', 'Q', 'B', 'r', 'q', 'b']:
                    rang = 8
                else:
                    rang = 2
                for move in moves[piece]:
                    # Check where king and rooks are
                    if (_pieces[piece] in ['K', 'k']) and \
                            (move in moves[piece][-2:]):

                        # Left some prints for testing
                        #print("MOD POSI R", not mod_posi[117] in ['R', 'r'])
                        #print("MOD ANY", any(x != '-' for x in mod_posi[115:117]))
                        #print("KING ROOK MOVE rook r", king_rook_move.get(_pieces[piece])['ROOK_K'])
                        #print("KING ROOK MOVE king", king_rook_move.get(_pieces[piece])['KING'])
                        #print("moved piece", moves[piece])
                        #print("moved", move)

                        if move == 2:
                            if (not mod_posi[117] in ['R', 'r']) or \
                                    (any(x != '-' for x in mod_posi[115:117])) or \
                                    ((king_rook_move.get(_pieces[piece])['ROOK_K']) or
                                        (king_rook_move.get(_pieces[piece])['KING'])):
                                continue
                        if move == -2:
                            if (mod_posi[110] not in ['R', 'r']) or \
                                    (any(x != '-' for x in mod_posi[111:114])) or \
                                    ((king_rook_move.get(_pieces[piece])['ROOK_Q']) or
                                        (king_rook_move.get(_pieces[piece])['KING'])):
                                continue

                    # This checks if a pawn is on its original square
                    if (_pieces[piece] in ['P', 'p']) and \
                            (moves[piece][1] == move) and \
                            (enum_piece not in range(98,106)):
                        continue
                    ate_piece = False

                    if _pieces[piece] in ['K', 'k']:
                        if move == moves[piece][-2]:
                            mod_posi[110], mod_posi[113] = \
                                    mod_posi[113], mod_posi[110]

                        if move == moves[piece][-1]:
                            mod_posi[117], mod_posi[115] = \
                                    mod_posi[115], mod_posi[117]

                    for go in range(1, rang):
                        if mod_posi[enum_piece + move * go] in \
                                (ZEROS + list(_pieces.values())):
                            break
                        elif mod_posi[enum_piece + move * go] != '-':
                            ate_piece = True
                            original_square = '-'
                        else:
                            original_square = mod_posi[enum_piece + move * go]
                            # Check if pawn's move is in the first two
                            # items in the list
                            if _pieces[piece] in ['P', 'p'] and \
                                    (move not in moves[piece][:2]):
                                continue
                        if _pieces[piece] in ['P', 'p'] and \
                                ((enum_piece + move * go) in range(26, 34)):
                            if _pieces[piece].isupper():
                                mod_posi[enum_piece] = 'Q'
                            else: mod_posi[enum_piece] = 'q'

                        mod_posi[enum_piece], mod_posi[enum_piece + move * go]\
                                = original_square, mod_posi[enum_piece]

                        positions.append(mod_posi)
                        mod_posi = list(orig_posi)
                        if ate_piece:
                            break
    return positions, posi


def bool_negation(bool):
    return not bool


def search_checks(orig_fetched_moves, white_to_move, player):
    white_to_move = bool_negation(white_to_move)
    remove_these = []
    for posit in orig_fetched_moves[0]:
        # white to move is set to false
        if player != 'black':
            rotate(posit)
        fetched_moves = get_piece_moves(posit, white_to_move, _pieces)

        # Search boards if one king is missing
        for board in fetched_moves[0]:
            kings = [i for i, x in enumerate(board) if x in ['K', 'k']]
            if len(kings) < 2:
                remove_these.append(posit)
                break
        if player != 'black':
            rotate(posit)
    for rem in remove_these:
        orig_fetched_moves[0].remove(rotate(rem))
    white_to_move = bool_negation(white_to_move)
    return orig_fetched_moves, white_to_move


def play_move(position, searched_moves, player):
    if player == "black":
        player_posi = player_posi_black
    else:
        player_posi = player_posi_white

    while True:
        print("Write 'q' to exit the program.")
        pos = list(position)
        print("Select a piece from: \n%s" % sorted(player_posi.keys()))
        start = input()

        if str(start) == 'q':
            sys.exit()

        if start not in player_posi.keys():
            print("Invalid initial square.")
            continue

        print("Select a destination square from: \n%s" % sorted(player_posi.keys()))
        dest = input()

        if dest not in player_posi.keys():
            print("Invalid destination square.")
            continue

        start_posi = player_posi[start]
        dest_posi = player_posi[dest]
        if pos[dest_posi] != '-':
            square = '-'
        else:
            square = pos[dest_posi]

        # Just adds castling to board positions. The legality of the move is
        # checked later.
        if start == 'e1' and dest == 'c1':
            pos[110], pos[113] = pos[113], pos[110]

        if start == 'e1' and dest == 'g1':
            pos[115], pos[117] = pos[117], pos[115]

        if (
                not player_posi.get(start) and player_posi.get(dest)
                or start == dest
            ):
            print("Invalid square")
            continue
        else:
            pos[start_posi], pos[dest_posi] = square, pos[start_posi]
            if pos in searched_moves:
                return pos
            else:
                continue


position = list(posiii)
print(board_view(position))
white_to_move = True
player = ""

while True:
    print("Write w or W to choose White pieces. Else write b or B to choose "
          "Black pieces.")
    choice = input()
    if choice in ['w', 'W']:
        player = "white"
        break
    elif choice in ['b', 'B']:
        player = "black"
        white_to_move = False
        break
    else:
        continue

# THIS NEEDS TO BE CLEANED, BUT IT WORKS OK
if not white_to_move:
    white_to_move = True
    # Change starting position here
    fetched_moves = get_piece_moves(position, white_to_move, _pieces)
    orig_fetched_moves = list(fetched_moves)
    searched_moves = search_checks(orig_fetched_moves, white_to_move, player)
    random_posi = random.choice(searched_moves[0][0])
    white_to_move = False

    position = first_rotation(random_posi)
    fetched_moves = get_piece_moves(random_posi, white_to_move, _pieces)
    orig_fetched_moves = list(fetched_moves)
    searched_moves = search_checks(orig_fetched_moves, white_to_move, player)

    print(board_view(position))
    random_posi = play_move(position, searched_moves[0][0], player)
else:
    fetched_moves = get_piece_moves(position, white_to_move, _pieces)
    orig_fetched_moves = list(fetched_moves)
    searched_moves = search_checks(orig_fetched_moves, white_to_move, player)
    random_posi = play_move(position, searched_moves[0][0], player)

print(board_view(random_posi))

if white_to_move:
    if random_posi[110] != 'R':
        king_rook_move['K']['ROOK_Q'] = True
    if random_posi[117] != 'R':
        king_rook_move['K']['ROOK_K'] = True
    if random_posi[114] != 'K':
        king_rook_move['K']['KING'] = True
else:
    if random_posi[110] != 'r':
        king_rook_move['k']['ROOK_Q'] = True
    if random_posi[117] != 'r':
        king_rook_move['k']['ROOK_K'] = True
    if random_posi[114] != 'k':
        king_rook_move['k']['KING'] = True

while True:
    white_to_move = bool_negation(white_to_move)
    if player != "black":
        rotate(random_posi)
    fetched_moves = get_piece_moves(random_posi, white_to_move, _pieces)
    orig_fetched_moves = list(fetched_moves)
    searched_moves = search_checks(orig_fetched_moves, white_to_move, player)
    if not searched_moves[0][0]:
        print("It is checkmate or stalemate")
        exit()

   # if white_to_move and player == "white":
    if player != 'black':
        if white_to_move:
            random_posi = play_move(random_posi, searched_moves[0][0], player)
        else:
            random_posi = random.choice(searched_moves[0][0])
    else:
        if white_to_move:
            random_posi = random.choice(searched_moves[0][0])
        else:
            random_posi = play_move(random_posi, searched_moves[0][0], player)
    # if white_to_move and player == "black":
    #if not white_to_move and player == "white":

   # if not white_to_move and player == "black":
   # else:

    #print("KING ROOK MOVE", king_rook_move)

    if white_to_move:
        if random_posi[110] != 'R':
            king_rook_move['K']['ROOK_Q'] = True
        if random_posi[117] != 'R':
            king_rook_move['K']['ROOK_K'] = True
        if random_posi[114] != 'K':
            king_rook_move['K']['KING'] = True
    else:
        if random_posi[110] != 'r':
            king_rook_move['k']['ROOK_Q'] = True
        if random_posi[117] != 'r':
            king_rook_move['k']['ROOK_K'] = True
        if random_posi[114] != 'k':
            king_rook_move['k']['KING'] = True
    #print(king_rook_move)
    if player != 'black':
        if not white_to_move:
            print(board_view(rotate(list(random_posi))))
        else:
            print(board_view(random_posi))
    else:
        print(board_view(random_posi))
    #print("WHITE TO MOVE", white_to_move)
    time.sleep(4.7)
###############

toc = time.process_time()
print("time spent:", toc - tic)
