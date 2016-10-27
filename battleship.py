#battleship.py

import string
import random

class BattleshipError(Exception):
    def __init__(self,message=None):
        Exception.__init__(self,message)

class Battleship:
    EMPTY = 0
    PLAYER = 1
    OPPONENT = 2
    HIT = 3
    ALREADY_SHOT = 4
    
    def __init__(self):
        self._board = self._create_board()
        self.opponent_lives = 12
        self.lives = 12
        self.computer_targets = []
    
    def print_board(self):
        row_count = 1
        print('  A B C D E F G H')
        for row in self._board:
            print('{} '.format(row_count), sep = '', end='')
            row_count += 1
            for col in row:
                if col == self.EMPTY:
                    print('. ',sep='',end='')
                elif col == self.OPPONENT:
                    print('. ', sep='',end='')
                elif col == self.PLAYER:
                    print('O ',sep= '',end='')
                elif col == self.HIT:
                    print('X ', sep ='',end='')
                elif col == self.ALREADY_SHOT:
                    print('* ',sep='',end='')
            print()
        print()

    def get_board(self):
        return self._board
         
    def place_ship(self,points, hide = False):
        if self._check_ship(points):
            start_row, start_col, end_row, end_col = points
            if start_row == end_row and start_col < end_col:
                while start_col <= end_col:
                    self._board[start_row][start_col] = 1 if hide == False else self.OPPONENT
                    start_col += 1
            elif start_row == end_row and start_col > end_col:
                while start_col >= end_col:
                    self._board[start_row][start_col] = 1 if hide == False else self.OPPONENT
                    start_col -= 1
            elif start_col == end_col and start_row < end_row:
                while start_row <= end_row:
                    self._board[start_row][start_col] = 1 if hide == False else self.OPPONENT
                    start_row += 1
            elif start_col == end_col and start_row > end_row:
                while start_row >= end_row:
                    self._board[start_row][start_col] = 1 if hide == False else self.OPPONENT
                    start_row -= 1
        else:
            raise BattleshipError('Cannot place battleship at this location')
        
    def get_winner(self):
        return self.PLAYER if self.opponent_lives == 0 else self.OPPONENT
    
    def letter_to_number(self,letter):
        intab = 'ABCDEFGH'
        outtab = '01234567'
        table = str.maketrans(intab,outtab)
        return int(letter.translate(table)) 
            
    def random_comp_move(self):
        if len(self.computer_targets) == 0: #Hunt Mode
            while True:
                row, col = int(random.random()*8), int(random.random()*8) 
                if all((self._board[row][col] != self.HIT,self._board[row][col] != self.OPPONENT,self._board[row][col] != self.ALREADY_SHOT)):
                    if self._board[row][col] == self.PLAYER:
                        self._board[row][col] = self.HIT #
                        self._add_surrounding_targets(row, col)
                        self.lives -= 1
                        return (True,row,col)
                    else:
                        break
        else: #Target Mode
            while True:
                target = int(random.random() * len(self.computer_targets))  
                row, col = self.computer_targets[target]
                self.computer_targets.remove((row,col))
                if self._board[row][col]  != self.HIT and self._board[row][col] != self.ALREADY_SHOT:
                    break
            if self._board[row][col] == self.PLAYER:
                self._board[row][col] = self.HIT #
                self._add_surrounding_targets(row,col)
                self.lives -= 1
                return (True,row,col)           
        self._board[row][col] = self.ALREADY_SHOT
        return (False,row,col)
        
    def _add_surrounding_targets(self, row,col):
        nesw = [(row-1,col), (row,col+1), (row+1,col), (row,col-1)]
        for point in nesw:
            row,col = point
            if all((row >= 0,row < 8,col >= 0,col < 8)):
                if self._board[row][col] == 0 or self._board[row][col] == self.PLAYER:
                    self.computer_targets.append(point)  
    
    def _translate_points(self,start_end):   
        start = start_end.strip().split(',')[0]
        start_row, start_col = int(start[1])-1, self.letter_to_number(start[0])
        end = start_end.strip().split(',')[1]
        end_row, end_col = int(end[1])-1, self.letter_to_number(end[0])
        return (start_row,start_col,end_row,end_col)   
        
    def _random_points(self,length):
        row_or_col, subtract_or_add = int(random.random() * 2), int(random.random()*2)
        same_number, start = int(random.random() * 8), int(random.random()*8)    
        if length == 4:   
            end = 3 + start if (subtract_or_add == 0 or start - 3 < 0) else start - 3
        elif length == 3: 
            end = 2 + start if (subtract_or_add == 0 or start - 2 < 0)  else start - 2
        elif length == 2:
            end = 1 + start if (subtract_or_add == 0 or start - 1 < 0) else start - 1
        points = (same_number,start,same_number,end) if row_or_col == 0 else (start,same_number,end,same_number)   
        return points if all(num < 8 for num in points) else self._random_points(length)       
         
    def _check_ship(self, points):
        start_row, start_col, end_row, end_col = points
        if start_row == end_row and start_col < end_col:
            while start_col <= end_col:
                if self._board[start_row][start_col] != 0:
                    return False
                start_col += 1  
        elif start_row == end_row and start_col > end_col:
            while start_col >= end_col:
                if self._board[start_row][start_col] != 0:
                    return False
                start_col -= 1
        elif start_col == end_col and start_row < end_row: 
            while start_row <= end_row:
                if self._board[start_row][start_col] != 0:
                    return False
                start_row += 1
        else:
            while start_row >= end_row:
                if self._board[start_row][start_col] != 0:
                    return False
                start_row -= 1
        return True
    
    def _check_targets(self):
        for point in self.computer_targets:
            row,col = point
            if self._board[row][col] == self.ALREADY_SHOT:
                self.computer_targets.remove(point)
        
    def _create_board(self):
        board = []
        for _row in range(0,8):
            board.append([0,0,0,0,0,0,0,0])
        return board
    
    def _computer_rand_battleship(self):
        while True:
            points = self._random_points(4)
            if self._check_ship(points):
                self.place_ship(points, True)
                break
    
    def _computer_rand_submarine(self): 
        while True:
            points = self._random_points(3)
            if self._check_ship(points):
                self.place_ship(points, True)
                break
            
    def _computer_rand_destroyer(self):
        while True:
            points = self._random_points(2)
            if self._check_ship(points):
                self.place_ship(points, True)
                break
        
    def convert_coordinate(self,point):
        col, row = point.strip()
        row = int(row)-1
        col = self.letter_to_number(col)
        return (row,col)
     
    # Battleship Console Functions
    
    def move(self,row, col):
        if self._board[row][col] == self.OPPONENT:
            self._board[row][col] = self.HIT
            self.opponent_lives -= 1
        elif self._board[row][col] == self.EMPTY:
            self._board[row][col] = self.ALREADY_SHOT
        elif self._board[row][col] == self.HIT or self._board[row][col] == self.ALREADY_SHOT:
            raise BattleshipError
        elif self._board[row][col] == self.PLAYER:
            raise BattleshipError
    '''        
    def run(self):
        print('Welcome to the game of Battleship!')
        self.print_board()
        print()
        while True:
            battleship = input('Where would you like to place your battleship? (Length 4): ')
            try: 
                self.place_ship(self._translate_points(battleship))
                self.print_board()
                break
            except:
                print('Try again!')
                
        while True:
            submarine = input('Where would you like to place your submarine? (Length 3): ')
            try: 
                self.place_ship(self._translate_points(submarine))
                self.print_board()
                break
            except:
                print('Try again!')
                
        while True:
            destroyer = input('Where would you like to place your other submarine? (Length 3): ')
            try: 
                self.place_ship(self._translate_points(destroyer))
                self.print_board()
                break
            except:
                print('Try again!')
                
        while True:
            destroyer = input('Where would you like to place your last destroyer? (Length 2): ')
            try: 
                self.place_ship(self._translate_points(destroyer))
                self.print_board()
                break
            except:
                print('Try again!')
                
        self._computer_rand_battleship()
        self._computer_rand_destroyer()
        self._computer_rand_submarine()
        self._computer_rand_submarine()
        
        self.print_board()     
        while self.opponent_lives > 0 and self.lives > 0:
            while True:
                point = input('Enter a target: ')
                try:
                    row, col = self.convert_coordinate(point)
                    self.move(row,col)
                    break
                except BattleshipError:
                    pass   
            self.random_comp_move() 
            print()
            self.print_board()   
            print('PLAYER ', self.lives)
            print('COMPUTER ', self.opponent_lives)         
            
        self.print_board()
        
        if self.opponent_lives == 0:
            print('You win!')
        else:
            print('You lost!')
    '''
