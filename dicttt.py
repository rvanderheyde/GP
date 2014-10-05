#!/usr/bin/env python
# 

#
# Game Programming, Level 2 Project
#
# TIC-TAC-TOE 4
#
# A simple strategy game, an extension of the standard 3x3 tic-tac-toe
#

import sys

from graphics import *

def fail (msg):
    raise StandardError(msg)


def create_board (string):
    # FIX ME
    #
    # Take a description of the board as input and create the board
    #  in your representation
    #
    # The string description is a sequence of 16 characters,
    #   each either X or O, or . to represent a free space
    # It is allowed to pass in a string describing a board
    #   that would never arise in legal play starting from an empty
    #   board
    board = []
    for i in range(len(string)):
        board.append(string[i])
    return board

def has_mark (board,x,y):
    # FIX ME
    #
    # Take a board representation and checks if there's a mark at
    #    position x, y (each between 1 and 4)
    # Return 'X' or 'O' if there is a mark
    # Return False if there is not
    #i = (y-1)*x
    i=x
    if board[i] != '.':
        return board[i]
    else:
        return False

def possible_moves (board):
    return [i for (i,e) in enumerate(board) if e == '.']

def has_win (board):
    # FIX ME
    # 
    # Check if a board is a win for X or for O.
    # Return 'X' if it is a win for X, 'O' if it is a win for O,
    # and False otherwise
    win_states = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[0,5,10,15],[3,6,9,12],[0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15]]
    for win in win_states:
        if board[win[0]] == board[win[1]] and board[win[0]] == board[win[2]] and board[win[0]] == board[win[3]]:
            if board[win[0]] == 'X':
                #print 'X won'
                return 'X'
            elif board[win[0]] == 'O':
                #print 'O won'
                return 'O'
        #for i in win:
         #   l = board[i]
    return False

def done (board):
    # FIX ME
    return (has_win(board) or not [ e for e in board if (e == '.')])

    #
    # Check if the board is done, either because it is a win or a draw
    # if has_win(board) == False:
    #     for i in range(0,15):
    #         if has_mark(board,i,0) == False:
    #             return False
    #     return True
        # for i in range(1,5):
        #     for j in range(1,5):
        #         if has_mark(board,i,j) == False:
        #             return False
        # return True
    # else:
    #     return True


def print_board (board):
    # FIX ME
    #
    # Display a board on the console
    display = ''
    for i in board: 
        display +=i

    print (display[0:4])
    print (display[4:8])
    print (display[8:12])
    print (display[12:16])
    return None

def draw_board(board,win):
    #fix me
    for i in range(100, 500, 100):
        for j in range(100, 500, 100):
            pt1 = Point(i-95,j-95)
            pt2 = Point(i-5, j-5)
            rectangle = Rectangle(pt1, pt2)
            rectangle.draw(win)
    for spot in board:
        return None
    return None

def wait_player_input(board,player,win):
    #fix me
    move = win.getMouse()
    #translate point into spot in array
    return move

def read_player_input (board, player,tree):
    # FIX ME
    #
    # Read player input when playing as 'player' (either 'X' or 'O')
    # Return a move (a tuple (x,y) with each position between 1 and 4)
    valid = [ i for (i,e) in enumerate(board) if e == '.']
    while True:
        move = raw_input('Position (x,y)? ')
        if move == 'q':
            exit(0)
        return int(move)
        #if len(move)>0:
         #   move_calc = int(move[0])*(int(move[1])-1)
          #  if move_calc in valid:
           #     return (int(move[0]),int(move[1]))
    return None

def make_move (board,move,player):
    # FIX ME
    #
    # Returns a board where 'move' has been performed on 'board' by 
    #    'player'
    # Change can be done in place in 'board' or a new copy created

    new_board = board[:]
    new_board[move] = player
    return new_board


def utility (board):
    # fix me
    if has_win(board) == 'O':
        return -1
    elif has_win(board) == 'X':
        return 1
    else:
        return 0

def min_value (board, player,tree):
    # fix me 
    scores = []
    moves = []
    if done(board) != False:
        #print 'Game over'
        return utility(board)

    for mov in possible_moves(board):
        new_board = make_move(board,mov,player)
        value = tree_check(board,tree)
        if value == None:
            win = max_value(new_board,other(player),tree)
            scores.append(win)
            brd=board_to_string(new_board)
            tree[brd] = win
            moves.append(mov)
        else:
            scores.append(value)  
            moves.append(mov)      

    score=min(scores)
    #print 'Minimizing',scores,score
    return score


def max_value (board,player,tree):
    # fix me
    scores = []
    moves = []
    if done(board) != False:
        #print 'Game over'
        return utility(board)

    for mov in possible_moves(board):
        new_board = make_move(board,mov,player)
        value = tree_check(board,tree)
        if value == None:
            win = min_value(new_board,other(player),tree)
            scores.append(win)
            brd=board_to_string(new_board)
            tree[brd] = win
            moves.append(mov)   
        else:
            scores.append(value)
            moves.append(mov)     

    score = max(scores)
    #print 'Maxing',scores, score
    return score

def computer_move (board,player,tree):
    # fix me
    scores = []
    moves = []

    for mov in possible_moves(board):
        new_board = make_move(board,mov,player)
        value = tree_check(board,tree)
        if value == None:
            score=max_value(new_board,other(player),tree)
            scores.append(score)
            brd=board_to_string(new_board)
            tree[brd] = score
            moves.append(mov)
        else:
            scores.append(value)
            moves.append(mov)


    print moves
    print scores

    move = moves[scores.index(min(scores))]
    print move
    return move

def tree_check(board,tree):
    b1,b2,b3,b4 = rotate_board(board)
    b1 = board_to_string(b1)
    b2 = board_to_string(b2)
    b3 = board_to_string(b3)
    b4 = board_to_string(b4)

    if b1 in tree:
        return tree[b1]
    elif b2 in tree:
        return tree[b2]
    elif b3 in tree:
        return tree[b3]
    elif b4 in tree:
        return tree[b4]
    else:
        return None

def rotate_board(board):
    b1=board
    b2=board
    b2.reverse()
    b3=[]
    b4=[]

    for i in range(3,0,-1):
        b3.append(b1[i])
        b3.append(b1[i+4])
        b3.append(b1[i+8])
        b3.append(b1[i+12])
        b4.append(b2[i])
        b4.append(b2[i+4])
        b4.append(b2[i+8])
        b4.append(b2[i+12])
    
    return b1, b2, b3, b4



def board_to_string(board):
    brd=''
    for spot in board:
        brd+=str(spot)
    return brd


def other (player):
    if player == 'X':
        return 'O'
    return 'X'


def run (stg,player,playX,playO): 

    board = create_board(stg)
    #win = GraphWin('TIC-TAC-TOE',450,500)
    tree = {}

    print_board(board)
    #draw_board(board,win)

    while not done(board):
        if player == 'X':
            move = playX(board,player,tree)
        elif player == 'O':
            move = playO(board,player,tree)
        else:
            fail('Unrecognized player '+player)
        board = make_move(board,move,player)
        print_board(board)
        player = other(player)

    winner = has_win(board)
    if winner:
        print winner,'wins!'
    else:
        print 'Draw'
        
def main ():
    run('.' * 16, 'X', read_player_input, computer_move)


PLAYER_MAP = {
    'human': read_player_input,
    'computer': computer_move
}

if __name__ == '__main__':

  try:
      stg = sys.argv[1] if len(sys.argv)>1 else '.' * 16
      player = sys.argv[2] if len(sys.argv)>3 else 'X'
      playX = PLAYER_MAP[sys.argv[3]] if len(sys.argv)>3 else read_player_input
      playO = PLAYER_MAP[sys.argv[4]] if len(sys.argv)>4 else computer_move
  except:
    print 'Usage: %s [starting board] [X|O] [human|computer] [human|computer]' % (sys.argv[0])
    exit(1)
  run(stg,player,playX,playO)


