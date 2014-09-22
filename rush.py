#!/usr/bin/env python

#
# Game Programming, Level 1 Project
#
# RUSH HOUR
#
# A simple puzzle game, based on the physical game of the same name 
# by Binary Arts Corp
#
# Chelsea Bailey and Radmer van der Heyde
# nothing really special here. Everything is functional and there should be no bugs. 
# Overall the project was not too bad.






GRID_SIZE = 6


def validate_move (brd,move):
    for vehicle in brd.vehicles:
        x,y = vehicle.position
        x,y = (x-1,y-1)
        players_vehicle = move[0]
        players_direction = move[1]
        players_distance = int(move[2])
        if players_vehicle == vehicle.name:
            if (players_direction == 'U' or players_direction == 'D') and vehicle.direction =='D':
                if players_direction == 'U':
                    for i in range(0,players_distance):
                        #print i 
                        if x-i <= 0:
                            print 'invalid distance'
                            return False
                        if brd.brd[x-i][y] != 0 and i != 0:
                            print 'invalid distance' 
                            return False
                    print "moving up"
                    return [vehicle,'U',players_distance]
                else:
                    for i in range(0,players_distance+1):
                        #print i
                        #print y+(vehicle.length-1)+i
                        
                        if x+(vehicle.length-1)+i > 5:
                            print 'invalid distance'
                            return False
                           # print brd.brd[x+(vehicle.length-1)+i][y]
                        if brd.brd[x+(vehicle.length-1)+i][y] != 0 and i != 0:
                            print 'invalid distance'
                            return False
                    return [vehicle,'D',players_distance]
                    print "moving down"
            elif  (players_direction == 'L' or players_direction == 'R') and vehicle.direction =='R':
                if players_direction == 'L':
                    for i in range(0,players_distance):
                        #print i 
                        if y-i <= 0:
                            print 'invalid distance'
                            return False
                        if brd.brd[x][y-i] != 0 and i != 0:
                            print 'invalid distance' 
                            return False
                    return [vehicle,'L',players_distance]
                    print "moving left"
                else:
                    for i in range(0,players_distance+1):
                        #print i
                        #print y+(vehicle.length-1)+i
                        if y+(vehicle.length-1)+i > 5:
                            print 'invalid distance'
                            return False
                            #print brd.brd[x][y+(vehicle.length-1)+i]
                        if brd.brd[x][y+(vehicle.length-1)+i] != 0 and i != 0:
                            print 'invalid distance'
                            return False
                    print "moving right"
                    return [vehicle,'R',players_distance]
            else:
                print "Not a valid move!!"
                return False
    return False


def read_player_input (brd):
    player_input = raw_input("Enter Move(or q): ")
    return player_input.upper()


def update_board (brd,move):
    move[0].move(move[1],move[2])
    brd.place_in_board()

    # FIX ME!
    return brd


def print_board (brd):
    
    for i in brd.brd:
        row = ''
        for j in i: 
            if j == 0:
                j = '.'
            row = row + j + '  '
        print row
    # l=len(brd.brd)
    # for i in range(l):
    #     row = []
    #     for j in range(l):
    #         row.append(brd.brd[j][i])
    #     print row

    # FIX ME!


    
def done (brd):
    for vehicle in brd.vehicles:
        if vehicle.name.upper() == 'X':
            if vehicle.position == (3,5):
                return True
            else:
                return False


# initial board:
# Board positions (1-6,1-6), directions 'R' or 'D'
#
# X @ (2,3) r
# A @ (2,4) r
# B @ (2,5) d
# C @ (3,6) r
# O @ (4,3) d
# P @ (6,4) d
class board(object):
    def __init__(self):
        self.brd = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.vehicles = []

    def add_vehicle(self,cars):
        for car in cars:
            self.vehicles.append(car)

    def place_in_board(self):
        self.brd = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        for vehicle in self.vehicles:
            x,y = vehicle.position
            #print x,y
            self.brd[x-1][y-1] = vehicle.name
            if vehicle.direction == 'D':
                for j in range(0,vehicle.length):
                    self.brd[x-1+j][y-1] = vehicle.name
            else:
                for j in range(0,vehicle.length):
                    self.brd[x-1][y-1+j] = vehicle.name
            

class vehicle(object):
    def __init__(self,name,(x,y),d,l=2):
        self.name = name
        self.position = (x,y)
        self.length = l
        self.direction = d

    def move(self,m_dir,m_dis):
        x,y = self.position
        if m_dir == 'U':
            x = x-m_dis
        elif m_dir == 'D':
            x= x+m_dis
        elif m_dir == 'L':
            y = y-m_dis
        else:
            y = y+m_dis
        self.position = (x,y)

def create_initial_level():
    brd =  board()
    X = vehicle('X',(3,2),'R',2)
    A = vehicle('A',(4,2),'R',2)
    B = vehicle('B',(5,2),'D',2)
    C = vehicle('C',(6,3),'R',2)
    O = vehicle('O',(3,4),'D',3)
    P = vehicle('P',(4,6),'D',3)
    list_of_vehicles = [X,A,B,C,O,P]
    brd.add_vehicle(list_of_vehicles)
    brd.place_in_board()
    # FIX ME!
    return brd


def main ():

    brd = create_initial_level()

    print_board(brd)
    quit = False
    while not done(brd):
        move = read_player_input(brd)
        if move == 'Q':
            quit = True
            break
        valid_move = validate_move(brd,move)
        if valid_move != False:
            brd = update_board(brd,valid_move)
        print_board(brd)
    if quit != True:
        print 'YOU WIN! (Yay...)\n'
    else:
        print 'you suck'

def main_with_input(desc):
    brd = board()
    list_of_vehicles = []
    for i in range(0,len(desc),4):
        name = desc[i]
        x = int(desc[i+2])
        y = int(desc[i+1])
        direction = desc[i+3]
        if name == 'O' or name == 'P':
            l = 3;
            list_of_vehicles.append(vehicle(name,(x,y),direction,l))
        else:
            list_of_vehicles.append(vehicle(name,(x,y),direction))
    brd.add_vehicle(list_of_vehicles)
    brd.place_in_board()
    print_board(brd)
    quit = False
    while not done(brd):
        move = read_player_input(brd)
        if move == 'Q':
            quit = True
            break
        valid_move = validate_move(brd,move)
        if valid_move != False:
            brd = update_board(brd,valid_move)
        print_board(brd)
    if quit != True:
        print 'YOU WIN! (Yay...)\n'
    else:
        print 'you suck'
        

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        sys.argv[1] = sys.argv[1].upper()
        main_with_input (sys.argv[1])
    else:
        main()
    #test = create_initial_level()
    #for i in range(len(test.vehicles)):
        #print test.vehicles[i].name
    #print_board(test.brd)