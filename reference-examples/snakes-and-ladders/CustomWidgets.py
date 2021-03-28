from tkinter import *
from tkinter import ttk
import math
import random


class StartupWidget:
    """
    Creates the startup menu
    """
    def __init__(self, a_frame):
        self.frame = a_frame
        # styles for the start menu
        style = ttk.Style()
        style.configure('title.TLabel', font=('Helvetica', 28))
        style.configure('option.TButton', color='blue', font=('Helvetica',14))
        style.configure('option.TLabel', font=('Helvetica', 14))
        self.init_labels()

        self.player_selector = Spinbox(self.frame, from_=2, to=14, insertborderwidth=40, increment=1, bd=2, state='readonly', justify=CENTER)
        self.player_selector.invoke('buttondown')  # ensures a value displays on start 
        self.player_selector.grid(column=3, columnspan=2, row=1, sticky=W)

        self.capture_value = BooleanVar(value=True)  # tkinter widgets want to use these wrapper objects 
        self.capture_selector = Checkbutton(self.frame, variable=self.capture_value)
        self.capture_selector.grid(column=3, columnspan=2, row=2, sticky=(N,S,W))

        self.exact_value = BooleanVar(value=True)
        self.exact_selector = Checkbutton(self.frame, variable=self.exact_value)
        self.exact_selector.grid(column=3, columnspan=2, row=3, sticky=(N,S,W))

        self.start_button = ttk.Button(self.frame, text='Start!', style='option.TButton')
        self.start_button.grid(column=1, columnspan=3,row=4, sticky=(N,S,E,W))

    def set_start_button(self, function):
        self.start_button['command'] = function

    def init_labels(self):
        title = ttk.Label(self.frame, text='Snakes and Ladders', style='title.TLabel')
        title.grid(column=0, columnspan=5)
        player_option_label = ttk.Label(self.frame, text='Players', style='option.TLabel')
        player_option_label.grid(column = 0, columnspan=2, row=1, sticky=E)
        capture_option_label = ttk.Label(self.frame, text='Capturing', style='option.TLabel')
        capture_option_label.grid(column=0, row=2, columnspan=2, sticky=E)
        exact_option_label = ttk.Label(self.frame, text='Exact to Win', style='option.TLabel')
        exact_option_label.grid(column=0, row=3, columnspan=2, sticky=E)


class DiceWidget:
    """
    Displays the dice images and the roll button
    Also logs roll results
    """
    def __init__(self, gamebrain):
        self.gamebrain = gamebrain
        self.roll_1 = PhotoImage(file="roll-1.gif")
        self.roll_2 = PhotoImage(file="roll-2.gif")
        self.roll_3 = PhotoImage(file="roll-3.gif")
        self.roll_4 = PhotoImage(file="roll-4.gif")
        self.roll_5 = PhotoImage(file="roll-5.gif")
        self.roll_6 = PhotoImage(file="roll-6.gif")
        self.roll_label = Label(self.gamebrain.control_frame, image=self.roll_1) # the dice picture label 
        self.last_roll = 0
        self.roll_label.grid()
        self.roll_button = ttk.Button(self.gamebrain.control_frame, text="Roll!", command=self.roll_button_press)
        self.roll_button.grid()
        # fill the text logs initially so there's no weird window resizing. Probably are better solutions but it works
        self.text_logs = ["--------------------------"]*13
        self.message = Message(self.gamebrain.control_frame)
        self.message.grid()
        self.log_message('--------------------------',14)



    def log_message(self, message, max_items=14):
        self.text_logs.insert(0,message)
        self.text_logs = self.text_logs[0:max_items]
        self.message['text'] = '\n'.join(self.text_logs)

    def roll_button_press(self):
        self.roll_graphic()
        self.gamebrain.roll()

    def roll_graphic(self):
        """
        This changes the dice graphic, but also changes the last roll 
        Its called 1 time for each player by the gamebrain whenever the player presses the roll button 
        """
        self.last_roll = random.randint(1,6)
        if self.last_roll == 1:
            img = self.roll_1
        elif self.last_roll == 2:
            img = self.roll_2
        elif self.last_roll == 3:
            img = self.roll_3
        elif self.last_roll == 4:
            img = self.roll_4
        elif self.last_roll == 5:
            img = self.roll_5
        else:
            img = self.roll_6
        self.roll_label["image"] = img


class BoardWidget:
    """
    Draws the board squares, generates the snake and ladder graphics, tells them to draw
    """
    def __init__(self, gamebrain, board_data, size):
        self.gamebrain = gamebrain
        self.frame = gamebrain.board_frame
        self.board_data = board_data
        self.size = size
        self.canvas = Canvas(self.frame, width=size, height=size)
        self.canvas.grid()
        self.board_squares = []
        self.ladder_graphics = []  # the snake/ladder graphics lists aren't currently used. Could add a wiggle animation or something to them
        self.snake_graphics = []
        self.start_square = ''
        self.end_square = ''
        self.make_board()

    def make_board(self):
        sizing = int(math.sqrt(self.board_data.length))  # number of squares per row and column
        x_pad = 70
        y_pad = 0
        square_sizing = ((self.size-x_pad) / sizing)-5  # how big to make each square 
        x = x_pad
        y = square_sizing * sizing - y_pad
        adding = True  # because they are drawn back and forth 
        self.start_square = StartSquare(self, x_pad-square_sizing, y, square_sizing)  # make the start square
        self.start_square.draw_on_canvas()
        for i in range(1, self.board_data.length+1):   # make the board squares
            square = BoardSquare(self, i, x, y, square_sizing)
            self.board_squares.append(square)  # square.number - 1 corresponds to the index in this list 
            square.draw_on_canvas()
            if i % sizing == 0:  # if at the end of a row
                y -= square_sizing
                adding = not adding
            else:
                if adding:
                    x += square_sizing
                else:
                    x -= square_sizing
        self.end_square = EndSquare(self, x - square_sizing, y+square_sizing, square_sizing)
        self.end_square.draw_on_canvas()

        for snake_pair in self.board_data.snakes:   # make the snake graphics
            start_square = self.board_squares[snake_pair[0]-1]
            end_square = self.board_squares[snake_pair[1]-1]
            snake_graphic = SnakeGraphic(start_square, end_square)
            snake_graphic.draw_on_canvas(self.canvas)
            self.snake_graphics.append(snake_graphic)
        for ladder_pair in self.board_data.ladders:  # make the ladder graphics
            start_square = self.board_squares[ladder_pair[0]-1]
            end_square = self.board_squares[ladder_pair[1]-1]
            ladder_graphic = LadderGraphic(start_square, end_square)
            ladder_graphic.draw_on_canvas(self.canvas)
            self.ladder_graphics.append(ladder_graphic)

    def get_square(self, new_square_number):
        return self.board_squares[new_square_number-1]


class GamePiece:
    """
    Draws a game piece, holds the piece's name and square
    """
    def __init__(self, name, color, starting_square, board, outline=1):
        self.name = name
        self.color = color
        self.square = starting_square
        self.square.pieces.append(self)
        self.square.piece_count += 1
        self.height = self.square.size / 2
        self.width = self.square.size / 4
        self.bottom_pad = self.width
        self.x = self.square.x
        self.y = self.square.y - self.bottom_pad
        self.head = -1   # these will be indexes of the shapes drawn on the canvas, so the canvas can be told 
        self.body = -1   # to move the shapes, delete them, etc. as the gamepiece moves around the board 
        self.body_outline = -1
        self.body_outline_width = outline  # so the human player piece can have a slightly thicker outline 
        self.current_square = 0 # start square 
        self.board = board
        self.draw_on_canvas()
        self.square.add_piece(self)

    def remove(self, canvas):  # used on a game reset
        canvas.delete(self.head)
        canvas.delete(self.body)
        canvas.delete(self.body_outline)

    def draw_on_canvas(self):
        x = self.x
        y = self.y
        x_2 = x + self.width
        y_2 = y + self.height/2
        tri_start_x = x + self.width / 2
        tri_start_y = y + self.height/ 4
        tri_end_y = y + (self.height/3)*4
        self.body_outline = self.board.canvas.create_line(tri_start_x, tri_start_y, x_2, tri_end_y, x, tri_end_y, tri_start_x, tri_start_y, fill='black', width=self.body_outline_width)
        self.head = self.board.canvas.create_oval(x, y, x_2, y_2, fill=self.color)
        self.body = self.board.canvas.create_polygon(tri_start_x, tri_start_y, x_2, tri_end_y, x, tri_end_y, tri_start_x, tri_start_y, fill=self.color)

    def move(self, x_off, y_off):
        self.x += x_off
        self.y += y_off
        self.board.canvas.move(self.head, x_off, y_off)
        self.board.canvas.move(self.body, x_off, y_off)
        self.board.canvas.move(self.body_outline, x_off, y_off)

    def move_to(self, target_x, target_y):
        x_off = target_x - self.x
        y_off = target_y - self.y - self.bottom_pad # ensures it's always a little above the square
        self.move(x_off, y_off)


class BoardSquare:
    """
    Draws a square on the canvas

    Holds list of pieces in that square

    Tells a piece to move to a location when it's added, and tells the old square to remove that piece
    """
    def __init__(self, board, num, x, y, size):
        self.board = board
        self.number = num
        if num % 2 == 0:
            self.color = 'white'
        else:
            self.color = 'red'
        self.x = x
        self.y = y
        self.size = size
        self.piece_count = 0
        self.pieces = []
        self.rectangle_id = -1  # holds indexes for canvas changes to shapes, but not currently used 
        self.text_id = -1

    def draw_on_canvas(self):
        canvas = self.board.canvas
        self.rectangle_id = canvas.create_rectangle(self.x, self.y, self.x+self.size, self.y+self.size, fill=self.color)
        center_y = int(self.y + self.size/2)
        center_x = int(self.x + self.size/2)
        self.text_id = canvas.create_text(center_x, center_y, text=str(self.number))
        
    def add_piece(self, piece):
        """
        Adds the piece to this square AND removes it from its last square
        Then moves the piece graphics to this square
        """
        self.pieces.append(piece)
        self.piece_count += 1
        piece.current_square = self.number
        piece.square.remove_piece(piece)
        piece.square = self
        piece.move_to(self.x, self.y)
        self.draw_pieces()
        

    def remove_piece(self, piece):
        index = self.pieces.index(piece)
        self.pieces.pop(index)
        self.piece_count -= 1

    def draw_pieces(self):
        """
        Rearranges all the pieces in the square so multiple pieces are visible at once
        
        Max is 14, because any more doesn't really look good 
        """
        x_off = 0
        y_off = 0
        canvas = self.board.canvas
        for index, piece in enumerate(self.pieces):
            piece.move_to(self.x, self.y)
            if piece.head == -1 or piece.body == -1:
                piece.draw_on_canvas()
            piece.move(x_off, y_off)
            if index == 6:
                x_off = 0
                y_off += self.size/2
            else:
                x_off += self.size/8


class StartSquare(BoardSquare):
    def __init__(self, board, x, y, size):
        BoardSquare.__init__(self, board, 0, x, y, size)
        self.color = '#9193bf'

    def draw_on_canvas(self):
        canvas = self.board.canvas
        x = self.x
        y = self.y
        x1 = self.x + self.size
        y1 = self.y + self.size/2
        x2 = self.x
        y2 = self.y + self.size
        canvas.create_polygon(x,y,x1,y1,x2,y2, fill=self.color)


class EndSquare(BoardSquare):
    def __init__(self, board, x, y, size):
        BoardSquare.__init__(self, board, 0, x, y, size)
        self.color = '#afea2e'

    def draw_on_canvas(self):
        canvas = self.board.canvas
        x = self.x + self.size
        y = self.y
        x1 = self.x
        y1 = self.y + self.size/2
        x2 = self.x + self.size
        y2 = self.y + self.size
        canvas.create_polygon(x,y,x1,y1,x2,y2, fill=self.color)


class SnakeGraphic:
    def __init__(self, start_square, end_square):
        self.start_square = start_square
        self.end_square = end_square

    def draw_on_canvas(self, canvas):
        """
        The snake graphic is just a 6 point smooth line 
        A few offset points are found between the start point and the end point,
        then the line is drawn through those point with the property "smooth"
        """
        size = self.start_square.size
        right_snake = False
        if self.start_square.x < self.end_square.x:
            left = self.start_square.x + size/2
            right = self.end_square.x + size/2
        else:
            left = self.end_square.x + size/2
            right = self.start_square.x + size/2
            right_snake = True
        if self.start_square.y > self.end_square.y:
            bottom = self.start_square.y + (size/4)
            top = self.end_square.y + (size/4)*3
        else:
            bottom = self.end_square.y + (size/4)
            top = self.start_square.y + (size/4)*3

        height = bottom-top
        width = right-left

        if right_snake:
            x = left
            y = bottom
            x1 = x
            y1 = bottom - height/3
            x2 = x1 + width/3
            y2 = y1
            x3 = x2 + width/3
            y3 = y1 - height/3
            x4 = x3 + width/3
            y4 = y3
            x5 = right
            y5 = top
            points = [x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5]
            canvas.create_line(points,width=10, smooth=True, fill='#4bc92c')
        else:
            x = right
            y = bottom
            x1 = x
            y1 = y - height/3
            x2 = x1 - width/3
            y2 = y1
            x3 = x2 - width/3
            y3 = y2 - height/3
            x4 = x3 - width/3
            y4 = y3
            x5 = x4
            y5 = y3 - height/3
            points = [x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5]
            canvas.create_line(points, width=10, smooth=True, fill = '#4bc92c')


class LadderGraphic:
    def __init__(self, board_square_start, board_square_end):
        self.start_square = board_square_start
        self.end_square = board_square_end

    def draw_on_canvas(self, canvas):
        pad_up_down_ratio = 0.27  # how offset should the ladder be from the top and bottom of square 
        width_ratio = 0.3  # how wide should the ladder be compared to the square

        size = self.start_square.size
        width = size * width_ratio
        pad_left_right = (size-width)/2

        if self.start_square.x < self.end_square.x:  # always draw left to right to ensure math for rungs will work 
            start_x = self.start_square.x
            start_y = self.start_square.y + pad_up_down_ratio * size
            end_x = self.end_square.x
            end_y = self.end_square.y + size - size * pad_up_down_ratio
        else:
            start_x = self.end_square.x
            start_y = self.end_square.y + size - size * pad_up_down_ratio
            end_x = self.start_square.x
            end_y = self.start_square.y + pad_up_down_ratio * size

        start_x += pad_left_right
        end_x += pad_left_right

        left_line = canvas.create_line(start_x, start_y, end_x, end_y, width=4)
        start_x += width
        end_x += width
        right_line = canvas.create_line(start_x, start_y, end_x, end_y, width=4)

        y_component = start_y - end_y  # a little trig and vectors for the rungs
        x_component = end_x - start_x
        angle = math.atan(y_component/x_component)
        magnitude = math.sqrt(x_component**2 + y_component**2)
        rungs = int(magnitude/width)
        magnitude_pad = (magnitude - rungs * width)/2
        sin = math.sin(angle)
        cos = math.cos(angle)
        y_1 = -magnitude_pad * sin + start_y
        x_1 = magnitude_pad * cos + start_x
        for i in range(0, rungs+1):
            # this just draws horizontal lines equal to the width of the ladder
            # where the rungs start is determined by the width of the ladder 
            canvas.create_line(x_1, y_1, x_1-width, y_1)
            y_1 = -(magnitude_pad + width * i) * sin + start_y
            x_1 = (magnitude_pad + width * i) * cos + start_x



