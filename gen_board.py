import random as rnd
from collections import deque
import itertools as it
import numpy as np
from operator import add
import time
import copy
from matplotlib import pyplot as plt
import cPickle as pickle

#I should probably write a readme for this shit but I aint yet so holla if you have any
#questions.

class MyBoard:
    def __init__(self):
        self.width = 6
        self.height = 6
        self.squares = [[deque() for x in range(self.width)] for y in range(self.height)]
        self.saved_squares = copy.deepcopy(self.squares)
        self.eval_dict = {
            0: self.evalMove,
            1: self.evalJump,
            2: self.evalSlide,
            3: self.evalStrike,
            4: self.evalJumpSlide,
            5: self.evalCommandSquare,
            6: self.evalDivination,
            7: self.evalSummon
            #8: self.escape
            #9: self.ransom
        }
        self.discard = [deque(), deque()]
        self.duke_pos = [[], []]
        self.bag = [deque(), deque()]
        self.viewable_board = [[0 for x in range(self.width)] for y in range(self.height)]
        self.color_dict = {
            0: "White",
            1: "Black"
        }
    
    def __repr__(self):
        board = self.viewBoard()
        return board
    #old implementation of __repr__
    '''
        square_width = 16
        board_width = self.width
        width = square_width*board_width + 7
        boardview = ''
        blank_space = '|'+' '*square_width
        blank_row = blank_space*board_width + '|\n'
        line_row = '-'*width + '\n'
        for row in self.squares:
            boardview += line_row
            boardview += blank_row*2
            for space in row:
                boardview += '|'
                if space:
                    margin = square_width - len(space.__repr__())
                    left_margin = margin/2
                    right_margin = margin - left_margin
                    boardview += ' '*left_margin + space.__repr__() + ' '*right_margin
                else:
                    boardview += ' '*square_width
            boardview += '|\n'
            boardview += blank_row*3
        boardview += line_row
        return boardview
    '''
    
    def saveState(self):
        self.saved_squares = copy.deepcopy(self.squares)
        self.saved_bag = copy.deepcopy(self.bag)
        self.saved_discard = copy.deepcopy(self.discard)
        self.saved_duke_pos = copy.deepcopy(self.duke_pos)
    
    def loadState(self):
        self.squares = copy.deepcopy(self.saved_squares)
        self.bag = copy.deepcopy(self.saved_bag)
        self.discard = copy.deepcopy(self.saved_discard)
        self.duke = copy.deepcopy(self.saved_duke_pos)
    
    def returnState(self):
        state = {
            'squares': copy.deepcopy(self.saved_squares),
            'bag': copy.deepcopy(self.saved_bag)
            #'discard': copy.deepcopy(self.saved_discard),
        }
        return state
    
    #A better visual representation of the board than old repr. Relies on accessing the
    #2-D string representations of each piece and then figuring out what each line of the
    #final representation should be by looking at all the pieces that intersect that line.
    def viewBoard(self):
        square_width = 15
        square_height = 6
        empty_piece = [' '*square_width for i in range(square_height)]
        width = square_width*self.width + 7
        line_row = '-'*width + '\n'
        board_view = ''
        #loops to build viewable_board
        for i in range(self.height):
            for j in range(self.width):
                if self.squares[i][j]:
                    piece = self.squares[i][j]
                    self.viewable_board[i][j] = piece.str_array[piece.flipped]
                    if piece.color == 0:
                        piece
                else:
                    self.viewable_board[i][j] = empty_piece
            board_view += line_row
            for k in range(square_height):
                next_line = '|'
                for j in range(self.width):
                    next_line += self.viewable_board[i][j][k] + '|'
                next_line += '\n'
                board_view += next_line
        board_view += line_row
        return board_view
    
    
    #given a position of the form [row, column], return the piece object at that location
    #or 0 if the square is empty.
    def returnPiece(self, position):
        piece = self.squares[position[0]][position[1]]
        if piece:
            return piece
        else:
            return 0
    
    #find and update the positions of both dukes. Return 1 if both are still on the board
    #or 0 if either or both are not. 
    def updateDuke(self):
        duke_exists = [[],[]]
        for i in range(self.height):
            for j in range(self.width):
                space = self.squares[i][j]
                if space:
                    if space.name == 'Duke':
                        duke_exists[space.color] = 1
                        self.duke_pos[space.color] = [i, j]
        if duke_exists[0] and duke_exists[1]:
            return 1
        else:
            return 0
    
    #Return 1 if there are open spaces next to the specified duke, 0 if not. Terminates on
    #finding an open space, so is on average faster than dukeSpaces.
    def dukeOpen(self, color):
        adjct = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        positions = [map(add, adj, self.duke_pos[color]) for adj in adjct]
        for position in positions:
            if self.isPosValid(position) and not self.returnPiece(position):
                return 1
        return 0
    
    #return open spaces next to the specified duke, if any
    def dukeSpaces(self, color):
        open_spaces = []
        adjct = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        positions = [map(add, adj, self.duke_pos[color]) for adj in adjct]
        for position in positions:
            if self.isPosValid(position) and not self.returnPiece(position):
                open_spaces.append(position)
        return open_spaces
    
    #given a position, check if it is on the board
    def isPosValid(self, position):
        if position[0] not in range(self.height):
            return 0
        if position[1] not in range(self.width):
            return 0
        return 1
    
    #given a color and a position, check if there is a peice of the same color at position
    def sameColor(self, position, color):
        tile = self.returnPiece(position)
        if tile and tile.color == color:
            return 1
        else:
            return 0    
    
    #List all the pieces currently on the board. The order of nested list comprehensions
    #in python looks weird, but there's a simple explanation for it. Feel free to ask me
    #if you haven't run into it before.
    def listPieces(self):
        return [tile for row in self.squares for tile in row if tile]
    
    #As listPieces but only lists pieces of the specified color.
    def listPiecesColor(self, color):
        return [tile for row in self.squares for tile in row if (tile and tile.color == color)]
    
    #Given a starting postion, a piece color and a move, return the move packaged as a
    #list of the form [(starting place, ending place, tile to flip)], or an empty list if
    #the move is not legal.
    def evalMove(self, start, move, color):
        step = move[:2]
        num_steps = move[2]
        position = start
        for i in range(num_steps - 1):
            position = map(add, position, step)
            if not self.isPosValid(position):
                return []
            if self.returnPiece(position):
                return []
        position = map(add, position, step)
        if not self.isPosValid(position):
            return []
        if self.sameColor(position, color):
            return []
        return [(start, position, position)]
    
    #Given a starting postion, a piece color and a jump, return the action packaged as a
    #list of the form [(starting place, ending place, tile to flip)], or an empty list if
    #the move is not legal.
    def evalJump(self, start, move, color):
        destination = map(add, start, move)
        if not self.isPosValid(destination):
            return []
        if self.sameColor(destination, color):
            return []
        return [(start, destination, destination)]
    
    #Given a starting postion, a piece color and a slide, return the possible slides
    #packaged as a list of tuples of the form (starting place, ending place, tile to flip),
    #or an empty list if there are no legal slides.
    def evalSlide(self, start, move, color):
        valid_slides = []
        position = map(add, start, move)
        while self.isPosValid(position):
            if self.sameColor(position, color):
                break
            valid_slides.append(position)
            if self.returnPiece(position):
                break
            position = map(add, position, move)
        if valid_slides:
            valid_moves = [(start, slide, slide) for slide in valid_slides]
            return valid_moves
        else:
            return []
    
    #Given a starting position, a piece color and a strike, return a strike move packaged
    #as a list of the form [('Strike', target, tile to flip)] if the strike is valid, or
    #an empty list if it is not.
    def evalStrike(self, start, move, color):
        position = map(add, start, move)
        if (self.isPosValid(position)) and (not self.sameColor(position, color)):
            target = self.returnPiece(position)
            if target:
                return [('Strike', position, start)]
        return []
    
    #Given a starting postion, a piece color and a jump slide, return the possible slides
    #packaged as a list of tuples of the form (starting place, ending place, tile to flip),
    #or an empty list if there are no legal jump slides.
    def evalJumpSlide(self, start, move, color):
        valid_slides = []
        first_position = map(add, start, move)
        if self.isPosValid(first_position) and not self.sameColor(first_position, color):
            valid_slides.append(first_position)
        position = map(add, first_position, move)
        while self.isPosValid(position):
            if self.sameColor(position, color):
                break
            valid_slides.append(position)
            if self.returnPiece(position):
                break
            position = map(add, position, move)
        if valid_slides:
            valid_moves = [(start, slide, slide) for slide in valid_slides]
            return valid_moves
        else:
            return []
    
    #Given a list of command squares, return a list of all possible command square moves
    #each packaged as a tuple of the form (tile to move, place to move it, tile to flip).
    #If there are no valid command square moves, return an empty list.
    def evalCommandSquare(self, start, move, color):
        command_squares = zip(*[iter(move)] * 2)   #lol wat
        squares = [map(add, square, start) for square in command_squares]
        allies = []
        destinations = []
        valid_moves = []
        for square in squares:
            if self.isPosValid(square):
                if self.sameColor(square, color):
                    allies.append(list(square))
                else:
                    destinations.append(list(square))
        valid_moves = [(ally, destination, start) for ally in allies for destination in destinations]
        return valid_moves
    
    #Given a divination move, return a list of the form [('Diviniation', start)] if it is
    #possible to draw pieces, or an empty list if it is not.
    def evalDivination(self, start, move, color):
        if not self.bag[color]:
            return []
        if self.dukeOpen(color):
            return [('Divination', start)]
        return []
    
    #Given a summon move, return a list of all possible summon actions each of the form
    #(tile to summon, place to summon it to, tile to flip), or an empty list if thre are
    #possible summon actions.
    def evalSummon(self, start, move, color):
        open_spaces = self.dukeSpaces(color)
        if open_spaces:
            return [(start, space, self.duke_pos[color]) for space in open_spaces]
        else:
            return []
    
    #def evalEscape(self, start, move, color):
    
    #def evalRansom(self, start, move, color):
    
    
    #Determine if the duke of the specified side is in guard or not.
    def inGuard(self, color):
        enemy_moves = self.moveTable(not color)
        for move in enemy_moves:
            if move[0] == 'Draw':
                continue
            if move[0] == 'Diviniation':
                continue
            target = self.returnPiece(move[1])
            if target and target.name == 'Duke' and target.color == color:
                #print move
                return 1
        return 0
    
    def leaveGuard(self, color):
        self.saveState()
        possible_moves = self.moveTable(color)
        rnd.shuffle(possible_moves)
        for move in possible_moves:
            self.makeMove(move, color)
            self.updateDuke()
            if not self.inGuard(color):
                return
            else:
                self.loadState()
                self.updateDuke()
        return -1
            
    
    def makeMove(self, move, color):
        if move[0] == 'Draw':
            draw_spaces = move[1]
            rnd.shuffle(draw_spaces)
            space = draw_spaces.pop()
            self.squares[space[0]][space[1]] = self.bag[color].pop()
            return
        if move[0] == 'Strike':
            end = move[1]
            target = self.returnPiece(end)
            start = move[2]
            originator = self.returnPiece(start)
            self.discard[target.color].append(target)
            self.squares[end[0]][end[1]] = 0
            originator.flipped = not originator.flipped
            return
        if move[0] == 'Divination':
            open_spaces = self.dukeSpaces(color)
            rnd.shuffle(open_spaces)
            space = open_spaces.pop()
            available_pieces = [self.bag[color].pop() for i in range(3) if self.bag[color]]
            rnd.shuffle(available_pieces)
            piece = available_pieces.pop()
            self.squares[space[0]][space[1]] = piece
            self.bag[color].extend(available_pieces)
            rnd.shuffle(self.bag[color])
            return
        #print "move is: ", rand_move
        start, end, flip = move
        start_tile = self.returnPiece(start)
        end_tile = self.returnPiece(end)
        if end_tile:
            self.discard[end_tile.color].append(end_tile)
        self.squares[end[0]][end[1]] = start_tile
        self.squares[start[0]][start[1]] = 0
        self.squares[flip[0]][flip[1]].flipped = not self.squares[flip[0]][flip[1]].flipped
    
    #Given a tile and a location, return a list of all the moves that tile can make
    #repesented as tuples, or an empty list if there are none.
    def ennumerateActions(self, tile, row, column):
        action_list = tile.actions[tile.flipped]
        start = [row, column]
        valid_moves = []
        for action in action_list:
            valid_moves.extend(self.eval_dict[action[0]](start, action[1:], tile.color))
        return valid_moves
    
    #Create a table of all possible moves for the specified side as a list of move tuples.
    def moveTable(self, color):
        move_list = []
        for i in range(self.height):
            for j in range(self.width):
                tile = self.squares[i][j]
                if tile and tile.color == color:
                    #print "finding actions for", tile.name
                    actions_list = self.ennumerateActions(tile, i, j)
                    if actions_list:
                        move_list.extend(actions_list)
        draw_spaces = self.dukeSpaces(color)
        if draw_spaces and self.bag[color]:
            move_list.extend([('Draw', draw_spaces)]) 
        return move_list
    
    #Pick a move at random out of all possible moves for the specified side and make it.
    def randomMove(self, color):
        #global iteration
        #if self.inGuard(color):
        #    print "I'm in guard!", color, iteration
        move_table = self.moveTable(color)
        if not move_table:
            #print self.color_dict[color], " has made a stupid and has no more moves."
            #print self
            #raw_input("press enter to continue")
            return -1
        self.saveState()
        rnd.shuffle(move_table)
        for move in move_table:
            self.makeMove(move, color)
            if self.inGuard(color):
                self.loadState()
                continue
            return 0
        #print self.color_dict[color], " cannot move without going into guard."
        #print self
        #raw_input("press enter to continue")
        return -1
                
    
    #Make random moves, alternating sides, until either duke is captured. Keeps track of
    #how many total moves are made.
    def moveRandomly(self, saved = 0, printed = 0, delay = 0.75):
        turn = 0
        global iteration
        iteration = 0
        if saved == 1:
            state_list = []
        success = 0
        while (len(self.listPiecesColor(turn)) > 0) and (iteration < 1000):
            error1 = error2 = 0
            if self.inGuard(turn):
                error1 = self.leaveGuard(turn)
            else:
                error2 = self.randomMove(turn)
            if error1:
                #print self.color_dict[turn], " is in checkmate!. ", iteration
                #print self
                #raw_input("press enter to continue")
                success = 1
                break
            if error2:
                #print self.color_dict[turn], " cannot make a move, and has lost.", iteration
                #print self
                #raw_input("press enter to continue")
                success = 1
                break
            turn = not turn
            iteration += 1
            if printed:
                print iteration
                print self
                time.sleep(delay)
            if saved == 1:
                state_list.append(self.returnState())
            if not self.updateDuke():
                print "a duke has gone missing ", iteration
                return iteration
        #the game has ended, if normally then success = 1
        if saved == 1:
            if success == 1:
                return state_list
            #print iteration, len(self.listPiecesColor(turn))
            return False
        return iteration

class Piece:
    def __init__(self, name, color):
        self.color = color
        self.name = name
        self.actions = [[],[]]
        self.flipped = 0
        self.str_array = [deque(), deque()]
    
    def __repr__(self):
        if self.color:
            rep = 'Black_'+self.name
        else:
            rep = 'White_'+self.name
        return rep


#given a black and white bag of peices, pick the first three, which are determined by the
#peice_moves.txt file, from each bag and place them on the board in starting positions at
#random.
def setupBoard():
    white_bag, black_bag = setupBags()
    board = MyBoard()
    white_duke = [0, rnd.randint(0,1)+2]
    black_duke = [5, rnd.randint(0,1)+2]
    board.duke_pos[0] = white_duke
    board.duke_pos[1] = black_duke
    board.squares[0][white_duke[1]] = white_bag.popleft()
    board.squares[5][black_duke[1]] = black_bag.popleft()

    wh_ftmn_strt = [[0, 1], [0, -1], [1, 0]]
    bl_ftmn_strt = [[0, 1], [0, -1], [-1, 0]]
    rnd.shuffle(wh_ftmn_strt)
    rnd.shuffle(bl_ftmn_strt)
    wfootman1 = map(add, wh_ftmn_strt.pop(), white_duke)
    wfootman2 = map(add, wh_ftmn_strt.pop(), white_duke)
    bfootman1 = map(add, bl_ftmn_strt.pop(), black_duke)
    bfootman2 = map(add, bl_ftmn_strt.pop(), black_duke)
    board.squares[wfootman1[0]][wfootman1[1]] = white_bag.popleft()
    board.squares[wfootman2[0]][wfootman2[1]] = white_bag.popleft()
    board.squares[bfootman1[0]][bfootman1[1]] = black_bag.popleft()
    board.squares[bfootman2[0]][bfootman2[1]] = black_bag.popleft()
    
    rnd.shuffle(white_bag)
    rnd.shuffle(black_bag)
    board.bag[0] = white_bag
    board.bag[1] = black_bag

    return board
    
def setupBags():
    with open('piece_names.txt') as infile:
        names = [line.strip() for line in infile]

    white_bag = deque([])
    black_bag = deque([])
    flipped = 0
    with open('piece_moves.txt') as infile:
        for line in infile:
            stripped = line.strip()
            if stripped in names:
                white_bag.append(Piece(stripped, 0))
                black_bag.append(Piece(stripped, 1))
                flipped = 0
                continue
            
            if stripped == 'FLIP':
                flipped = 1
                continue
            
            ints = [int(item) for item in stripped.split()]
            move = ints
            black_move = [move[0]]
            black_move.extend([-coord for coord in move[1:3]])
            if len(move) > 3:
                black_move.append(move[3])
            
            white_bag[-1].actions[flipped].append(move)
            black_bag[-1].actions[flipped].append(black_move)

    flipped = 0
    with open('piece_strings.txt') as infile:
        for line in infile:
            stripped = line.strip()
            line = line.rstrip('\n')
            if stripped in names:
                white_pieces = [piece for piece in white_bag if piece.name == stripped]
                black_pieces = [piece for piece in black_bag if piece.name == stripped]
                flipped = 0
                continue
            
            if stripped == 'FLIP':
                flipped = 1
                continue
            
            for piece in white_pieces:
                piece.str_array[flipped].append(line)
            for piece in black_pieces:
                piece.str_array[flipped].appendleft(line[::-1])
    
    square_width = 15
    for white, black in zip(white_bag, black_bag):
        white.str_array[0] = deque(reversed(white.str_array[0]))
        white.str_array[1] = deque(reversed(white.str_array[1]))
        black.str_array[0] = deque(reversed(white.str_array[0]))
        black.str_array[1] = deque(reversed(white.str_array[1]))
        white_name, black_name = 'Wh_' + white.name, 'Bl_' + black.name
        margin = square_width - len(white_name)
        left_margin = margin/2
        right_margin = margin - left_margin
        white_string = ' '*left_margin + white_name + ' '*right_margin
        black_string = ' '*left_margin + black_name + ' '*right_margin
        white.str_array[0].appendleft(white_string)
        white.str_array[1].appendleft(white_string)
        black.str_array[0].append(black_string)
        black.str_array[1].append(black_string)
    
    return white_bag, black_bag

def timeGames(num_games):
    board = setupBoard()
    init_board = copy.deepcopy(board)
    iteration = 0
    num_turns = 0
    length_list = []
    a = time.time()
    for i in range(num_games):
        board = copy.deepcopy(init_board)
        length_list.append(board.moveRandomly())
    b = time.time()
    length_list = [game for game in length_list if game < 1000]
    diff = num_games - len(length_list)
    valid = len(length_list)
    print valid, " out of ", num_games, " games took: ", b - a, '\nAverage number of turns per game: ', round(float(sum(length_list))/valid)
    return length_list

def saveGame(filename = 'saved_game.txt', write_mode = 'w'):
    board = setupBoard()
    states = board.moveRandomly(saved = 1)
    print len(states)
    if states:
        with open(filename, write_mode) as f:
            pickle.dump(states, f)
        print "Game saved."
    

def plotGames(length_list):
    max_turns = max(length_list)
    histogram = [0]*(max_turns + 1)
    for length in length_list:
        print length
        histogram[length] += 1
    plt.plot(range(max_turns + 1), histogram)
    plt.show()


