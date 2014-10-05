#!/usr/bin/env python
# 

#
# Game Programming, Level 2 Project
#
# TIC-TAC-TOE 4
#
# Radmer van der Heyde & Chelsea Bailey
# October 5, 2014

# Things of Note:
#   Our game quits as soon as a draw is guaranteed
#   To optimize minimax we implemented both caching and giving up
#   We end our search depth at 6 moves and evaluate the board based on which player has the most potential wins still
#       These values are cleared from the dictionary before the next turn to allow for reevalution if final depth is reached
#
# Project Reflection:
#   We felt this project was much more challenging than Rush Hour, but the good kind of challenging. 
#   Despite our frustrations at times we learned a lot and quite enjoyed the overall experience.
#   Given more time we know our final product could be greatly improved.

import sys

from graphics import *

def fail (msg):
    raise StandardError(msg)


def create_board (string):
    # Takes a description of the board as input and creates the board
    #  in our representation
    
    board = []
    for i in range(len(string)):
        board.append(string[i])
    return board

def has_mark (board,x,y):
    # Takes a board representation and checks if there's a mark at
    #    spot x in the array
    # Returns 'X' or 'O' if there is a mark
    # Returns False if there is not
    
    if board[x] != '.':
        return board[x]
    else:
        return False

def possible_moves (board):
    return [i for (i,e) in enumerate(board) if e == '.']

def has_win (board):
    # Checks if a board is a win for X or for O.
    # Returns 'X' if it is a win for X, 'O' if it is a win for O,
    # and False otherwise
    win_states = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[0,5,10,15],[3,6,9,12],[0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15]]
    
    for win in win_states:
        if board[win[0]] == board[win[1]] and board[win[0]] == board[win[2]] and board[win[0]] == board[win[3]]:
            if board[win[0]] == 'X':
                return 'X'
            elif board[win[0]] == 'O':
                return 'O'

    return False

def done (board):
    # Checks if only ties are still possible
    # Returns True if only ties are left
    # Returns has_win(board) if a player has won and False otherwise
    impossible=0
    win_states = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[0,5,10,15],[3,6,9,12],[0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15]]
    for win in win_states:
        if (board[win[0]] == 'X' or board[win[1]] == 'X' or board[win[2]] == 'X' or board[win[3]] == 'X') and (board[win[0]] == 'O' or board[win[1]] == 'O' or board[win[2]] == 'O' or board[win[3]] == 'O'):
            impossible+=1
    if impossible == 10:
        return True

    return (has_win(board) or not [ e for e in board if (e == '.')])



def print_board (board):
    # Converts the board into a string
    # Prints board to console

    display = ''
    for i in board: 
        display +=i

    print (display[0:4])
    print (display[4:8])
    print (display[8:12])
    print (display[12:16])
    print ' '
    print ' '

def draw_board(board,win):
    # Draws game board in window
    # Draws on X's and O's
    brd=[]
    brd.append(board[0:4])
    brd.append(board[4:8])
    brd.append(board[8:12])
    brd.append(board[12:16])

    for i in range(110, 550, 110):
        for j in range(110, 550, 110):
            pt1 = Point(i-100,j-100)
            pt2 = Point(i, j)
            rectangle = Rectangle(pt1, pt2)
            rectangle.draw(win)
    for i in range(0,4):
        for j in range(0,4):
            pt= Point((j+1)*110-50,(i+1)*110-50) 
            if brd[i][j] == 'X':
                txt = Text(pt,'X')
                txt.setSize(36)
                txt.draw(win)
            elif brd[i][j] == 'O':
                txt = Text(pt,'O')
                txt.setSize(36)
                txt.draw(win)

def wait_player_input(board,player,tree,win):
    # Waits for mouse click from player
    # Converts mouse click to index for board
    moves=[[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]
    pt = win.getMouse()
    x,y = (pt.getX(),pt.getY())

    for i in range(0, 440, 110):
        for j in range(0, 440, 110):
            if x>i+10 and x<i+110 and y>j+10 and y<j+110:
                x1 = i/110
                y1 = j/110
                return moves[y1][x1]

def read_player_input (board, player, tree, win):
    # Reads player input when playing as 'player' (either 'X' or 'O')
    # Returns a move (0-15)
    # Currently runs wait_player_input for GUI but that can be commented out
    
    move = wait_player_input(board,player,tree,win)
    return move
    
    valid = [ i for (i,e) in enumerate(board) if e == '.']
    while True:
        move = raw_input('Position (0-15)? ')
        if move == 'q':
            exit(0)
        return int(move)
        if len(move)>0 or int(move)>15 or int(move)<0:
          print 'Try a valid move!'
          read_player_input(board,player,tree)

def make_move (board,move,player):
    # Returns a board where 'move' has been performed on 'board' by 
    #    'player'

    new_board = board[:]
    new_board[move] = player
    return new_board

def utility (board):
    # Called when game is completed
    # Returns a point value that corresponds to the game state
    if has_win(board) == 'O':
        return -10
    elif has_win(board) == 'X':
        return 10
    else:
        return 0

def evaluate(board):
    # Checks for possible wins for either X or O
    # Adds value if X can win, subtracts value if O can win, and returns final points

    poss=0

    win_states = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[0,5,10,15],[3,6,9,12],[0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15]]
    for win in win_states:
        if (board[win[0]] == 'X' or board[win[1]] == 'X' or board[win[2]] == 'X' or board[win[3]] == 'X') and (board[win[0]] != 'O' or board[win[1]] != 'O' or board[win[2]] != 'O' or board[win[3]] != 'O'):
            poss+=1
        if (board[win[0]] != 'X' or board[win[1]] != 'X' or board[win[2]] != 'X' or board[win[3]] != 'X') and (board[win[0]] == 'O' or board[win[1]] == 'O' or board[win[2]] == 'O' or board[win[3]] == 'O'):
            poss-=1
    return poss

def min_value (board, player,tree,depth):
    # The min part of minimax
    # Checks if depth is reached or game is over and returns value
    # Checks if board exists in dictionary
    # Makes next move on board
    
    scores = []
    moves = []
    win = 0

    depth+=1
    if depth > 5:
        return evaluate(board)

    if done(board) != False:
        return utility(board)

    for mov in possible_moves(board):
        new_board = make_move(board,mov,player)
        value = tree_check(board,tree)
        if value == None:
            win = max_value(new_board,other(player),tree,depth)
            scores.append(win)
            brd=board_to_string(new_board)
            tree[brd] = win
            moves.append(mov)
        else:
            scores.append(value)  
            moves.append(mov)   
        if value == -10:
            return value
        if win == -10:
            return win   

    score=min(scores)
    return score


def max_value (board,player,tree,depth):
    # Read above description of min_value (basic function is the same)
    scores = []
    moves = []
    win = 0

    depth+=1
    if depth > 5:
        return evaluate(board)

    if done(board) != False:
        return utility(board)

    for mov in possible_moves(board):
        new_board = make_move(board,mov,player)
        value = tree_check(board,tree)
        if value == None:
            win = min_value(new_board,other(player),tree,depth)
            scores.append(win)
            brd=board_to_string(new_board)
            tree[brd] = win
            moves.append(mov)   
        else:
            scores.append(value)
            moves.append(mov)  
        if value == 10:
            return value
        if win == 10:
            return win

    score = max(scores)
    return score

def computer_move (board,player,tree,win):
    # Runs through minimax
    # Evaluates as a minimizer if computer is O
    # Evaluates as a maximizer if computer is X

    scores = []
    moves = []
    win = 0

    for mov in possible_moves(board):
        depth = 0
        new_board = make_move(board,mov,player)
        value = tree_check(board,tree)
        if value == None:
            if player == 'O':
                win=max_value(new_board,other(player),tree,depth)
            else:
                win=min_value(new_board,other(player),tree,depth)
            scores.append(win)
            brd=board_to_string(new_board)
            tree[brd] = win
            moves.append(mov)
        else:
            scores.append(value)
            moves.append(mov)
        if player == 'O' and (value == -10 or win == -10):
            return mov
        elif player == 'X' and (value == 10 or win == 10):
            return mov
        print mov, value, win

    print moves
    print scores

    if player == 'O':
        move = moves[scores.index(min(scores))]
    else:
        move = moves[scores.index(max(scores))] 

    for key in tree:
        if tree[key] != 0 or tree[key] != 10 or tree[key] != -10:
            tree[key] = None

    return move

def tree_check(board,tree):
    # Takes in board and the existing game tree
    # Creates rotations of the board
    # Checks for each rotation in the dictionary
    # Returns value from dictionary, else it returns None

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
    # Takes in board
    # Returns 4 versions of board (the original board and each rotation)

    b1=board[:]
    b2=board[:]
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
    # Takes in board (list) and returns brd (string)
    brd=''
    for spot in board:
        brd+=str(spot)
    return brd


def other (player):
    #Switches players

    if player == 'X':
        return 'O'
    return 'X'


def run (stg,player,playX,playO): 

    board = create_board(stg)
    win = GraphWin('TIC-TAC-TOE',450,500)
    tree = {}

    print_board(board)
    draw_board(board,win)

    while not done(board):
        if player == 'X':
            move = playX(board,player,tree,win)
        elif player == 'O':
            move = playO(board,player,tree,win)
        else:
            fail('Unrecognized player '+player)
        board = make_move(board,move,player)
        print_board(board)
        draw_board(board,win)
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


