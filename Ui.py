from tkinter import *
from tkinter import ttk

import threading
import time

from Options import Options
import Physics
import DebugTab
import Utility

import PhysicsWindow


class MainWindow:
    """
    MainWindow serves as the entry point to the application. It builds the PhysicsCanvas, the right side Notebook, and the tabs in that notebook. Many other objects contain references to MainWindow (usually simply as self.window) in order that they can access all other parts of the application.
    """
    def __init__(self):
        self.root = Tk()  # start tkinter
        """The Tkinter root"""
        self.root.title = '2d Physics Simulator'
        self.root_frame = ttk.Frame(self.root)
        """The root frame"""

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
        """Simply call window.log(message) to log directly to the log tab"""
        self.right_notebook.add(self.options_tab, text='Options')
        self.right_notebook.add(self.environment_tab, text='Environment')
        self.right_notebook.add(self.debug_tab, text='Debug')
        self.right_notebook.add(self.log_tab, text='Log')

        # time selector handles play/pause
        self.bottom_time_frame = ttk.Frame(self.root_frame)
        self.time_selector = TimeSelector(self, self.bottom_time_frame)

        # additional windows for vector popups
        self.additional_windows = []
        """Extant instances from PhysicsWindows module"""

        self.root_frame.grid()
        self.center_frame.grid(row=0, column=1)
        self.right_notebook.grid(row=0, column=2, sticky=N)
        self.bottom_time_frame.grid(row=1, column=1)
        Utility.center(self.root)
        self.root.mainloop()


class PhysicsCanvas:
    """
    Controls the drawing of PhysicsObjects and inheriting classes on a canvas

    Sets origin to center and calculates actual pixel coordinates from object displacement vectors.
    """
    def __init__(self, window, parent_frame):
        self.window = window
        self.frame = parent_frame
        self.width = Options['canvas width']
        self.height = Options['canvas height']
        self.scale = Options['zoom']
        """Not yet implemented"""
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

        # set click handlers
        self.canvas.bind("<Button-3>", self.context_popup)

        self.physics_objects = []
        """Instances from e.g., :class:`Physics.ForceObject` that need to be have update called"""
        self.interacting_forces = []
        """Instances from, e.g. :class:`Physics.GravitationalForceGenerator` that need to be have update called"""
        self.particles = []
        self.new_physics_object_plugins = []
        """These are functions. Each will have func(physics_object) called on it when a new object is added.
            You can generate a callback to go in this list to add functionality to new objects that are added
        """
        self.canvas.grid()
        self.draw_cartesian()

    def draw_cartesian(self):
        """
        Draw axis lines.
        """
        color = Options['canvas axis color']
        self.canvas.create_line(0, self.origin_y, self.width, self.origin_y, fill=color)
        self.canvas.create_line(self.origin_x, 0, self.origin_x, self.height, fill=color)

    def add_physics_object(self, physics_object):
        """
        This replaced redundant methods add_force_object, add_vector_object, etc. in the refactor. Those classes were also all merged into PhysicsObject.

        Draws a rectangle to represent the physicsObject on the canvas.

        Adds a reference to the new PhysicsObject in self.physicsObjects

        Sets physics_object.canvas_id to the canvas id (integer) resulting from drawing a shape

        Sets physics_object.physics_canvas to a reference to this PhysicsCanvas

        :param physics_object: A physics object to draw on the canvas
        :type physics_object: :class:`Physics.PhysicsObject`
        """
        if hasattr(physics_object, 'material'):
            color = physics_object.material.color
        else:
            color = 'blue'
        x0 = physics_object.displacement.x - physics_object.side + self.origin_x
        x1 = physics_object.displacement.x + physics_object.side + self.origin_x
        y0 = physics_object.displacement.y - physics_object.side + self.origin_y
        y1 = physics_object.displacement.y + physics_object.side + self.origin_y
        # down the line, the physics object should draw itself
        physics_object.canvas_id = self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        physics_object.physics_canvas = self
        self.physics_objects.append(physics_object)

        for plugin in self.new_physics_object_plugins:
            plugin(physics_object)

        self.move_physics_object(physics_object)

    def update(self, interval):
        """
        Passes update to interval to self.physics_objects and self.interacting_forces
        :param interval: time in seconds
        :type interval: number
        """
        for o in self.physics_objects:
            o.update(interval)
        for f in self.interacting_forces:
            f.update(interval)
        for p in self.particles:
            p.update(interval)

    def move_physics_object(self, physics_object):
        """
        Called by :class:`Physics.ForceObject` when they need to move.

        Checks the displacement vector of the parameter object, calculates where that should appear on the canvas,
        then moves the rendering to the appropriate pixel x,y.

        Currently, this is a little buggy and needs to be reworked. Positive and negative y are not accounted for correctly.

        :param physics_object: An object with a displacement vector that wants to move
        :type physics_object: extends :class:`Physics.PhysicsObject`
        """
        velocity = physics_object.velocity
        acceleration = physics_object.acceleration
        dx = physics_object.displacement.x
        dy = physics_object.displacement.y
        side = physics_object.side
        x0 = dx - side
        x1 = dx + side
        y0 = dy - side
        y1 = dy + side
        if x0 < self.min_x + Options['canvas left physics adjustment'] and velocity.x < 0.001:
            velocity.x *= -1
        elif x1 > self.max_x + Options['canvas right physics adjustment'] and velocity.x > 0.001:
            velocity.x *= -1
        if y0 < self.min_y + Options['canvas top physics adjustment'] and velocity.y < 0.001:
            velocity.y *= -1
        elif y1 > self.max_y - Options['canvas bottom physics adjustment'] and velocity.y > 0.001:
            velocity.y *= -1
        velocity.calculate_angles()
        acceleration.calculate_angles()
        new_x = physics_object.displacement.x + self.origin_x - side
        new_y = self.origin_y - (physics_object.displacement.y + side)
        self.canvas.moveto(physics_object.canvas_id, new_x, new_y)

    def get_physics_object_from_id(self, id):
        """
        Returns the object with canvas id equal to id
        :param id: A canvas id
        :type id: int
        :return: :class:`Physics.PhysicsObject`
        """
        for p in self.physics_objects:
            if p.canvas_id == id:
                return p

    def delete_physics_object(self, physics_object):
        """
        Deletes an object and removes its rendering from the canvas.

        :param physics_object: Object to delete
        :type physics_object: extends :class:`Physics.PhysicsObject`
        :return:
        """
        delete_id = physics_object.canvas_id
        for i in range(0, len(self.physics_objects)-1):
            phys_object = self.physics_objects[i]
            if phys_object == physics_object:
                self.physics_objects.pop(i)
        self.canvas.delete(delete_id)
        self.window.log(f"deleted physics object {delete_id}")

    def context_popup(self, event):
        """
        Pops a right click option menu near the user click.

        If there is a ForceObject within Option['click radius'] of the click, the option menu is populated with
        entries relating to that object. Otherwise, the entry for adding a new object is in the menu.

        :param event: Mouse click event
        """
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
            cb = self.popup_add(event)
            self.context_menu.add_command(label='Add', command=cb)
        else:
            cb = self.popup_info(found_match, event)
            self.context_menu.add_command(label='Info', command=cb)
        self.context_menu.tk_popup(event.x_root, event.y_root)
        # self.context_menu.destroy()
        self.context_menu = Menu(self.frame)

    def popup_add(self, event):
        """
        Generates a callback function for use with the context menu, to popup a new window for adding a PHysics Object at the click location.
        :param event: MouseEvent
        :return: A callback function to be attached as a UI command
        :rtype: Function
        """
        def callb():
            PhysicsWindow.AddObjectWindow(self.window, event)
        return callb


    def popup_info(self, force_object, event):
        """
        Generates a callback function for use with the context menu, so the ForceObject is linked to the PhysicsObjectWindow when it is created.

        :param force_object: The physics object to link
        :type force_object: :class:`Physics.ForceObject`
        :param event: Mouse click event
        :return: A callback to pass to the menu entry as the command
        :rtype: Function
        """
        self.window.log('window popup called')
        po = force_object

        def callb():
            if type(po) == Physics.PhysicsObject:
                fow = PhysicsWindow.PhysicsObjectWindow(self.window, po, event.x, event.y)
        return callb


class TimeSelector:
    """
    Handles pause, step, and play buttons at the bottom of the UI.

    Calculates update time and sends it to window.physics_canvas for updating.

    :param window: The main entry of the application
    :type window: :class:`Ui.Window`
    :param parent_frame: The frame where these components should be located
    :type frame: Tkinter.Frame
    """
    def __init__(self, window, parent_frame):
        self.window = window
        self.frame = parent_frame
        self.pause_button = Button(self.frame, text='Pause', command=self.stop_thread)
        self.start_button = Button(self.frame, text='Play', command=self.start_thread)
        self.step_button = Button(self.frame, text='Step', command=self.step)

        self.run_thread = threading.Thread(target=self.run, daemon=True)
        """Main program time loop"""

        self.running = False
        """Set True when program is running"""

        self.pause_button.grid(column=0, row=0)
        self.start_button.grid(column=1, row=0)
        self.step_button.grid(column=2, row=0)
        self.window.root.bind('<Return>', self.toggle_run_button)

    def toggle_run_button(self, event):
        """
        Bound to the Enter keyboard key to toggle whether time is running
        :param event: Key event, not used
        """
        if not self.running:
            self.start_thread()
        else:
            self.stop_thread()

    def run(self):
        """
        Run by the program thread(s), not called directly!

        Sleeps for approximately `Options.Options['update interval']` seconds, then calls self.update(interval) with
        the interval being the actual time passed since the last update was called. :return:
        """
        last_time = time.time()
        while self.running:
            now_time = time.time()
            interval = now_time - last_time
            last_time = now_time
            self.update(interval)
            time.sleep(Options['update interval'])

    def start_thread(self):
        """
        Stops the old thread in case it's running, then sets self.run_thread to a new thread and starts it.
        """
        self.stop_thread()
        self.running = True
        self.run_thread = threading.Thread(target=self.run, daemon=True)
        self.run_thread.start()

    def update(self, interval):
        """
        Tells :class:`Ui.PhysicsWindow` to update with interval amount.

        Also tells each window in `MainWindow.additional_windows` to update by interval amount.

        :param interval: Time to update in seconds
        :type interval: number
        """
        self.window.physics_canvas.update(interval)
        for i in range(0, len(self.window.additional_windows)):
            window = self.window.additional_windows[i]
            window.update(interval)

    def stop_thread(self):
        """
        Stops the current self.run_thread and joins it (if its alive)

        Also sets self.running to false
        :return:
        """
        self.running = False
        if self.run_thread.is_alive():
            self.run_thread.join()

    def step(self):
        """
        Calls self.update(Options['update interval']), 'stepping' the time that would pass in 1 'frame'
        """
        self.update(Options['update interval'])


class EnvironmentTab(ttk.Frame):
    """
    Will have environment options like grav, air resistance, maybe scaling
    """
    def __init__(self, parent, window):
        ttk.Frame.__init__(self, parent)
        self.window = window
        self.clear_button = ttk.Button(self, text="Clear", command=self.clear_press)

        self.is_gravity = BooleanVar()
        gravity_check = ttk.Checkbutton(self, text="gravity", variable=self.is_gravity, command=self.toggle_gravity)
        self.is_gravity.set(Options['gravity'])
        self.gravity_accel = IntVar()
        self.gravity_accel.set(9.8)

        self.is_air = BooleanVar()
        air_check = ttk.Checkbutton(self, text="air resistance", variable=self.is_air, command=self.toggle_air)
        self.is_air.set(Options['air resistance'])

        self.clear_button.grid(column=0, row=0)
        gravity_check.grid(column=0, row=1,sticky=W)
        air_check.grid(column=0,row=2, sticky=W)

    def toggle_air(self):
        """
        Creates drag forces for objects

        Drag acts opposite to the direction of motion
        """
        physics_canvas = self.window.physics_canvas
        if self.is_air.get(): # checkbox changes before command is called
            for p_object in physics_canvas.physics_objects:
                # make a drag force
                p_object._drag = Physics.DragForce(p_object)
                p_object.forces.append(p_object._drag)
            physics_canvas.new_physics_object_plugins.append(self.set_drag_for_new_physics_object)
        else:
            for p_object in physics_canvas.physics_objects:
                if hasattr(p_object, '_drag'):
                    drag_force = p_object._drag
                    for f in p_object.forces:
                        if f == drag_force:  # remove
                            i = p_object.forces.index(f)
                            p_object.forces.pop(i)
                            break
            for plug in physics_canvas.new_physics_object_plugins:
                if plug == self.set_drag_for_new_physics_object:
                    i = physics_canvas.new_physics_object_plugins.index(plug)
                    physics_canvas.new_physics_object_plugins.pop(i)

    def toggle_gravity(self):
        physics_canvas = self.window.physics_canvas
        if self.is_gravity.get(): # checkbox changes before command is called
            for p_object in physics_canvas.physics_objects:
                p_object._grav_force = Physics.Force.make_directional_force('S', self.gravity_accel.get()*p_object.mass)
                p_object._grav_force.constant = True
                p_object.forces.append(p_object._grav_force)
            physics_canvas.new_physics_object_plugins.append(self.set_grav_for_new_physics_object)
        else:
            for p_object in physics_canvas.physics_objects:
                if hasattr(p_object, '_grav_force'):
                    grav_force = p_object._grav_force
                    for f in p_object.forces:
                        if f == grav_force:
                            i = p_object.forces.index(f)
                            p_object.forces.pop(i)
                            break
            for plug in physics_canvas.new_physics_object_plugins:
                if plug == self.set_grav_for_new_physics_object:
                    i = physics_canvas.new_physics_object_plugins.index(plug)
                    physics_canvas.new_physics_object_plugins.pop(i)

    def set_grav_for_new_physics_object(self, physics_object):
        """
        Append this function to :class:`PhysicsCanvas.new_physics_object_plugins`

        :param physics_object: A new physics object
        :type :class:`Physics.PhysicsObject`
        """
        if self.is_gravity.get():
            physics_object._grav_force = Physics.Force.make_directional_force('S', self.gravity_accel.get()*physics_object.mass)
            physics_object._grav_force.constant = True
            physics_object.forces.append(physics_object._grav_force)

    def set_drag_for_new_physics_object(self, physics_object):
        """
        Append this function to :class:`PhysicsCanvas.new_physics_object_plugins`

        :param physics_object: A new physics object
        :type :class:`Physics.PhysicsObject`

        """
        if self.is_air.get():
            physics_object._drag = Physics.DragForce(physics_object)
            physics_object.forces.append(physics_object._drag)



    def clear_press(self):
        """
        Deletes all refs in physics Canvas
        Closes all hanging windows

        Clears canvas of extant physics objects

        Removes interacting forces
        """

        for win in self.window.additional_windows:
            win.del_win()

        pos = self.window.physics_canvas.physics_objects
        self.window.physics_canvas.physics_objects = []

        for obj in pos:
            self.window.physics_canvas.canvas.delete(obj.canvas_id)

        for force in self.window.physics_canvas.interacting_forces:
            force.remove()

        for particle in self.window.physics_canvas.particles:
            self.window.physics_canvas.canvas.delete(particle.canvas_id)


class OptionsTab(ttk.Frame):
    """
    Will have UI components for changing values such as in Options.Options

    """
    def __init__(self, parent, window):
        ttk.Frame.__init__(self, parent)
        self.window = window
