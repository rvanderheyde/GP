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
    i = (y-1)*x
    if board[i] != '.':
        return board[i]
    else:
        return False

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
                return 'X'
            elif board[win[0]] == 'O':
                return 'O'
        #for i in win:
         #   l = board[i]
    return False

def done (board):
    # FIX ME
    #
    # Check if the board is done, either because it is a win or a draw
    if has_win(board) == False:
        for i in range(1,5):
            for j in range(1,5):
                if has_mark(board,i,j) == False:
                    return False
        return True
    else:
        return True


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

def read_player_input (board, player):
    # FIX ME
    #
    # Read player input when playing as 'player' (either 'X' or 'O')
    # Return a move (a tuple (x,y) with each position between 1 and 4)
    valid = [ i for (i,e) in enumerate(board) if e == '.']
    while True:
        move = raw_input('Position (x,y)? ')
        if move == 'q':
            exit(0)
        if len(move)>0:
            move_calc = int(move[0])*(int(move[1])-1)
            if move_calc in valid:
                return (int(move[0]),int(move[1]))
    return None

def make_move (board,move,player):
    # FIX ME
    #
    # Returns a board where 'move' has been performed on 'board' by 
    #    'player'
    # Change can be done in place in 'board' or a new copy created
    if move == None:
        return board
    else:
        x,y = move
        i = (y-1)*x
        board[i] = player
        return board

def computer_move (board,player):
    # FIX ME
    #
    # Select a move for the computer, when playing as 'player' (either 
    #   'X' or 'O')
    # Return the selected move (a tuple (x,y) with each position between 
    #   1 and 4)
    return None


def other (player):
    if player == 'X':
        return 'O'
    return 'X'


def run (str,player,playX,playO): 

    board = create_board(str)

    print_board(board)

    while not done(board):
        if player == 'X':
            move = playX(board,player)
        elif player == 'O':
            move = playO(board,player)
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
      str = sys.argv[1] if len(sys.argv)>1 else '.' * 16
      player = sys.argv[2] if len(sys.argv)>3 else 'X'
      playX = PLAYER_MAP[sys.argv[3]] if len(sys.argv)>3 else read_player_input
      playO = PLAYER_MAP[sys.argv[4]] if len(sys.argv)>4 else computer_move
  except:
    print 'Usage: %s [starting board] [X|O] [human|computer] [human|computer]' % (sys.argv[0])
    exit(1)
  run(str,player,playX,playO)


