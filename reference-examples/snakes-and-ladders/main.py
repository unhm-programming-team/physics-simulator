from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from CustomWidgets import *


class GameBrain():
    """
    Handles game logic, creates needed widgets
    """
    def __init__(self, tk_root):
        self.root_frame = ttk.Frame(tk_root)
        # create the tkinter frames 
        self.startup_frame = ttk.Frame(self.root_frame, padding="20 20 20 20")
        self.board_frame = ttk.Frame(self.root_frame)
        self.control_frame = ttk.Frame(self.root_frame)
        
        # create the custom widgets 
        self.startup = StartupWidget(self.startup_frame)
        self.startup.set_start_button(self.game_start)
        self.data = BoardData.default_board()
        self.board = BoardWidget(self, self.data, 600)
        self.dice = DiceWidget(self)
        
        # state just controls what enter button does 
        self.state = 'startup'

        self.human_player = -1  # will be set to a gamepiece widget object game_start is called  
        self.players = []

        self.root_frame.grid()  # .grid adds tkinter widgets to the layout they are assigned
        self.ui_start()

        tk_root.bind("<Return>", self.enter_press)  # press enter to start game or roll dice 

    def game_start(self):
        self.state = 'game'
        self.startup_frame.grid_remove()
        for p in self.players:  # reset the board by clearing players from last game(if any)
            p.remove(self.board.canvas)
        for square in self.board.board_squares:
            square.pieces = []
        self.players = []
        self.human_player = GamePiece('human', '#edf418', self.board.start_square, self.board, outline=3)
        player_count = int(self.startup.player_selector.get())  # gets count from startup UI menu
        self.players = [self.human_player]
        for i in range(1, player_count):
            b = str(hex(i))[2]  # vary the computer piece colors slightly
            self.players.append(GamePiece('computer '+str(i),'#'+b+'88', self.board.start_square, self.board))
        self.board_frame.grid(column=0)
        self.control_frame.grid(column=1, row=0)

    def roll(self):
        """
        Called when player presses the roll button or presses the enter key
        
        Rolls the dice and moves the player by that amount, then rolls the dice for every computer and moves them all
        """
        amount = self.dice.last_roll
        self.move_piece(self.human_player, amount)
        for i in range(1, len(self.players)):
            self.dice.roll_graphic()
            player = self.players[i]
            amount = self.dice.last_roll
            self.move_piece(player, amount)

    def move_piece(self, piece, amount):
        current_square_number = piece.current_square
        new_square_number = current_square_number + amount
        new_square_number = self.data.check_for_snakes_or_ladders(new_square_number)
        exact = self.startup.exact_value.get()
        # check for win condition
        if new_square_number >= self.data.length-1:
            if not exact:
                self.board.end_square.add_piece(piece)
                self.win(piece)
            elif new_square_number == self.data.length:
                self.board.end_square.add_piece(piece)
                self.win(piece)
        else:  # otherwise, move the piece and check if capturing. If so, move those pieces to start
            new_square = self.board.get_square(new_square_number)
            capturing = self.startup.capture_value.get()  # get this from the ui select on startup 
            if capturing:
                for p in new_square.pieces:
                    self.board.start_square.add_piece(p)
            new_square.add_piece(piece)
        self.dice.log_message(f"{piece.name} rolled {amount}: {current_square_number} to {new_square_number}")

    def win(self, piece):
        self.state = 'win'
        if piece == self.human_player:
            status = 'victory'
        else:
            status = 'defeat'
        messagebox.showinfo(message=f"{piece.name} won!", title=status)
        self.ui_start()

    def ui_start(self):
        self.state = 'startup'
        self.board_frame.grid_remove()
        self.control_frame.grid_remove()
        self.startup_frame.grid()

    def enter_press(self,b):
        if self.state == 'startup':
            self.game_start()
        elif self.state == 'game':
            self.dice.roll_graphic()
            self.roll()


class BoardData:
    """
    Holds raw numeric data about the board with lists
    """
    def __init__(self, length, ladders, snakes):
        self.length = length
        self.ladders = ladders
        self.snakes = snakes

    def check_for_snakes_or_ladders(self, square_number):
        """
        Checks square against snakes and ladders
        :param square_number: square to check
        :type square_number: int
        :return: the resulting square, may be the same if it doesn't match snake or ladder
        :rtype: int
        """
        for pair in self.snakes + self.ladders:
            if pair[0] == square_number:
                return pair[1]
        return square_number

    @staticmethod
    def default_board():
        length = 100
        ladders = [[86, 99], [71, 92], [28, 76], [50, 67], [21, 42], [1, 38], [4, 14], [8, 10]]
        snakes = [ [97, 78], [95, 56], [88, 24], [62, 18], [48, 26], [36, 6], [32, 10]]
        return BoardData(length, ladders, snakes)


root = Tk()
root.title('Snakes and Ladders')

brain = GameBrain(root)

root.mainloop()
