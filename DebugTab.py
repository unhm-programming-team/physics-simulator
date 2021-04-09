"""Contains 'tabs' which are really just frames but are used by the `ttk.Notebook object
<https://tkdocs.com/shipman/ttk-Notebook.html>`_ for tabbed display.

The LogTab contains a Listbox and a Scrollbar. Strings can be sent to LogTab to be logged - they will be added to
the list. When clicked, they display on a lower label to account for long-stringed log events.

The DebugTab contains buttons for adding objects, for testing purposes. The panels for adding those objects are part
of this module. """

from tkinter import *
from tkinter import ttk, colorchooser

import Utility, Substance, Physics
from Options import Options

import time


class LogTab(ttk.Frame):
    """
    Fills a frame with UI component necessary for keeping a log. Intended use is as a tab for the Notebook object.

    Created by :class:`Ui.MainWindow`

    Uses a `Tkinter.Listbox <https://tkdocs.com/shipman/listbox.html>`_.

    :param parent: The frame where this component will be placed.
    :type parent: widget
    :param window: The broad reference window.
    :type window: See MainWindow in :doc: Ui
    """
    def __init__(self, parent, window):
        """
        Constructor
        """
        ttk.Frame.__init__(self, parent)
        self.window = window
        self.scroll_bar = Scrollbar(self)
        self.list_box = Listbox(self, selectmode=SINGLE, width=45, yscrollcommand=self.scroll_bar.set)
        self.list_box.bind('<ButtonPress>', self.click)
        self.selected_var = StringVar()
        selected_label = ttk.Label(self, textvariable=self.selected_var, wraplength=230)
        self.list_box.grid(column=1, row=0)
        self.scroll_bar.grid(column=0, row=0, sticky=(N,S))
        selected_label.grid(column=1,row=1)

    def click(self, event):
        """
        Called when ListBox in this widget is clicked.

        Displays selected item in the label, in case the log entry is too long for the ListBox.

        :param event: MouseEvent
        """
        index = self.list_box.nearest(event.y)
        selection = self.list_box.get(index)
        self.selected_var.set(selection)

    def log(self, string):
        """
        Creates an entry in the Listbox from the string. Prepends a timestamp.
        :param string: text to log
        """
        timestring = time.strftime('%H:%M:%S', time.localtime())
        self.list_box.insert(END, f"{string}    {timestring}")


class DebugTab(ttk.Frame):
    """
    Fills a frame with some UI components for doing debug operations.

    Created by :class:`Ui.MainWindow`.

    :param parent: The frame where this component will be placed.
    :type parent: widget
    """
    def __init__(self, parent, window):
        ttk.Frame.__init__(self, parent)
        self.window = window
        self.force_adder = ForceObjectAdder(self.window, ttk.Frame(self))


class ForceObjectAdder:
    """
    Created by :class:`DebugTab.DebugTab`.

    May be removed in a future version. Somewhat redundant due to AddObjectWindow being implemented. However,
    it still does the binding of key presses to object moves, so it's left for now while said feature is still useful
    for debug and testing.
    """
    def __init__(self, window, parent_frame):
        """
        Will call .grid() on parent_frame
        """
        self.window = window
        self.frame = parent_frame
        self.add_button = ttk.Button(self.frame, text='add Force Object', command=self.add_button_press)

        self.add_button.grid(column=0, row=1)
        self.frame.grid()

        self.force_objects = []
        self.window.root.bind('<Down>', self.key_handler)
        self.window.root.bind('<Up>', self.key_handler)
        self.window.root.bind('<Left>', self.key_handler)
        self.window.root.bind('<Right>', self.key_handler)

    def add_button_press(self):
        """
        Adds a cork object with mass 100,000 to the PhysicsCanvas

        The object is controllable with keyboard inputs.

        :return:
        """
        material = Substance.MATERIALS['cork']
        mass = 100000
        force_object = Physics.PhysicsObject(material, mass)
        self.force_objects.append(force_object)
        self.window.physics_canvas.add_physics_object(force_object)

    def key_handler(self, event):
        direction = 's'
        if event.keysym == 'Right':
            direction = 'e'
        elif event.keysym == 'Up':
            direction = 'n'
        elif event.keysym == 'Left':
            direction = 'w'
        for i in range(0, len(self.force_objects)):
            force = Physics.Force.make_directional_force(direction, Options['key force magnitude'], Options['key force duration'])
            self.force_objects[i].forces.append(force)

