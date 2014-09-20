#!/usr/bin/env python

#
# Game Programming, Level 1 Project
#
# RUSH HOUR
#
# A simple puzzle game, based on the physical game of the same name 
# by Binary Arts Corp
#
#from rush_object import vehicle


# fail somewhat gracefully
from graphics import *




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
                    for i in range(0,players_distance+1):
                        #print i 
                        if x-i < 0:
                            print 'invalid distance'
                            return False
                        if brd.brd[x-i][y] != 0 and i != 0:
                            print 'invalid distance' 
                            return False
                    print "moving up"
                    return [vehicle,'U',players_distance]
                else:
                    for i in range(0,players_distance):
                        #print i
                        #print y+(vehicle.length-1)+i
                        
                        if x+(vehicle.length-1)+i > 5:
                            print 'invalid distance'
                            return False
                           # print brd.brd[x+(vehicle.length-1)+i][y]
                        if brd.brd[x+(vehicle.length-1)+i][y] != 0 and i != 0:
                            print 'invalid distance'
                            return False
                    print "moving down" 
                    return [vehicle,'D',players_distance]
            elif  (players_direction == 'L' or players_direction == 'R') and vehicle.direction =='R':
                if players_direction == 'L':
                    for i in range(0,players_distance+1):
                        #print i 
                        if y-i < 0:
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


def read_player_input (win,brd):
    # return player_input.upper()
    vehicle_point = win.getMouse()
    car_selected = select_car(vehicle_point,brd)
    if car_selected == 'q':
        move = False
        return move
    move_point = win.getMouse()
    tile_selected = select_tile(move_point,brd)
    if tile_selected == 'q':
        move = False
        return move
    if tile_selected == False or car_selected == False:
        print 'Your selection was invalide'
        move = ''
        return move
    move = convert_move(car_selected,tile_selected)
    return move

def select_car(pt,brd):
    car_selected = ''
    x,y = (pt.getX(),pt.getY())
    if y > 600:
        return 'q'
    for vehicle in brd.vehicles:
        p1 = vehicle.rectangle.p1
        p2 = vehicle.rectangle.p2
        x1,y1 = (p1.getX(),p1.getY())
        x2,y2 = (p2.getX(),p2.getY())
        if x <= x2 and x >= x1 and y <= y2 and y >= y1:
            vehicle.rectangle.setFill('peachpuff')
            return vehicle
    return False  

def select_tile(pt,brd):
    tile_selected = ''
    x,y = (pt.getX(),pt.getY())
    if y > 600:
        return 'q'
    for tile in brd.grid:
        p1 = tile.p1
        p2 = tile.p2
        x1,y1 = (p1.getX(),p1.getY())
        x2,y2 = (p2.getX(),p2.getY())
        if x <= x2 and x >= x1 and y <= y2 and y >= y1:
            tile.setFill('peachpuff')
            return tile
    return False

def convert_move(car,tile):
    p1 = tile.p1
    cp1 = car.rectangle.p1
    xt1,yt1 = (p1.getX(),p1.getY())
    xc1,yc1 = (cp1.getX(),cp1.getY())
    if xt1 > xc1:
        d = 'R'
        dis = (xt1-xc1)/100-car.length+1 
    elif xt1<xc1:
        d = 'L'
        dis = (xc1-xt1)/100 
    elif yt1 > yc1:
        d = 'D'
        dis = (yt1-yc1)/100-car.length+1 
    else:
        d = 'U'
        dis = (yc1-yt1)/100 

    e = str(dis)

    move = car.name + d + e
    print move
    return move

def update_board (brd,move):
    move[0].move(move[1],move[2])
    brd.place_in_board()

    # FIX ME!
    return brd


def print_board (win, brd):
    ptclear1 = Point(0,0)
    ptclear2 = Point(600,600)
    clearbrd = Rectangle(ptclear1,ptclear2)
    clearbrd.setOutline('white')
    clearbrd.setFill('white')
    clearbrd.draw(win)
    pt1quit = Point(0,600)
    pt2quit = Point(600,700)
    quit = Rectangle(pt1quit,pt2quit)
    quit.setFill('red')
    quit.draw(win)
    quit_txt = Text(Point(win.getWidth()/2,610),'QUIT')
    quit_txt.draw(win)
    grid = [];
    for i in range(100, 700, 100):
        for j in range(100, 700, 100):
            pt1 = Point(i-95,j-95)
            pt2 = Point(i-5, j-5)
            rectangle = Rectangle(pt1, pt2)
            rectangle.draw(win)
            grid.append(rectangle)
    for vehicle in brd.vehicles:
        x,y = vehicle.position
        l = vehicle.length
        if vehicle.direction == 'R':
            pt1 = Point(y*100-95,x*100-95)
            pt2 = Point((y+l-1)*100-5,x*100-5)    
        else:
            pt1 = Point(y*100-95,x*100-95)
            pt2 = Point(y*100-5,(x+l-1)*100-5)
        rectangle = Rectangle(pt1,pt2)
        if vehicle.name == 'X':
            rectangle.setFill('cyan')
        else:
            rectangle.setFill('blue')
        vehicle.rectangle = rectangle
        rectangle.draw(win)
    brd.grid = grid 
    

    # for i in brd.brd:
    #     row = ''
    #     for j in i: 
    #         if j == 0:
    #             j = '.'
    #         row = row + j + '  '
    #     print row

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
        self.grid = []

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
        self.rectangle = ''

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
    win = GraphWin('RUSH HOUR',600,620)
    brd = create_initial_level()

    print_board(win,brd)
    quit = False
    while not done(brd):
        move = read_player_input(win,brd)
        if move == False:
            quit = True
            break
        if move != '':
            valid_move = validate_move(brd,move)
            if valid_move != False:
                brd = update_board(brd,valid_move)
        print_board(win, brd)
    if quit != True:
        print 'YOU WIN! (Yay...)\n'
    else:
        print 'you suck'

def main_with_input(desc):
    win = GraphWin('Rush HOUR',600,600)
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
    print_board(win,brd)
    quit = False
    while not done(brd):
        move = read_player_input(win,brd)
        if move == False:
            quit = True
            break
        if move != '':
            valid_move = validate_move(brd,move)
            if valid_move != False:
                brd = update_board(brd,valid_move)
        print_board(win, brd)
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