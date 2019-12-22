#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import pprint
import time
import sys
from itertools import chain
import itertools
import pickle

tic = time.clock()

CHECKLIST_ONE = [24, 35, 108, 119]
CHECKLIST_TWO = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                36, 48, 60, 72, 84, 96, 109, 110, 111, 112,
                113, 114, 115, 116, 117, 118, 95, 83, 71, 59,
                47]

"""Use these two boards to play around"""

#The board representation
posiii = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,                  #0-11
    0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0,                  #12-23
    0, 0, 'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r', 0, 0,  #24-35     #26-33
    0, 0, 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 0, 0,  #36-47     #38-45
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  #48-59     #50-57
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  #60-71     #62-69
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  #72-83     #74-81
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  #84-95     #86-93
    0, 0, 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 0, 0,  #96-107    #98-105
    0, 0, 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R', 0, 0,  #108-119   #110-117
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,                  #120-131
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0                   #132-143
    ]

#The board for testing moves and functions of different pieces
posi = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,                  #0-11
    0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0,                  #12-23
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  #24-35     #26-33
    0, 0, 'P', '-', '-', '-', '-', '-', '-', 'k', 0, 0,  #36-47     #38-45
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  #48-59     #50-57
    0, 0, '-', '-', '-', '-', 'p', '-', '-', '-', 0, 0,  #60-71     #62-69
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  #72-83     #74-81
    0, 0, '-', '-', 'K', '-', '-', '-', '-', '-', 0, 0,  #84-95     #86-93
    0, 0, '-', '-', '-', '-', '-', '-', 'p', '-', 0, 0,  #96-107    #98-105
    0, 0, '-', '-', '-', '-', '-', '-', '-', '-', 0, 0,  #108-119   #110-117
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,                  #120-131
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0                   #132-143
    ]

#Used for printing the board
def board_view(list):
    view = [list[i:i + 12] for i in xrange(0, 11, 12)]
    o = '\n'.join(map(str, view))
    view_2 = [list[i:i + 12] for i in xrange(12, 23, 12)]
    o_2 = '\n'.join(map(str, view_2))
    view_3 = [list[i:i + 12] for i in xrange(24, 117, 12)]
    o_3 = '\n'.join(map(str, view_3))
    view_4 = [list[i:i + 12] for i in xrange(120, 131, 12)]
    o_4 = '\n'.join(map(str, view_4))
    view_5 = [list[i:i + 12] for i in xrange(132, 143, 12)]
    o_5 = '\n'.join(map(str, view_5))
    good_board = '\t%s\n\t%s\n%s\n\t%s\n\t%s\n' % (o, o_2, o_3, o_4, o_5)
    return good_board

#Illegal positions for pieces
ZEROS = [i for i, x in enumerate(posi) if x == 0]

X, Y = 1, 12
moves = {
"rook" : [X, Y, -X, -Y],
"knight" : [Y+Y-X, Y+Y+X, X+X+Y, X+X-Y, -Y-Y+X, -Y-Y-X, -X-X-Y, -X-X+Y],
"bishop" : [X+Y, X-Y, -X+Y, -X-Y],
"queen" : [X, Y, -X, -Y, X+Y, X-Y, -X+Y, -X-Y],
"king" : [X, Y, -X, -Y, X+Y, X-Y, -X+Y, -X-Y],
"pawn" : [-Y, -Y-Y, -Y+X, -Y-X]
}

#The function for rotating the board; used when a move is made
#and it is other player's move.
def rotate(BOARD):
    for SQUARE in range(0, 8):
        BOARD[26+SQUARE], BOARD[117-SQUARE] \
        = BOARD[117-SQUARE], BOARD[26+SQUARE]
    for SQUARE in range(0, 8):
        BOARD[38+SQUARE], BOARD[105-SQUARE] \
        = BOARD[105-SQUARE], BOARD[38+SQUARE]
    for SQUARE in range(0, 8):
        BOARD[50+SQUARE], BOARD[93-SQUARE] \
        = BOARD[93-SQUARE], BOARD[50+SQUARE]
    for SQUARE in range(0, 8):
        BOARD[62+SQUARE], BOARD[81-SQUARE] \
        = BOARD[81-SQUARE], BOARD[62+SQUARE]
    return BOARD


white_pieces = {
    "king": 'K', "rook": 'R', "pawn": 'P',
    "knight": 'N', "queen": 'Q', "bishop": 'B'
    }

_pieces = {
    "king": 'K', "rook": 'R', "pawn": 'P',
    "knight": 'N', "queen": 'Q', "bishop": 'B'
    }

def lower_case(d):
    new = dict((k.lower(), v.lower()) for k,v in d.iteritems())
    return new

def upper_case(d):
    new = dict((k, v.upper()) for k,v in d.iteritems())
    return new

def upper_keys(d):
    new = dict((k.upper(), v) for k,v in d.iteritems())
    return new

#Maybe will be used later
def low(d):
    new = dict((k.lower(), v) for k,v in d.iteritems())
    return new

#Two lists for positions and lists of moves for White and Black
newlist = {'K': [], 'R': [], 'P': [], 'N': [], 'Q': [], 'B': []} #White
position = {'K': [], 'R': [], 'P': [], 'N': [], 'Q': [], 'B': []} #White
newlist_B = {'k': [], 'r': [], 'p': [], 'n': [], 'q': [], 'b': []} #Black
position_B = {'k': [], 'r': [], 'p': [], 'n': [], 'q': [], 'b': []} #Black
RANGE_SQUARE_NUMBERS = []
RANGE_SQUARES = []
enemy = []
enemy_w = []
ene = []
PIECE_POSITIONS = []

class Dictionaries(object):

    pass

# These will be implemented to prevent castling
#kingmove = False
#rookmove = False

CHECKING_SQUARE_LIST = []

class Whitem(Dictionaries):

    def __init__(self, kingmove, rookmove, white_to_move, newlist, newlist_B, pieces, posis, start):
        self.kingmove = kingmove
        self.rookmove = rookmove
        self.white_to_move = white_to_move
        self.newlist = newlist
        self.newlist_B = newlist
        self.pieces = pieces
        self.posis = posis
        self.start = start

    def move_gen(self, posi):
        # Links necessary lists to enumerate moves and positions.
        global white_pieces
        del RANGE_SQUARE_NUMBERS[:]
        del RANGE_SQUARES[:]
        del ene[:]
        del enemy[:]
        del enemy_w[:]
        del PIECE_POSITIONS[:]

        if self.white_to_move:
            self.pieces = upper_case(self.pieces)
        else:
            self.pieces = lower_case(self.pieces)

#         self.posis.append(self.start)

        OWN_PIECES = []

        for piece in self.pieces:
            orig_posi = list(self.start)
            OWN_PIECES = [i for i, x in enumerate(orig_posi) if x == self.pieces[piece]]
#             print OWN_PIECES
#             orig_posi = list(self.posis[0])
            mod_posi = list(orig_posi)
#             print "PIECE", piece
            if OWN_PIECES != []:
                for enum_piece in OWN_PIECES:
                    if self.pieces[piece] in ['R','Q','B','r','q','b']:
                        rang = 8
                    else:
                        rang = 2
                    for move in moves[piece]:
                        if (self.pieces[piece] in ['P','p']) and (moves[piece][1] == move) and (enum_piece not in range(98,106)):
                            continue
                        ate_piece = False
                        for go in range(1, rang):
#                             print mod_posi[enum_piece + move * go]
                            if mod_posi[enum_piece + move * go] in (ZEROS + self.pieces.values()):
                                break
                            elif mod_posi[enum_piece + move * go] != '-':
                                ate_piece = True
                                original_square = '-'
                            else:
                                original_square = mod_posi[enum_piece + move * go]
                                # Check if pawn's move is in the first two items in the list
                                if self.pieces[piece] in ['P','p'] and (move not in moves[piece][:2]):
                                    continue
                            mod_posi[enum_piece], mod_posi[enum_piece + move * go] = \
                            original_square, mod_posi[enum_piece]
                            self.posis.append(mod_posi)
#                             print board_view(mod_posi)
                            mod_posi = list(orig_posi)
                            if ate_piece:
                                break

#         piece_avoid = upper_case(self.pieces).values() + lower_case(self.pieces).values()
#
#         print piece_avoid

        return

        ###

        #kings.seek_threats(posi)
        kings.check = False

        SIZE = 0

        for i in self.newlist: #empties the list
            self.newlist[i] = []
        for i in self.newlist_B: #empties the list
            self.newlist_B[i] = []

        if self.white_to_move == False:
            kings.CURRENT_PIECE = [i for i, x in enumerate(posi) if x == 'k'][0]
            self.newlist_B = upper_keys(self.newlist_B)
            self.newlist = low(self.newlist)
            #rotate(self.posi)
            white_pieces = lower_case(white_pieces)
        else:
            kings.CURRENT_PIECE = [i for i, x in enumerate(posi) if x == 'K'][0]
            self.newlist_B = low(self.newlist_B)
            self.newlist = upper_keys(self.newlist)
            white_pieces = upper_case(white_pieces)

        kings.seek_threats(posi, kings.CURRENT_PIECE)

        print kings.piece

        LOOK_ALL = 1

        while len(kings.kingSafety()[0]) + LOOK_ALL >= 2:
            kings.kingSafety()
            LOOK_ALL -= 1

        kings.pieces_attacking = []


        #Searches all white's pieces' positions
        for j in self.newlist.keys():
            T = [i for i, x in enumerate(posi) if x == j]
            PIECE_POSITIONS.append(T)
        PIECE_UNNESTED = list(itertools.chain.from_iterable(PIECE_POSITIONS))

        RANDOM_SQUARE = random.choice(PIECE_UNNESTED)
        PIECE = posi[RANDOM_SQUARE]

        print "RANDOM_SQ", RANDOM_SQUARE


        #print "SAFE?", kings.kingSafety()



        if kings.seek_threats(posi, kings.CURRENT_PIECE) != []:
            print kings.pieces_attacking
            attack_this = random.choice(kings.pieces_attacking)
            kings.pieces_attacking = []
            print kings.pieces_attacking
            print attack_this
            kings.seek_threats(posi, attack_this)

            kings.check = True
            if kings.pieces_attacking != []:
                while kings.check:
                    attack_that = random.choice(kings.pieces_attacking)
                    previous_piece = attack_that
                    posi[attack_this], posi[attack_that] = \
                    posi[attack_that], posi[attack_this]
                    posi[attack_that] = "-"
                    kings.pieces_attacking = []
                    if kings.seek_threats(posi, kings.CURRENT_PIECE) != []:
                        attack_that = previous_piece
                        posi[attack_that], posi[attack_this] = \
                        posi[attack_this], posi[attack_that]
                        continue
                    else:
                        return posi
            if self.white_to_move == True:
                PIECE = 'K'
                RANDOM_SQUARE = [i for i, y in enumerate(posi) if y == 'K']
                SIZE += 1
                RANDOM_SQUARE = RANDOM_SQUARE[0]
            elif self.white_to_move == False:
                PIECE = 'k'
                RANDOM_SQUARE = [i for i, y in enumerate(posi) if y == 'k']
                SIZE += 1
                RANDOM_SQUARE = RANDOM_SQUARE[0]

            #else:
            #    RANDOM_SQUARE = kings.CURRENT_PIECE
            #    PIECE = posi[RANDOM_SQUARE]

        #kings.check = False

        #print "posiiii", RANDOM_SQUARE
        PIECE_STRING = white_pieces.keys()[white_pieces.values().index(PIECE)]

        F = [x.lower() for x in list(self.newlist)]
        for MOVE in moves[PIECE_STRING]:
            H = MOVE + RANDOM_SQUARE
            P = posi[MOVE + RANDOM_SQUARE]
            self.newlist[PIECE].append(H)
            ene.append(P)

        for ENEMY_PIECE in self.newlist_B:
            # Checks are there enemy pieces in ene list
            SQUARES = [i for i, y in enumerate(ene[1:3]) if y == ENEMY_PIECE]
            for SQUARE in SQUARES:
                # enemy_w is for king, pawn and knight. They are not
                # ranged pieces
                enemy.append(SQUARE)

        #newlist is a list of possible moves of randomly selected piece
        RND_MOVE = random.choice(self.newlist[PIECE])
        # RND_MOVE is a random move of PIECE

        # Pawns' initial squares
        INITIAL_PAWN_SQUARE = any(x in [RANDOM_SQUARE] \
        for x in list(range(98, 105)))

        # posi[RND_MOVE] == '-' is a condition for square to be empty
        if PIECE in ['B', 'R', 'Q', 'b', 'r', 'q'] \
        and posi[RND_MOVE] == '-':
            n = 8
            for RANGE in range(1, 8):
                while (any(x in list(self.newlist) \
                for x in RANGE_SQUARES) == False):
                    try:
                        M = RANDOM_SQUARE - (RANDOM_SQUARE-RND_MOVE)*RANGE
                        B = posi[RANDOM_SQUARE - \
                        (RANDOM_SQUARE-RND_MOVE)*RANGE]
                        # Not moving to a square which is zero
                        # No jumping over Black pieces
                        # No jumping over White pieces
                        # Stay inside board, no 'floor' to 'roof' action
                        if any(x in ZEROS for x in RANGE_SQUARE_NUMBERS) \
                        == False \
                        and any(x in list(self.newlist_B) for x in \
                        RANGE_SQUARES) == False \
                        and any(x in list(self.newlist) for x in \
                        RANGE_SQUARES) == False \
                        and ((RANDOM_SQUARE \
                        - (RANDOM_SQUARE-RND_MOVE)*RANGE) - (RANDOM_SQUARE \
                        - (RANDOM_SQUARE-RND_MOVE)*(RANGE-1))) < 14:
                            RANGE_SQUARE_NUMBERS.append(M)
                            RANGE_SQUARES.append(B)
                        break
                    except IndexError:
                        break

            if PIECE == 'R' or 'r':
                self.rookmove = True
            else:
                pass

            for ENEMY_PIECE in self.newlist_B:
                SQUARES = [i for i, y in enumerate(RANGE_SQUARES) \
                if y == ENEMY_PIECE]
                for SQUARE in SQUARES:
                    enemy.append(SQUARE)

            if enemy != []: #list of opponents pieces for capture
                ENEMY_INDEX = min(s for s in enemy)
                CAPTURE = RANGE_SQUARE_NUMBERS[ENEMY_INDEX]

                if posi[CAPTURE] not in self.newlist.keys() + ['k', 'K', 0]:
                    # Below piece of code means that a move is made
                    posi[RANDOM_SQUARE], posi[CAPTURE] \
                    = posi[CAPTURE], posi[RANDOM_SQUARE]
                    posi[RANDOM_SQUARE] = '-'
                    return posi
                else:
                    pass
            else:
                pass

            INDICES = [i for i, y in enumerate(RANGE_SQUARES) if y == '-']
            FREE_SQUARE_INDEX = random.choice(INDICES)
            FREE_SQUARE = RANGE_SQUARE_NUMBERS[FREE_SQUARE_INDEX]

            if posi[FREE_SQUARE] != 0:
                posi[RANDOM_SQUARE], posi[FREE_SQUARE] = \
                posi[FREE_SQUARE], posi[RANDOM_SQUARE]
                return posi
            else:
                Whitem.move_gen(self, posi)
        else:
            if (PIECE == 'P' or PIECE == 'p') and posi[RANDOM_SQUARE - \
            (RANDOM_SQUARE-self.newlist[PIECE][0])] == '-':
                if enemy != []:
                    ENEMY_INDEX = random.choice(enemy)
                    CAPTURE = self.newlist[PIECE][ENEMY_INDEX + 1]
                    if posi[CAPTURE] not in self.newlist.keys() \
                    + ['k', 'K']:
                        posi[RANDOM_SQUARE], posi[CAPTURE] = \
                        posi[CAPTURE], posi[RANDOM_SQUARE]
                        posi[RANDOM_SQUARE] = '-'
                        return posi
                    else:
                        pass

                elif INITIAL_PAWN_SQUARE == True and (PIECE == 'P' or PIECE \
                == 'p') and posi[self.newlist[PIECE][0] - 12] == '-' and \
                posi[self.newlist[PIECE][0] - 24] == '-':
                    # Pawn moves randomly one or two squares depending on
                    # z value.
                    z = random.choice(range(1, 3))
                    posi[RANDOM_SQUARE], posi[RANDOM_SQUARE - \
                    (RANDOM_SQUARE-self.newlist[PIECE][0])*z] = \
                    posi[RANDOM_SQUARE - (RANDOM_SQUARE \
                    - self.newlist[PIECE][0])*z], posi[RANDOM_SQUARE]
                    return posi
                else:
                    posi[RANDOM_SQUARE], \
                    posi[self.newlist[PIECE][0]] = \
                    posi[self.newlist[PIECE][0]], posi[RANDOM_SQUARE]
                    return posi

            if RANDOM_SQUARE in CHECKLIST_ONE:
                SIZE = 3
            elif RANDOM_SQUARE in CHECKLIST_TWO:
                SIZE = 5
            else:
                SIZE = 8

            if len(CHECKING_SQUARE_LIST) == SIZE:
                print "Checkmate!"
                exit(1)

            # Normal king move or captures enemy piece
            elif (PIECE == 'K' or PIECE == 'k') and (posi[RANDOM_SQUARE \
            - (RANDOM_SQUARE-RND_MOVE)*2] not in ['K', 'k']):
                noppa = random.choice(range(0, 2))
                if enemy != []:

                    print "SEEK", kings.seek_threats(posi, RANDOM_SQUARE)

                    ENEMY_INDEX = random.choice(enemy)
                    CAPTURE = self.newlist[PIECE][ENEMY_INDEX + 1]
                    # No capturing enemy King or own pieces
                    if posi[CAPTURE] not in self.newlist.keys() \
                    + ['k', 'K']:
                        X_ = posi[CAPTURE]
                        posi[RANDOM_SQUARE], posi[CAPTURE] \
                        = posi[CAPTURE], posi[RANDOM_SQUARE]
                        posi[RANDOM_SQUARE] = '-'

                        print kings.check
                        if kings.check == True:
                            if CAPTURE not in CHECKING_SQUARE_LIST:
                                CHECKING_SQUARE_LIST.append(CAPTURE)
                            posi[CAPTURE] = X_
                            posi[RANDOM_SQUARE] = PIECE
                            print "back to normal"
                            Whitem.move_gen(self, posi)
                        del CHECKING_SQUARE_LIST[:]
                        return posi
                    else:
                        pass
                # Check if castling is a legal move
                elif noppa == 0 and self.kingmove == False and \
                self.rookmove == False and (posi[117] == 'R' or 'r') and \
                posi[115] == posi[116] == '-' \
                and posi[114] in ['K', 'k']:
                    posi[RANDOM_SQUARE], posi[115], posi[116], \
                    posi[117] = posi[115], posi[117], \
                    posi[RANDOM_SQUARE], posi[116]
                # Check if castling is a legal move
                elif noppa == 1 and self.kingmove == False and \
                self.rookmove == False and \
                posi[110] in ['R', 'r'] \
                and all(x=='-' for x in posi[111:113]) \
                and posi[114] in ['K', 'k']:
                    posi[110], posi[111], posi[112], \
                    posi[113], posi[RANDOM_SQUARE] \
                    = posi[113], posi[112], \
                    posi[RANDOM_SQUARE], posi[110], posi[111]
                    self.kingmove = True
                    self.rookmove = True
                else:
                    if posi[RANDOM_SQUARE - (RANDOM_SQUARE-RND_MOVE)] == '-':
                        self.kingmove = True
                        posi[RANDOM_SQUARE], posi[RND_MOVE] \
                        = posi[RND_MOVE], posi[RANDOM_SQUARE]

                        for i in moves["king"]:
                            if posi[RND_MOVE + i] in ['K', 'k']:
                                print "kunkku close"
                                posi[RND_MOVE], posi[RANDOM_SQUARE] \
                                = posi[RANDOM_SQUARE], posi[RND_MOVE]
                                Whitem.move_gen(self, posi)

                        kings.seek_threats(posi, RANDOM_SQUARE)
                        print "howmany??", kings.pieces_attacking
                        print kings.check
                        if kings.seek_threats(posi, RANDOM_SQUARE) != []:
                            if RND_MOVE not in CHECKING_SQUARE_LIST:
                                CHECKING_SQUARE_LIST.append(RND_MOVE)
                            print "back to normaaal"
                            posi[RND_MOVE], posi[RANDOM_SQUARE] \
                            = posi[RANDOM_SQUARE], posi[RND_MOVE]
                            Whitem.move_gen(self, posi)
                        del CHECKING_SQUARE_LIST[:]
                        return posi
                    else:
                        Whitem.move_gen(self, posi)
            # Knight captures a piece which is not the king or moves
            # to a different square.
            elif (PIECE == 'N' or PIECE == 'n') and posi[RANDOM_SQUARE \
            - (RANDOM_SQUARE-RND_MOVE)] == '-':
                if enemy != []:
                    ENEMY_INDEX = random.choice(enemy)
                    CAPTURE = self.newlist[PIECE][ENEMY_INDEX + 1]
                    if posi[CAPTURE] not in (self.newlist.keys() \
                    + ['k', 'K']):
                        posi[RANDOM_SQUARE], posi[CAPTURE] \
                        = posi[CAPTURE], posi[RANDOM_SQUARE]
                        posi[RANDOM_SQUARE] = '-'
                        return posi
                    else:
                        pass
                else:
                    posi[RANDOM_SQUARE], posi[RANDOM_SQUARE - \
                    (RANDOM_SQUARE-RND_MOVE)] = posi[RANDOM_SQUARE - \
                    (RANDOM_SQUARE-RND_MOVE)], posi[RANDOM_SQUARE]
                    return posi
            elif posi[RANDOM_SQUARE - (RANDOM_SQUARE-RND_MOVE)] == 0:
                Whitem.move_gen(self, posi)
            else:
                Whitem.move_gen(self, posi)


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

def chess_engine(): #This will be used for the evaluation function

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
        #print board_view(posi)
        #if first_save:
        #    this_board = board_object(posi)
            #BOARD_LIST[1] = board_object(posi)
        BOARD_LIST.append(board_object(posi))
        #    aaa = this_board.posi
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

    #for i in range(0, LIMIT):


    for i in range(0, LIMIT):
        print EVALUATIONS[i]

    print board_view(BOARD_LIST[LIMIT].posi)


    #Boards could be keys and evaluations values in dictionary


#check_these_pieces = []

class Threat(object):

    def __init__(self, check, piece, CURRENT_PIECE):
        self.check = check
        self.piece = piece
        self.CURRENT_PIECE = CURRENT_PIECE
        self.pieces_attacking = []

    def seek_threats(self, posit, initial_piece_square):
        #posi = test
        #See if the king is in check
        initial_piece = posit[initial_piece_square]

        #print "INITIAL", initial_piece

        own_pieces = white_pieces.values()
        opponent_pieces = white_pieces

        if initial_piece.isupper():
            opponent_pieces = lower_case(white_pieces)
            #opponent_pieces = map(lambda x:x.lower(),opponent_pieces)
        else:
            own_pieces = map(lambda x:x.lower(),own_pieces)

        #print opponent_pieces

        #initial_piece_square = [i for i, x in enumerate(posit) if x == initial_piece]

        #initial_piece_square = random.choice(initial_piece_square)
         #or x == 'k']
        #print "initial_piece_square:", initial_piece_square

        #print opponent_pieces.values()

        for index, name in enumerate(white_pieces.keys()):
            #print(index, name)
            #print moves[name]
            if index == 2:
                moves[name] = moves[name][1:]
            for i in moves[name]:
                if index in [1, 4, 5]:
                    j = 1
                    while posit[initial_piece_square + i * j] == '-' or \
                    posit[initial_piece_square + i * j] == opponent_pieces[name]:
                        if posit[initial_piece_square + i * j] == opponent_pieces[name]:
                            #print "PIECE", name
                            self.pieces_attacking.append(initial_piece_square + i * j)
                        j += 1
                if index == 2:
                    if posit[initial_piece_square + i] == opponent_pieces[name]:
                        #print "PIECE", name
                        self.pieces_attacking.append(initial_piece_square + i)
                if index in [0, 3]:
                    if posit[initial_piece_square + i] == opponent_pieces[name]:
                        #print "PIECE", name
                        self.pieces_attacking.append(initial_piece_square + i)

                #    if posit[initial_piece_square + i] == opponent_pieces[name]
        #print self.pieces_attacking
        #print "SELF", self.CURRENT_PIECE
        return self.pieces_attacking

    def kingSafety(self):
        if posi[self.CURRENT_PIECE] in ['K', 'k'] and self.pieces_attacking != []:
            self.check = True
            self.piece = random.choice(self.pieces_attacking)
            self.pieces_attacking = []
            #print "HESSU"
            self.seek_threats(posi, self.piece)
            return (self.pieces_attacking, self.piece)
            #return
        else:
            self.check = False
            return (self.pieces_attacking, self.CURRENT_PIECE)

def capture_piece():
    if kings.check:
        PIECE = kings.piece


        #print board_view(test)

#b_game = Blackm()
kings = Threat(False, None, None)

def moving_randomly():
    turn()

def turn():
    while True:
        print board_view(posi)
        print "Press enter to play"
        m = raw_input()
        if m == "":
            a_game.move_gen(posi)
            print board_view(posi)
            print "Press enter to play"
            rotate(posi)
            a_game.white_to_move = False
            nassu = raw_input()
            if nassu == "":
                print a_game.white_to_move
                a_game.move_gen(posi)
                a_game.white_to_move = True
                rotate(posi)
                print board_view(posi)
            else:
                continue
        else:
            continue

def turn_test():
    while True:
        a_game.move_gen()
        print board_view(posi)
        time.sleep(0.7)
        rotate(posi)
        b_game.move_gen()
        rotate(posi)
        print board_view(posi)



def get_piece_moves(posi, white_to_move, _pieces):

    if white_to_move:
        _pieces = upper_case(_pieces)
    else:
        _pieces = lower_case(_pieces)
#         posi = rotate(posi)

#         self.posis.append(self.start)

    positions = []

    OWN_PIECES = []

    for piece in _pieces:
        orig_posi = list(posi)
        OWN_PIECES = [i for i, x in enumerate(orig_posi) if x == _pieces[piece]]
        mod_posi = list(orig_posi)
        if OWN_PIECES != []:
            for enum_piece in OWN_PIECES:
                # Count more moves for ranger pieces
                if _pieces[piece] in ['R','Q','B','r','q','b']:
                    rang = 8
                else:
                    rang = 2
                for move in moves[piece]:
                    # This checks if a pawn is on its original square
                    if (_pieces[piece] in ['P','p']) and (moves[piece][1] == move) and (enum_piece not in range(98,106)):
                        continue
                    ate_piece = False
                    for go in range(1, rang):
#                             print mod_posi[enum_piece + move * go]
                        if mod_posi[enum_piece + move * go] in (ZEROS + _pieces.values()):
                            break
                        elif mod_posi[enum_piece + move * go] != '-':
                            ate_piece = True
                            original_square = '-'
                        else:
                            original_square = mod_posi[enum_piece + move * go]
                            # Check if pawn's move is in the first two items in the list
                            if _pieces[piece] in ['P','p'] and (move not in moves[piece][:2]):
                                continue
                        if _pieces[piece] in ['P','p'] and ((enum_piece + move * go) in range(26,34)):
                            if _pieces[piece].isupper():
                                mod_posi[enum_piece] = 'Q'
                            else: mod_posi[enum_piece] = 'q'

                        mod_posi[enum_piece], mod_posi[enum_piece + move * go] = \
                        original_square, mod_posi[enum_piece]

                        positions.append(mod_posi)
                        mod_posi = list(orig_posi)
                        if ate_piece:
                            break
    return positions, posi

def bool_negation(bool):
    return not bool

def search_checks(orig_fetched_moves, white_to_move):
    white_to_move = bool_negation(white_to_move)
    remove_these = []
    for posit in orig_fetched_moves[0]:
        # white to move is set to false
        rotate(posit)
        fetched_moves = get_piece_moves(posit, white_to_move, _pieces)

        # Search boards if one king is missing
        for board in fetched_moves[0]:
#             rotate(board)
#             print board_view(board)
#             rotate(board)
            kings = [i for i, x in enumerate(board) if x in ['K', 'k']]
#             print "kings", kings
            if len(kings) < 2:
                remove_these.append(posit)
                break
#                 orig_fetched_moves[0].remove(posit)
        rotate(posit)
    for rem in remove_these:
        orig_fetched_moves[0].remove(rotate(rem))
    white_to_move = bool_negation(white_to_move)
#                 return search_checks(orig_fetched_moves, white_to_move)
    return orig_fetched_moves, white_to_move


#moving_randomly()
# a_game = Whitem(False, False, True, newlist, newlist_B, _pieces, [], posi)

# for rand in searched_moves[0][0]:
#     print board_view(rand)

# def bit_board_move(random_posi, white_to_move, _pieces):
#     fetched_moves = get_piece_moves(random_posi, white_to_move, _pieces)
#     orig_fetched_moves = list(fetched_moves)
#     searched_moves = search_checks(orig_fetched_moves, white_to_move)
#     random_posi = random.choice(searched_moves[0][0])
#     print "fetched len", len(fetched_moves[0])
#     print board_view(random_posi)
# #     white_to_move = searched_moves[1]
# #     white_to_move = bool_negation(white_to_move)
#     print "WHITE TO MOVE", white_to_move
#     if searched_moves[0][0] == []:
#         print "It is checkmate"
#         exit()

print board_view(posi)
white_to_move = True

# Change starting position here
fetched_moves = get_piece_moves(posi, white_to_move, _pieces)
orig_fetched_moves = list(fetched_moves)
searched_moves = search_checks(orig_fetched_moves, white_to_move)
random_posi = random.choice(searched_moves[0][0])
print board_view(random_posi)
# rotate(random_posi)
# white_to_move = searched_moves[1]
print "WHITE TO MOVE", white_to_move

while True:
    white_to_move = bool_negation(white_to_move)
    rotate(random_posi)
    fetched_moves = get_piece_moves(random_posi, white_to_move, _pieces)
    orig_fetched_moves = list(fetched_moves)
    searched_moves = search_checks(orig_fetched_moves, white_to_move)
    if searched_moves[0][0] == []:
        print "It is checkmate or stalemate"
        exit()
    random_posi = random.choice(searched_moves[0][0])
    if not white_to_move:
        print board_view(rotate(list(random_posi)))
    else:
        print board_view(random_posi)
    print "WHITE TO MOVE", white_to_move
    time.sleep(0.7)
###############

toc = time.clock()
print "time spent:", toc - tic
