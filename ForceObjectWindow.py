from tkinter import *
from tkinter import ttk

import math

from Options import Options


class ForceObjectWindow:
    def __init__(self, window, force_object):
        self.root = Tk()  # start a new window
        self.root.geometry("200x200")
        self.window = window
        self.force_object = force_object
        self.root.title = 'ForceObject' + str(force_object.canvas_id)
        self.window.additional_windows.append(self)
        self.time_elapsed_since_last_update = 0

        id_label = ttk.Label(self.root, text='id: '+str(force_object.canvas_id))
        id_label.grid(row=0, column=0, sticky=W)
        material_text = f"{force_object.material.name}, {force_object.mass}kg"
        material_label = ttk.Label(self.root, text=material_text)
        material_label.grid(row=1, columnspan=4, sticky = W)
        x_label = ttk.Label(self.root, text='x: ')
        x_label.grid(row=2, column=0, sticky=E)
        self.x_val = ttk.Label(self.root)
        self.x_val.grid(row=2, column=1, sticky=W)
        y_label = ttk.Label(self.root, text='y: ')
        y_label.grid(row=2, column=2, sticky=E)
        self.y_val = ttk.Label(self.root)
        self.y_val.grid(row=2, column=3, sticky=W)
        self.velocity_label = ttk.Label(self.root)
        self.velocity_label.grid(row=3, column=0, columnspan=4, sticky=W)
        self.acceleration_label = ttk.Label(self.root)
        self.acceleration_label.grid(row=4, column=0, columnspan=4, sticky=W)
        self.net_force_label = ttk.Label(self.root)
        self.net_force_label.grid(row=5, column=0, columnspan=4, sticky=W)
        self.update(Options['object popup update interval'])
        # add additional protocol to window close so it removes from open window list
        self.root.protocol("WM_DELETE_WINDOW", self.del_win)
        self.root.mainloop()

    def update(self, interval):
        self.time_elapsed_since_last_update += interval
        if self.time_elapsed_since_last_update >= Options['object popup update interval']:
            self.root.lift()
            displacement = self.force_object.displacement
            x_text = f"{round(displacement.x)} m"
            y_text = f"{round(displacement.y)} m"
            self.x_val['text'] = x_text
            self.y_val['text'] = y_text
            velocity = self.force_object.velocity
            velocity_text = f"velocity: {round(velocity.magnitude)} m/s, {round(math.degrees(velocity.angle))} deg"
            self.velocity_label['text'] = velocity_text
            acceleration = self.force_object.acceleration
            acceleration_text = f"acceleration: {round(acceleration.magnitude)} m/s^2, {round(math.degrees(acceleration.angle))} deg"
            self.acceleration_label['text'] = acceleration_text
            net_force = self.force_object.net_force_vector
            net_force_text = f"net_force: {round(net_force.magnitude)} N, {round(math.degrees(net_force.angle))} deg"
            self.net_force_label['text'] = net_force_text
            self.time_elapsed_since_last_update = 0

    def del_win(self):
        print(len(self.window.additional_windows))
        index = self.window.additional_windows.index(self)
        self.window.additional_windows.pop(index)
        print(len(self.window.additional_windows))
        self.root.destroy()

