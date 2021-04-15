"""Contains 'tabs' which are really just frames but are used by the `ttk.Notebook object
<https://tkdocs.com/shipman/ttk-Notebook.html>`_ for tabbed display.

The LogTab contains a Listbox and a Scrollbar. Strings can be sent to LogTab to be logged - they will be added to
the list. When clicked, they display on a lower label to account for long-stringed log events.

The DebugTab contains buttons for adding objects, for testing purposes. The panels for adding those objects are part
of this module. """
import random
from tkinter import *
from tkinter import ttk, colorchooser

import Particle
import Utility, Substance, Physics
from Options import Options

import time, math


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

        self.test_collision = ttk.Button(self.frame, text='test collision', command=self.add_test_collision)
        self.test_collision.grid(column=0,row=2)
        self.is_horizontal_collision = BooleanVar()
        collision_check = ttk.Checkbutton(self.frame, text='horizontal', variable=self.is_horizontal_collision)
        collision_check.grid(column=1, row=2)
        self.frame.grid()

        self.particle_test = ttk.Button(self.frame, text='particle test', command=self.particle_test)
        self.particle_test.grid(column=0, row=3)

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

    def particle_test(self):
        particle = Particle.Particle()
        physics_canvas = self.window.physics_canvas
        particle.add_to(physics_canvas)


    def add_test_collision(self):
        physics_canvas = self.window.physics_canvas
        ob1 = Physics.PhysicsObject(Substance.MATERIALS['chalk'], Options['default mass'])
        ob2 = Physics.PhysicsObject(Substance.MATERIALS['maple'], (Options['default mass']*2)/3)

        x1 = -(random.random() * physics_canvas.width/2)
        x2 = (random.random() * physics_canvas.width/2)

        ob1.displacement = Physics.Vector.make_vector_from_components(x1, 50)
        ob2.displacement = Physics.Vector.make_vector_from_components(x2, 15)

        if not self.is_horizontal_collision.get():
            ob1.velocity = Physics.Vector.make_directional_vector('NE', 22)
            ob1.velocity.rotate(-1.3)
            ob2.velocity = Physics.Vector.make_directional_vector('NW', 20)
        else:
            ob1.velocity = Physics.Vector.make_directional_vector('E', 22)

        physics_canvas.add_physics_object(ob1)
        physics_canvas.add_physics_object(ob2)


        # try adding a test triangle vector to check our math on vector intersections
        ob1_to_2 = ob2.displacement.subtract_make(ob1.displacement)  # A Vector
        ob2_to_1 = ob1.displacement.subtract_make(ob2.displacement)

        ob1_inner_angle = math.fabs(ob1.velocity.angle - ob1_to_2.angle)
        ob2_inner_angle = math.fabs(ob2.velocity.angle - ob2_to_1.angle)
        missing_inner_angle = math.pi - ob1_inner_angle - ob2_inner_angle
        ob1_to_collision_length = (math.sin(ob2_inner_angle)*ob1_to_2.magnitude)/(math.sin(missing_inner_angle))
        ob1_to_collision = Physics.Vector(ob1.velocity.angle, ob1_to_collision_length)

        print('ob1 vel', ob1.velocity)
        print('ob2 vel', ob2.velocity)
        print('vec between', ob1_to_2)
        print('vec between back', ob2_to_1)

        line2 = Particle.Line(3, ob2.velocity.scale_make(2), 'black')
        line2.displacement = ob2.displacement.scale_make(1)
        line2.add_to(physics_canvas)

        line3 = Particle.Line(3, ob1_to_2, 'black')
        line3.displacement = ob1.displacement.scale_make(1)
        line3.add_to(physics_canvas)

        line5 = Particle.Line(3, ob1_to_collision, 'green')
        line5.displacement = ob1.displacement.scale_make(1)
        line5.add_to(physics_canvas)


