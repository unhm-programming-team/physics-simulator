from tkinter import *
from tkinter import ttk, colorchooser

import threading
import time

from Options import Options
import Physics
import Utility
import Substance


class Window:
    def __init__(self):
        self.root = Tk()  # start tkinter
        self.root.title = '2d Physics Simulator'
        self.root_frame = ttk.Frame(self.root)
        self.center_frame = ttk.Frame(self.root_frame)
        self.right_frame = ttk.Frame(self.root_frame)
        self.bottom_frame = ttk.Frame(self.root_frame)

        self.physics_canvas = PhysicsCanvas(self, self.center_frame)
        self.vector_object_adder = VectorObjectAdder(self, ttk.Frame(self.right_frame))
        self.mass_object_adder = MassObjectAdder(self, ttk.Frame(self.right_frame))
        self.force_object_adder = ForceObjectAdder(self, ttk.Frame(self.right_frame))
        self.time_selector = TimeSelector(self, self.bottom_frame)

        self.root_frame.grid()
        self.center_frame.grid(row=1, column=1)
        self.right_frame.grid(row=1, column=2)
        self.bottom_frame.grid(row=2, column=1)
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

    def add_gravity_vector_object(self, x=0, y=0, width=5, height=5, velocity=0, acceleration=0, color='blue'):
        physics_object = Physics.VectorObject(self)
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
        physics_object.acceleration = Physics.Vector.make_directional_vector('S', -9.8)
        physics_object.width = width
        physics_object.height = height
        x_0 = x - width/2 + self.origin_x
        y_0 = y - height/2 + self.origin_y
        x_1 = x + width/2 + self.origin_x
        y_1 = y + height/2 + self.origin_y
        physics_object.canvas_id = self.canvas.create_oval(x_0, y_0, x_1, y_1, fill=color)
        self.physics_objects.append(physics_object)

    def add_mass_object(self, mass_object):
        mass_object.displacement = Physics.Vector(0,0)
        mass_object.calculate_bounds()
        x_0 = mass_object.x_0
        y_0 = mass_object.y_0
        x_1 = mass_object.x_1
        y_1 = mass_object.y_1
        color = mass_object.material.color
        mass_object.canvas_id = self.canvas.create_oval(x_0, y_0, x_1, y_1, fill=color)
        self.physics_objects.append(mass_object)

    def update(self, interval):
        for o in self.physics_objects:
            o.update(interval)

    def move_me(self, physics_object):
        displacement_x = physics_object.displacement.x
        displacement_y = physics_object.displacement.y
        physics_object.calculate_bounds()
        if displacement_x + physics_object.width/2 > self.max_x and physics_object.velocity.x > 0:
            physics_object.velocity.x *= -1
        if displacement_x - physics_object.width/2 < self.min_x and physics_object.velocity.x < 0:
            physics_object.velocity.x *= -1
        if displacement_y + physics_object.height > self.max_y and physics_object.velocity.y > 0:
            physics_object.velocity.y *= -1
        if displacement_y - physics_object.width/2 < self.min_y and physics_object.velocity.y < 0:
            physics_object.velocity.y *= -1
        physics_object.velocity.calculate_angles()

        new_x = displacement_x + self.origin_x - physics_object.width/2
        new_y = displacement_y + self.origin_y - physics_object.height/2
        self.canvas.moveto(physics_object.canvas_id, new_x, new_y)

    def move_mass_object(self, mass_object):
        mass_object.calculate_bounds()
        velocity = mass_object.velocity
        x_0 = mass_object.x_0 + self.origin_x
        if x_0 < 0 and velocity.x < 0:
            velocity.x *= -1
        x_1 = mass_object.x_1 + self.origin_x
        if x_1 > self.width and velocity.x > 0:
            velocity.x *= -1
        y_0 = mass_object.y_0 + self.origin_y
        if y_0 < 0 and velocity.y < 0:
            velocity.y *= -1
        y_1 = mass_object.y_1 + self.origin_y
        if y_1 > self.height and velocity.y > 0:
            velocity.y *= -1
        x = mass_object.displacement.x + self.origin_x
        y = mass_object.displacement.y + self.origin_y
        self.canvas.moveto(mass_object.canvas_id, x_0, y_0)

    def add_force_object(self, force_object):
        self.physics_objects.append(force_object)
        x0 = force_object.x_0 + self.origin_x
        y0 = force_object.y_0 + self.origin_y
        x1 = force_object.x_1 + self.origin_x
        y1 = force_object.y_1 + self.origin_y
        color = force_object.material.color
        force_object.canvas_id = self.canvas.create_oval(x0, y0, x1, y1, fill=color)

    def move_force_object(self, force_object):
        velocity = force_object.velocity
        x0 = force_object.x_0 + self.origin_x
        y0 = force_object.y_0 + self.origin_y
        x1 = force_object.x_1 + self.origin_x
        y1 = force_object.y_1 + self.origin_y
        opp_force = False
        if x0 < 0 and velocity.x < 0:
            velocity.x *= -1
        if x1 > self.width and velocity.x > 0:
            velocity.x *= -1
        if y0 < 0 and velocity.y < 0:
            velocity.y *= -1
        if y1 > self.height and velocity.y > 0:
            velocity.y *= -1
        velocity.calculate_angles()
        force_object.calculate_bounds()
        self.canvas.moveto(force_object.canvas_id, x0, y0)


class VectorObjectAdder:
    def __init__(self, window, parent_frame):
        """
        Will call .grid() on parent_frame
        """
        self.window = window
        self.frame = parent_frame
        self.add_button = ttk.Button(self.frame, text='add massless gravity vector object', command=self.add_button_press)
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


class TimeSelector:
    def __init__(self, window, parent_frame):
        self.window = window
        self.frame = parent_frame
        self.pause_button = Button(self.frame, text='Pause', command=self.stop_thread)
        self.start_button = Button(self.frame, text='Play', command=self.start_thread)
        self.step_button = Button(self.frame, text='Step', command=self.step)

        self.run_thread = threading.Thread(target=self.run, daemon=True)

        self.running = False

        self.pause_button.grid(column=0, row=0)
        self.start_button.grid(column=1, row=0)
        self.step_button.grid(column=2, row=0)

    def run(self):
        last_time = time.time()
        while self.running:
            now_time = time.time()
            interval = now_time - last_time
            last_time = now_time
            self.window.physics_canvas.update(interval)
            time.sleep(Options['update interval'])

    def start_thread(self):
        self.stop_thread()
        self.running = True
        self.run_thread = threading.Thread(target=self.run, daemon=True)
        self.run_thread.start()

    def stop_thread(self):
        self.running = False
        if self.run_thread.is_alive():
            self.run_thread.join()

    def step(self):
        self.window.physics_canvas.update(Options['update interval'])
