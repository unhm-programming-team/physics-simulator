from tkinter import *
from tkinter import ttk, colorchooser

from Options import Options
import Physics
import Utility


class Window:
    def __init__(self):
        self.root = Tk()  # start tkinter
        self.root.title = '2d Physics Simulator'
        self.root_frame = ttk.Frame(self.root)
        self.center_frame = ttk.Frame(self.root_frame)
        self.right_frame = ttk.Frame(self.root_frame)

        self.physics_canvas = PhysicsCanvas(self, self.center_frame)
        self.object_adder = ObjectAdder(self, self.right_frame)

        self.root_frame.grid()
        self.center_frame.grid(row=0, column=1)
        self.right_frame.grid(row=0, column=2)
        self.root.mainloop()


class PhysicsCanvas:
    def __init__(self, window, parent_frame):
        self.window = window
        self.frame = parent_frame
        self.width = Options['canvas width']
        self.height = Options['canvas height']
        self.scale = Options['zoom']
        self.origin_x = self.width/2
        self.origin_y = self.height/2
        self.max_x = self.width/2
        self.min_x = -self.width/2
        self.max_y = self.height/2
        self.min_y = -self.height/2
        self.canvas = Canvas(self.frame, width=self.width, height=self.height)
        self.physics_objects = []

        self.canvas.grid()

    def add(self, x=0, y=0, width=5, height=5, velocity=0, acceleration=0, color='blue'):
        physics_object = Physics.PhysicsObject(self)
        if x > self.max_x:  # objects placed beyond canvas size get moved to edge
            x = self.max_x
        elif x < self.min_x:
            x = self.min_x
        if y > self.max_y:
            x = self.max_y
        elif y < self.min_y:
            x = self.min_y
        displacement_vector = Physics.Vector.make_vector_from_components(x, y)
        physics_object.displacement = displacement_vector
        physics_object.width = width
        physics_object.height = height
        x_0 = x - width/2 + self.origin_x
        y_0 = y - height/2 + self.origin_y
        x_1 = x + width/2 + self.origin_x
        y_1 = y + height/2 + self.origin_y
        physics_object.canvas_id = self.canvas.create_oval(x_0, y_0, x_1, y_1, fill=color)
        self.physics_objects.append(physics_object)


class ObjectAdder:
    def __init__(self, window, parent_frame):
        self.window = window
        self.frame = parent_frame
        self.add_button = ttk.Button(self.frame, text='add', command=self.add_button_press)
        x_label = ttk.Label(self.frame, text='x')
        y_label = ttk.Label(self.frame, text='y')
        width_label = ttk.Label(self.frame, text='width')
        height_label = ttk.Label(self.frame, text='height')
        color_label = ttk.Label(self.frame, text='color')

        registered_validator_id = self.frame.register(Utility.validate_number_input)

        self.x_entry = ttk.Entry(self.frame, width=5, validate='all', validatecommand=(registered_validator_id, '%S'))
        self.y_entry = ttk.Entry(self.frame, width=5, validate='all', validatecommand=(registered_validator_id, '%S'))
        self.width_entry = ttk.Entry(self.frame, width=5, validate='all', validatecommand=(registered_validator_id, '%S'))
        self.height_entry = ttk.Entry(self.frame, width=5, validate='all', validatecommand=(registered_validator_id, '%S'))

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

    def select_color(self):
        result = colorchooser.askcolor(color=self.color_button['text'])
        self.color_button['text'] = result[1]

    def add_button_press(self):
        # self, x = 0, y = 0, width = 5, height = 5, velocity = 0, acceleration = 0, color = 'blue')
        x = float(self.x_entry.get())
        y = float(self.y_entry.get())
        width = float(self.width_entry.get())
        height = float(self.height_entry.get())
        color = self.color_button['text']
        self.window.physics_canvas.add(x=x, y=y, width=width, height=height, color=color)


