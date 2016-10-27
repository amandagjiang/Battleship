#battleship_ui.py

import battleship
import tkinter
from PIL import Image,ImageTk

class BattleshipApplication:
    EMPTY = 0
    PLAYER = 1
    OPPONENT = 2
    HIT = 3
    ALREADY_SHOT = 4
    
    def __init__(self, bship, sub1, sub2, destroyer):
        self._game = battleship.Battleship()
        self._board = self._game.get_board()
        self._bship = bship
        self._sub1 = sub1
        self._sub2 = sub2
        self._destroyer = destroyer
        self._root_window = tkinter.Tk()
        self._player_turn = True
        
        self._canvas = tkinter.Canvas(
            master = self._root_window, width = 600, height = 600,
            background = 'lightblue')
        self._canvas.bind('<Configure>',self._on_canvas_resized)
        self._canvas.grid(row=1,column=0,
                          sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        battleship_label = tkinter.Label(
            master = self._root_window, text = "Welcome to the game of Battleship!", 
            font = ('Monaco', 20), background = "#0C89FF")
        battleship_label.grid(row = 2, column = 0, sticky = tkinter.N+
                              tkinter.S + tkinter.E + tkinter.W)
        self._resized = False
        self._splash_list = []
        self._fire_list = []
        
        #Battleship images       
        self._battleship = tkinter.PhotoImage(file = 'battleship.gif')
        self._battleship_rotated = tkinter.PhotoImage(file = 'battleship_rotated.png')
        self._sub = tkinter.PhotoImage(file = 'sub.png')
        self._sub_rotated = tkinter.PhotoImage(file = 'sub_rotated.png')
        self._dest = tkinter.PhotoImage(file = 'destroyer.png')
        self._dest_rotated = tkinter.PhotoImage(file = 'destroyer_rotated.png')
        self._splash = tkinter.PhotoImage(file = 'splash.png')
        self._fire = tkinter.PhotoImage(file = 'fire.png')
        self._ocean = tkinter.PhotoImage(file = 'ocean.png')
        
        self._canvas.bind('<Button-1>',self._player_move)

    def start(self):
        self._game.place_ship(self._game._translate_points(self._bship), False)
        self._game.place_ship(self._game._translate_points(self._destroyer), False)
        self._game.place_ship(self._game._translate_points(self._sub1), False)
        self._game.place_ship(self._game._translate_points(self._sub2), False)
        self._game._computer_rand_battleship()
        self._game._computer_rand_destroyer()
        self._game._computer_rand_submarine()
        self._game._computer_rand_submarine()
        self._root_window.mainloop()
        

    def _draw_rows(self,row_height) -> None:
        incr_row = row_height
        for _row in range(8):
            self._canvas.create_line(0,incr_row,self._canvas.winfo_width(),incr_row, fill='black')
            incr_row += row_height

    def _draw_cols(self, col_width) -> None:
        incr_col = col_width
        for _col in range(8):
            self._canvas.create_line(incr_col, 0, incr_col,self._canvas.winfo_height(), fill ='black')
            incr_col += col_width

    def _draw_letters(self, row_height,col_width) -> None:
        start,end = col_width, col_width*2
        letters = 'ABCDEFGH'
        for col in range(8):
            self._canvas.create_text((start+end)/2, row_height/2,text=letters[col],font = ('Monaco',40))
            start += col_width
            end += col_width

    def _draw_numbers(self, row_height,col_width) -> None:
        start,end = row_height, row_height*2
        numbers = '12345678'
        for row in range(8):
            self._canvas.create_text(col_width/2,(start+end)/2,text=numbers[row],font = ('Monaco',40))
            start += row_height
            end += row_height
            
    def _coordinates_to_square(self, x,y, col_width):
        col,row = int(x//col_width), int(y//col_width)
        return (row-1,col-1)
                
    def _convert_coordinates(self,coords):
        '''Converts a coordinate in format 'A1' to (1,1)'''
        return (int(coords[1]),self._game.letter_to_number(coords[0])+1)

    def _place_ship(self, coordinates, ship, row_height, col_width):
        '''Places a battleship on the board'''
        start_point = coordinates.split(',')[0]
        end_point = coordinates.split(',')[1]
        start = self._convert_coordinates(start_point)
        end = self._convert_coordinates(end_point)
        self._draw_ship(ship, start,end, row_height, col_width)
            
    def _draw_ship(self,ship, start,end, row_height, col_width): 
        '''Receives coordinates 'A5,A6' and type of ship to draw on the board'''   
        if start[0] == end[0]:
            self._canvas.create_image(start[1]*col_width,start[0]*row_height,
                                      image = eval('self._' + ship), anchor='nw')
        else:
            self._canvas.create_image(start[1]*col_width,start[0]*row_height,
                                      image = eval('self._' + ship + '_rotated'), anchor='nw')
            
    def _shot_result(self,coordinates,type,col_width):
        '''Places either fire or a splash on the board after a shot'''
        y,x = coordinates
        self._canvas.create_image((x+1)*col_width + col_width/2,(y+1)*col_width + col_width/2,image = eval('self._' + type))
            
    def _resize_images(self, height):
        if not self._resized:
            self._battleship = self._battleship.subsample(int(4/600 * height))
            self._battleship_rotated = self._battleship_rotated.subsample(int(4/600 * height))
            self._sub = self._sub.subsample(int(4/600*height))
            self._sub_rotated = self._sub_rotated.subsample(int(4/600*height))
            self._dest = self._dest.subsample(int(7/600*height))
            self._dest_rotated = self._dest_rotated.subsample(int(7/600*height))
            self._splash = self._splash.subsample(int(12/600*height))
            self._fire = self._fire.subsample(int(6/600*height))
            self._resized = True
            
    def _draw_board(self):
        self._resize_images(self._canvas.winfo_height())
        row_height = self._canvas.winfo_height()/9
        col_width = self._canvas.winfo_width()/9
        self._canvas.create_image(100,300,image = self._ocean)
        
        self._draw_rows(row_height)
        self._draw_cols(col_width)
        self._draw_letters(row_height,col_width)
        self._draw_numbers(row_height,col_width)
        self._place_ship(self._bship,'battleship',row_height,col_width)
        self._place_ship(self._sub1,'sub', row_height,col_width)
        self._place_ship(self._sub2,'sub',row_height, col_width)
        self._place_ship(self._destroyer,'dest',row_height,col_width)
        
        if len(self._splash_list) != 0:
            for splash in self._splash_list:
                self._shot_result(splash,'splash',col_width)
        
        if len(self._fire_list) != 0:
            for fire in self._fire_list:
                self._shot_result(fire,'fire',col_width)
            
    def _on_canvas_resized(self,event:tkinter.Event) -> None:        
        self._canvas.delete(tkinter.ALL)
        self._draw_board()
        
    def _player_move(self,event:tkinter.Event) -> None:
        if all([self._game.lives > 0, self._game.opponent_lives > 0, self._player_turn]):
            valid_move = False
            col_width = self._canvas.winfo_width()/9
            click_point = event.x, event.y
            if event.x > col_width and event.y > col_width:
                row, col = self._coordinates_to_square(event.x,event.y,col_width)
                if self._game._board[row][col] == self._game.OPPONENT:
                    self._fire_list.append((row,col))
                    self._game.move(row,col) 
                    self._hit_message(False)
                    self._game._check_targets()
                    self._player_turn = False
                    valid_move = True
                    
                elif self._game._board[row][col] == self.EMPTY:
                    self._splash_list.append((row,col))
                    self._game.move(row,col) 
                    self._game._check_targets()
                    self._miss_message(False)
                    self._player_turn = False
                    valid_move = True
                self._draw_board()       
                
                if self._check_winner():
                    self._winner_message(self._game.get_winner())
                    valid_move = False
                    
                if valid_move:
                    self._canvas.after(1500, self._computer_move)
            
    def _check_winner(self):
        return any([self._game.lives == 0, self._game.opponent_lives == 0])
            
    def _computer_move(self):
        hit, comp_row, comp_col = self._game.random_comp_move()
        if hit:
            self._fire_list.append((comp_row,comp_col))
            self._hit_message(True)
        else:
            self._splash_list.append((comp_row,comp_col))
            self._miss_message(True)
        if self._check_winner():
            self._winner_message(self._game.get_winner())
        self._draw_board()
        self._player_turn = True
            
    def _hit_message(self, computer_move):
        message = "The computer hit you!" if computer_move else "You hit the computer!"
        self._display_message(message)
        
    def _miss_message(self, computer_move):
        message = "The computer missed!" if computer_move else "You missed!"
        self._display_message(message)
    
    def _winner_message(self,winner):
        message = "Player wins!" if winner == self.PLAYER else "Computer wins!"
        self._display_message(message)
                
    def _display_message(self,message):
        battleship_label = tkinter.Label(
            master = self._root_window, text = message, 
            font = ('Monaco', 20), background = "#0C89FF")
        battleship_label.grid(row = 2, column = 0, sticky = tkinter.N+
                              tkinter.S + tkinter.E + tkinter.W)
        
if __name__ == '__main__':
    battleship = BattleshipApplication('H5,H8','C4,E4','F1,F3','B7,B8')
    battleship.start()
    
        
