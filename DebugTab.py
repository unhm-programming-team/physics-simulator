"""Contains 'tabs' which are really just frames but are used by the `ttk.Notebook object
<https://tkdocs.com/shipman/ttk-Notebook.html>`_ for tabbed display.

The LogTab contains a Listbox and a Scrollbar. Strings can be sent to LogTab to be logged - they will be added to
the list. When clicked, they display on a lower label to account for long-stringed log events.

The DebugTab contains buttons for adding objects, for testing purposes. The panels for adding those objects are part
of this module. Ultimately, the only objects that will likely be added in later versions of this project are
ForceObjects or higher. """

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
        self.vector_adder = VectorObjectAdder(self.window, ttk.Frame(self))
        self.mass_adder = MassObjectAdder(self.window, ttk.Frame(self))
        self.force_adder = ForceObjectAdder(self.window, ttk.Frame(self))


class VectorObjectAdder:
    """
    Created by :class:`DebugTab.DebugTab`.

    Deprecated, and should be removed in a future version.
    """
    def __init__(self, window, parent_frame):
        """
        Constructor

        Will call .grid() on parent_frame
        """
        self.window = window
        self.frame = parent_frame
        self.add_button = ttk.Button(self.frame, text='add massless vector object', command=self.add_button_press)
        x_label = ttk.Label(self.frame, text='x')
        y_label = ttk.Label(self.frame, text='y')
        width_label = ttk.Label(self.frame, text='width')
        height_label = ttk.Label(self.frame, text='height')
        color_label = ttk.Label(self.frame, text='color')

        registered_validator_id = self.frame.register(Utility.validate_number_input)

        self.x_variable = StringVar(value='0')
        self.y_variable = StringVar(value='0')
        self.width_variable = StringVar(value='20')
        self.height_variable = StringVar(value='20')
        self.x_entry = ttk.Entry(self.frame, textvariable=self.x_variable, width=5, validate='all', validatecommand=(registered_validator_id, '%S'))
        self.y_entry = ttk.Entry(self.frame, textvariable=self.y_variable, width=5, validate='all', validatecommand=(registered_validator_id, '%S'))
        self.width_entry = ttk.Entry(self.frame, textvariable=self.width_variable, width=5, validate='all', validatecommand=(registered_validator_id, '%S'))
        self.height_entry = ttk.Entry(self.frame, textvariable=self.height_variable, width=5, validate='all', validatecommand=(registered_validator_id, '%S'))

        self.color_button = Button(self.frame, text='blue', command=self.select_color)

        self.add_button.grid(column=0, row=1)
        x_label.grid(column=1, row=0)
        self.x_entry.grid(column=1, row=1)
        y_label.grid(column=2, row=0)
        self.y_entry.grid(column=2, row=1)
        width_label.grid(column=3, row=0)
        self.width_entry.grid(column=3, row=1)
        height_label.grid(column=4, row=0)
        self.height_entry.grid(column=4, row=1)
        color_label.grid(column=5, row=0)
        self.color_button.grid(column=5, row=1)
        self.frame.grid()

    def select_color(self):
        result = colorchooser.askcolor(color=self.color_button['text'])
        self.color_button['text'] = result[1]

    def add_button_press(self):
        # self, x = 0, y = 0, width = 5, height = 5, velocity = 0, acceleration = 0, color = 'blue')
        x = float(self.x_variable.get())
        y = float(self.y_variable.get())
        width = float(self.width_variable.get())
        height = float(self.height_variable.get())
        color = self.color_button['text']
        self.window.physics_canvas.add_gravity_vector_object(x=x, y=y, width=width, height=height, color=color)


class MassObjectAdder:
    """
    Created by :class:`DebugTab.DebugTab`.

    Deprecated, and should be removed in a future version.
    """
    def __init__(self, window, parent_frame):
        """
        Will call .grid() on parent frame
        """
        self.window = window
        self.frame = parent_frame
        self.add_button = ttk.Button(self.frame, text='add object with mass', command=self.add_button_press)
        material_label = ttk.Label(self.frame, text='material')
        mass_label = ttk.Label(self.frame, text='mass')

        self.listbox = ttk.Spinbox(self.frame, value=list(Substance.MATERIALS.keys()), state='readonly', width=11 )
        self.listbox.set(list(Substance.MATERIALS.keys())[0])

        registered_validator_id = self.frame.register(Utility.validate_number_input)
        self.mass_variable = StringVar(value=str(Options['default mass']))
        self.mass_entry = ttk.Entry(self.frame, textvariable=self.mass_variable, validate='all', validatecommand=(registered_validator_id, '%S'))

        self.add_button.grid(column=0, row=1)
        material_label.grid(column=1, row=0)
        self.listbox.grid(column=1,row=1)
        mass_label.grid(column=2,row=0)
        self.mass_entry.grid(column=2,row=1)
        self.frame.grid()

    def add_button_press(self):
        material = Substance.MATERIALS[self.listbox.get()]
        mass = float(self.mass_variable.get())
        mass_object = Physics.MassObject(self.window.physics_canvas, material, mass)
        self.window.physics_canvas.add_mass_object(mass_object)
        self.window.physics_canvas.move_mass_object(mass_object)


class ForceObjectAdder:
    """
    Created by :class:`DebugTab.DebugTab`.

    Deprecated, and should be removed in a future version.
    """
    def __init__(self, window, parent_frame):
        """
        Will call .grid() on parent_frame
        """
        self.window = window
        self.frame = parent_frame
        self.add_button = ttk.Button(self.frame, text='add Force Object', command=self.add_button_press)
        force_angle_label = ttk.Label(self.frame, text='angle')
        magnitude_label = ttk.Label(self.frame, text='magnitude')
        self.force_angle_string = StringVar()
        self.force_magnitude_string = StringVar()
        force_angle_display = ttk.Label(self.frame, textvariable=self.force_angle_string)
        force_magnitude_display = ttk.Label(self.frame, textvariable=self.force_magnitude_string)

        self.add_button.grid(column=0, row=1)
        force_angle_label.grid(column=1,row=0)
        magnitude_label.grid(column=2,row=0)
        force_angle_display.grid(column=1, row=1)
        force_magnitude_display.grid(column=1,row=1)
        self.frame.grid()

        self.force_objects = []
        self.window.root.bind('<Down>', self.key_handler)
        self.window.root.bind('<Up>', self.key_handler)
        self.window.root.bind('<Left>', self.key_handler)
        self.window.root.bind('<Right>', self.key_handler)

    def add_button_press(self):
        material = Substance.MATERIALS['cork']
        mass = 100000
        force_object = Physics.ForceObject(self.window.physics_canvas, material, mass)
        self.force_objects.append(force_object)
        self.window.physics_canvas.add_force_object(force_object)

    def key_handler(self, event):
        direction = 'n'
        if event.keysym == 'Right':
            direction = 'e'
        elif event.keysym == 'Up':
            direction = 's'
        elif event.keysym == 'Left':
            direction = 'w'
        for i in range(0, len(self.force_objects)):
            force = Physics.Force.make_directional_force(direction, Options['key force magnitude'], Options['key force duration'])
            self.force_objects[i].forces.append(force)

