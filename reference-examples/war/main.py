"""
Tkinter War Entry

Created by Karl Miller, 3/20/21
"""

from tkinter import *
from tkinter import ttk
from customwidgets import *


root = Tk()
root.title('War!')

topFrame = ttk.Frame(root, padding="100 10 100 10")
midFrame = ttk.Frame(root, padding="100 10 100 10")
bottomFrame = ttk.Frame(root, padding="100 10 100 10")

opponent = PlayerWidget('Computer')
player = PlayerWidget('Player')
play_area = PlayAreaWidget(midFrame, player, opponent)

opponent.draw_on_frame(topFrame)
play_area.draw()
player.draw_on_frame(bottomFrame)

topFrame.grid()
midFrame.grid()
bottomFrame.grid()


def key_press(key):
    if play_area.playing:
        play_area.draw_card()
    else:
        play_area.new_game()


root.bind('<Return>', key_press)

root.mainloop()