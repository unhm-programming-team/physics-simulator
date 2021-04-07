from tkinter import *
from tkinter import ttk

import threading
import time

from Options import Options
import Physics
import DebugTab

import PhysicsWindow


class MainWindow:
    def __init__(self):
        self.root = Tk()  # start tkinter
        self.root.title = '2d Physics Simulator'
        self.root_frame = ttk.Frame(self.root)

        # physics canvas will create and grid the canvas
        self.center_frame = ttk.Frame(self.root_frame)
        pad = Options['canvas border width']
        # self.center_frame['style'] = 'BorderCanvas.TFrame
        # self.center_frame['padding'] = (pad,pad,pad,pad)
        self.physics_canvas = PhysicsCanvas(self, self.center_frame)

        # notebook has tabbed selections
        self.right_notebook = ttk.Notebook(self.root_frame)
        self.options_tab = OptionsTab(self.right_notebook, self)
        self.environment_tab = EnvironmentTab(self.right_notebook, self)
        self.debug_tab = DebugTab.DebugTab(self.right_notebook, self)
        self.log_tab = DebugTab.LogTab(self.right_notebook, self)
        self.log = self.log_tab.log
        self.right_notebook.add(self.options_tab, text='Options')
        self.right_notebook.add(self.environment_tab, text='Environment')
        self.right_notebook.add(self.debug_tab, text='Debug')
        self.right_notebook.add(self.log_tab, text='Log')

        # time selector handles play/pause
        self.bottom_time_frame = ttk.Frame(self.root_frame)
        self.time_selector = TimeSelector(self, self.bottom_time_frame)

        # additional windows for vector popups
        self.additional_windows = []

        self.root_frame.grid()
        self.center_frame.grid(row=0, column=1)
        self.right_notebook.grid(row=0, column=2, sticky=N)
        self.bottom_time_frame.grid(row=1, column=1)
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
        self.context_menu = Menu(self.frame)  # menu items created at the time of click

        # set canvas style from options
        self.canvas['relief'] = Options['canvas border type']
        self.canvas['bd'] = Options['canvas border width']
        self.canvas['bg'] = Options['canvas background color']

        # set click handler
        self.canvas.bind("<Button-1>", self.click_handler)
        self.canvas.bind("<Button-3>", self.context_popup)

        self.physics_objects = []
        self.interacting_forces = []
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
        for f in self.interacting_forces:
            f.update(interval)

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
        force_object.canvas_id = self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        self.window.log(f'added force object {force_object.canvas_id}')

    def move_force_object(self, force_object):
        velocity = force_object.velocity
        force_object.calculate_bounds()
        x0 = force_object.x_0 + self.origin_x
        y0 = force_object.y_0 + self.origin_y
        x1 = force_object.x_1 + self.origin_x
        y1 = force_object.y_1 + self.origin_y
        if x0 < 0 + Options['canvas left physics adjustment'] and velocity.x < 0:
            velocity.x *= -1
        if x1 > self.width + Options['canvas right physics adjustment'] and velocity.x > 0:
            velocity.x *= -1
        if y0 < 0 + Options['canvas top physics adjustment'] and velocity.y < 0:
            velocity.y *= -1
        if y1 > self.height + Options['canvas bottom physics adjustment'] and velocity.y > 0:
            velocity.y *= -1
        velocity.calculate_angles()
        self.canvas.moveto(force_object.canvas_id, x0, y0)

    def delete_physics_object(self, physics_object):
        delete_id = physics_object.canvas_id
        for i in range(0, len(self.physics_objects)-1):
            phys_object = self.physics_objects[i]
            if phys_object == physics_object:
                self.physics_objects.pop(i)
        self.canvas.delete(delete_id)
        self.window.log(f"deleted physics object {delete_id}")

    def context_popup(self, event):
        radius = Options['canvas select radius']
        left = event.x - radius
        right = event.x + radius
        top = event.y - radius
        bottom = event.y + radius
        results = self.canvas.find_overlapping(left, top, right, bottom)

        found_match = ''
        for i in range(0, len(self.physics_objects)):
            phys_obj = self.physics_objects[i]
            for j in range(0, len(results)):
                if phys_obj.canvas_id == results[j]:
                    found_match = phys_obj
                    break
            if type(found_match) != str:
                break

        if type(found_match) == str:
            self.context_menu.add_command(label='Add')
        else:
            cb = self.popup_info(found_match, event)
            self.context_menu.add_command(label='Info', command=cb)
        self.context_menu.tk_popup(event.x_root, event.y_root)
        # self.context_menu.destroy()
        self.context_menu = Menu(self.frame)

    def popup_info(self, physics_object, event):
        self.window.log('window popup called')
        po = physics_object

        def callb():
            if type(po) == Physics.ForceObject:
                fow = PhysicsWindow.ForceObjectWindow(self.window, po, event.x, event.y)
        return callb

    def click_handler(self, event):
        radius = Options['canvas select radius']
        left = event.x - radius
        right = event.x + radius
        top = event.y - radius
        bottom = event.y + radius

        results = self.canvas.find_overlapping(left, top, right, bottom)

        objects = []

        for i in range(0, len(self.physics_objects)):
            p_o = self.physics_objects[i]
            if type(p_o) == Physics.ForceObject:
                for c in range(0,len(results)):
                    target_id = results[c]
                    if p_o.canvas_id == target_id:
                        objects.append(p_o)

        for force_object in objects:
            Window.ForceObjectWindow(self.window, force_object)


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
        self.window.root.bind('<Return>', self.toggle_run_button)

    def toggle_run_button(self, event):
        if not self.running:
            self.start_thread()
        else:
            self.stop_thread()

    def run(self):
        last_time = time.time()
        while self.running:
            now_time = time.time()
            interval = now_time - last_time
            last_time = now_time
            self.update(interval)
            time.sleep(Options['update interval'])

    def start_thread(self):
        self.stop_thread()
        self.running = True
        self.run_thread = threading.Thread(target=self.run, daemon=True)
        self.run_thread.start()

    def update(self, interval):
        self.window.physics_canvas.update(interval)
        for i in range(0, len(self.window.additional_windows)):
            window = self.window.additional_windows[i]
            window.update(interval)

    def stop_thread(self):
        self.running = False
        if self.run_thread.is_alive():
            self.run_thread.join()

    def step(self):
        self.update(Options['update interval'])


class EnvironmentTab(ttk.Frame):
    def __init__(self, parent, window):
        ttk.Frame.__init__(self, parent)
        self.window = window


class OptionsTab(ttk.Frame):
    def __init__(self, parent, window):
        ttk.Frame.__init__(self, parent)
        self.window = window