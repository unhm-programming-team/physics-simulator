"""
Tkinter UI Widgets for War

Created by Karl Miller, 3/20/21
"""


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random


class PlayerWidget:
    def __init__(self, name):
        self.name = StringVar()  # this allows the name to be changable, but that option isn't currently implemented
        self.name.set(name)
        self.cards = []
        self.card_count = IntVar(0)  # IntVar lets the label update whenever the card count changes 

    def give_cards(self, card_array):
        self.cards = self.cards + card_array
        self.card_count.set(len(self.cards))

    def clear_cards(self):
        self.cards = []
        self.card_count.set(0)

    def take_card(self):
        self.card_count.set(self.card_count.get() - 1)
        if self.card_count.get() > -1:
            return self.cards.pop(0)
        else:   # this only happens if game ends on two cards matching - this return val will not be read 
            return 0

    def draw_on_frame(self, a_frame):
        ttk.Label(a_frame, textvariable=self.name).grid(column= 0, row=0, columnspan=3, sticky = W)
        ttk.Label(a_frame, text="cards:").grid(column= 0, row=1, sticky = E, padx=10)
        ttk.Label(a_frame, textvariable = self.card_count).grid(column=1, row=1, sticky = W)


class Card:
    """
    Holds a value and a suit

    To test win condition logic quickly, set shuffle to False in static method get_deck
    """
    def __init__(self, val, suit):
        self.val = val
        self.suit = suit

    @staticmethod
    def get_deck(shuffle=True):
        deck = []
        suits = ['hearts','diamonds','spades','clubs']
        for i in range(1, 14):
            for s in range(0, 4):
                deck.append(Card(i, suits[s]))
        if(shuffle):
            random.shuffle(deck)
        return deck

    @staticmethod
    def compare(card1, card2):
        """
        Returns 1 if card1 > card2
        Returns -1 if card2 > card1
        Returns 0 if equal

        Accounts for 2s beating aces
        :param card1:
        :type card1: class Card
        :param card2:
        :type card2: class Card
        :return: 1, -1, or 0
        """
        if card1.val == 1 and card2.val != 2:
            return 1
        if card2.val == 1 and card1.val != 2:
            return -1
        if card1.val > card2.val:
            return 1
        if card2.val > card1.val:
            return -1
        return 0


class CardWidget:
    """
    Display the value of the card and a graphic for the suit
    """
    def __init__(self, a_frame):
        self.frame = ttk.Frame(a_frame, relief='ridge')
        self.spade_image = PhotoImage(file='spade.gif')
        self.club_image = PhotoImage(file='club.gif')
        self.heart_image = PhotoImage(file='heart.gif')
        self.diamond_image = PhotoImage(file='diamond.gif')
        self.spade = ttk.Label(self.frame, image=self.spade_image)
        self.club = ttk.Label(self.frame, image=self.club_image)
        self.heart = ttk.Label(self.frame, image=self.heart_image)
        self.diamond = ttk.Label(self.frame, image=self.diamond_image)
        self.value = StringVar()
        self.value.set('0')
        self.value_label = ttk.Label(self.frame, textvariable=self.value, padding=7)
        self.suit = self.spade
        self.first_run = True  # so we can safely call grid.forget and remove old card images after first one

    def load_card(self, card):
        val = card.val
        if val == 13:
            self.value.set('K')
        elif val == 12:
            self.value.set('Q')
        elif val == 11:
            self.value.set('J')
        elif val == 1:
            self.value.set('A')
        else:
            self.value.set(str(val))
        suit = card.suit
        self.suit.grid_forget()  # lose the old label 
        if suit == 'hearts':
            self.suit = self.heart
        elif suit == 'diamonds':
            self.suit = self.diamond
        elif suit == 'spades':
            self.suit = self.spade
        else:
            self.suit = self.club
        self.redraw()  #  redraw the label for the new suit 

    def draw_on_frame(self, target_row):
        self.frame.grid(row=target_row, columnspan=3)

    def redraw(self):
        if self.first_run:
            self.value_label.grid(column=0, row=0, sticky=E)
            self.first_run = False
        self.suit.grid(column=1, row=0, sticky=(N,S,W) )


class PlayAreaWidget:
    def __init__(self, a_frame, player, opponent):
        """
        The play area
        :param a_frame: class Tkinter Frame object
        :param player: class PlayerWidget
        :param opponent: class PlayerWidget
        """
        self.frame = a_frame  # needs reference for displaying card graphics 
        self.new_game_button = ttk.Button(a_frame, text="New Game", command=self.new_game)
        self.player = player
        self.opponent = opponent
        self.draw_button = ttk.Button(a_frame, text="Draw", command=self.draw_card)
        self.opponent_card = CardWidget(a_frame)
        self.player_card = CardWidget(a_frame)
        self.last_result = StringVar()
        self.last_result.set('+0')  # how many cards were added and to what stack, player, the pile, or the opponent
        self.last_result_label = ttk.Label(a_frame, textvariable=self.last_result)
        self.stack = []
        self.stack_count = IntVar()
        self.stack_count.set(0)
        self.stack_label = ttk.Label(a_frame, textvariable=self.stack_count)  # how many cards are on the pile
        self.playing = False

    def new_game(self):
        """
        Resets player and opponent decks
        :return:
        """
        deck = Card.get_deck()
        half1 = deck[0:int(len(deck) / 2)]
        half2 = deck[int(len(deck) / 2):]
        self.player.clear_cards()
        self.opponent.clear_cards()
        self.stack = []
        self.player.give_cards(half1)
        self.opponent.give_cards(half2)
        self.playing = True
        self.draw()

    def draw(self):
        """
        Called after initialization to ensure proper positioning

        Not to be confused with draw_card; this method creates the UI widgets
        """
        if self.playing:
            self.new_game_button.grid_forget()
            self.draw_button.grid(row=1,columnspan=3)
            self.opponent_card.draw_on_frame(0)
            self.player_card.draw_on_frame(2)
            self.last_result_label.grid(row=1, column=4)
            self.stack_label.grid(row=1, column=5)
        else:
            self.draw_button.grid_forget()
            self.new_game_button.grid(row=1, columnspan=3)

    def draw_card(self):
        player_card = self.player.take_card()
        opponent_card = self.opponent.take_card()
        self.player_card.load_card(player_card)  # loads it into the card widget for display
        self.opponent_card.load_card(opponent_card)
        self.stack += [player_card, opponent_card]  # adds both cards to the stack 
        result = Card.compare(player_card, opponent_card)
        if result > 0:
            self.player.give_cards(self.stack)
            self.last_result.set('+' + str(len(self.stack)-1)) # -1 because it doesn't include the card the opp just played 
            self.last_result_label.grid(row=2)
            self.stack = []
        elif result < 0:
            self.opponent.give_cards(self.stack)
            self.last_result.set('+' + str(len(self.stack)-1))
            self.last_result_label.grid(row=0)
            self.stack = []
        else:
            card_1 = self.player.take_card()   # each player puts 2 cards on the stack when card values are equal 
            card_2 = self.opponent.take_card()
            card_3 = self.player.take_card()
            card_4 = self.opponent.take_card()
            self.stack += [card_1,card_2,card_3,card_4]
            self.last_result.set('+6')
            self.last_result_label.grid(row=1)
        self.stack_count.set(len(self.stack)) # set the stack count to the number of cards there 
        if self.player.card_count.get() <= 0:
            self.win(self.opponent)
        elif self.opponent.card_count.get() <= 0:
            self.win(self.player)

    def win(self, player):
        self.playing = False
        if player == self.player:
            message_text = 'Congratulations!'
            title_text = 'Victory'
        else:
            message_text = 'Sorry!'
            title_text = 'Defeat'
        messagebox.showinfo(message=message_text, title=title_text)
        self.draw()


