"""For the purposes of this simulator, particles are objects which are rendered, and may behave in interesting ways,
but do not have mass like ForceObjects and only remain on the screen for a limited duration.

They can be used to draw debug lines, add some kind of effect, or so forth.

They are updated by the PhysicsCanvas, which they add themselves to.

To make a new particle, just extend the :class:`Particle.Particle` and overwrite the draw and transform methods.

There is no need to override the update and add_to methods.

To use a particle, initialize it, set its displacement to a vector, then call `add_to(physicsCanvas)`

"""

import Physics

import math

from tkinter import *

class Particle:
    """
    The base particle class.

    By default, for debug purposes, just shows a square at the origin that moves SE

    :param duration: The time to display the particle (s)
    :type duration: number
    """
    def __init__(self, duration=1):
        self.physics_canvas = None
        """ Particle gets a reference to PhysicsCanvas at the time add_to is called. """
        self.canvas_id = 0
        """ Id for moving on canvas """
        self.displacement = Physics.Vector(0,0)
        """ Vector from physicsCanvas origin that particle will be placed"""
        self.time_remaining = duration
        """ How much time the particle has left before it's removed from the rendered/referenced objects"""

    def update(self, interval):
        """
        Checks to see if there is time_remaining. If so, calls `self.transform`. Otherwise, removes references.

        No need to overwrite this in extending classes; overwrite `self.transform` instead.

        :param interval: Time since last update, seconds.
        :type interval: number
        """
        self.time_remaining -= interval
        if self.time_remaining <= 0:
            self.physics_canvas.canvas.delete(self.canvas_id)
            index = self.physics_canvas.particles.index(self)
            self.physics_canvas.particles.pop(index)
        else:
            self.transform(interval)

    def add_to(self, physics_canvas):
        """
        Adds this Particle to the physics canvas, appending it to the list of particles to be updated and making the
        internal reference of `self.physics_canvas`.

        Afterwards, calls `self.draw`

        No need to overwrite this in extending classes; overwrite `self.draw` instead.

        :param physics_canvas:
        :return:
        """
        physics_canvas.particles.append(self)
        self.physics_canvas = physics_canvas
        self.draw()

    def draw(self):
        """
        Draws Particle on the physics canvas.

        Overwrite this method on inheriting particles.
        """
        x = self.displacement.x + self.physics_canvas.origin_x
        y = self.displacement.y + self.physics_canvas.origin_y
        self.canvas_id = self.physics_canvas.canvas.create_rectangle(x-10,y+10,x+10,y-10, fill='black')  # e.g.

    def transform(self, interval):
        """
        Called by update. Changes the particle in some way, i.e. movement, scale, etc.

        Overwrite this method on inheriting particles

        :param interval: interval, seconds
        :type interval: number
        """
        c = self.physics_canvas.canvas
        c.scale(self.canvas_id, 0,1, 1.01, 1.01)


class Triangle(Particle):
    """
    Probably can remove this - didn't wind up using

    """
    def __init__(self, duration, x1, y1, x2, y2, x3, y3, color='blue'):
        Particle.__init__(self, duration)
        self.points = (x1, y1, x2, y2, x3, y3)
        self.color = color
        self.displacement = Physics.Vector(0, 0)

    def draw(self):
        x1, y1, x2, y2, x3, y3 = self.points
        self.canvas_id = self.physics_canvas.canvas.create_polygon(x1,y1,x2,y2,x3,y3,0,0, fill=self.color)
        origin_x = self.physics_canvas.origin_x
        origin_y = self.physics_canvas.origin_y
        self.physics_canvas.canvas.moveto(self.canvas_id, self.displacement.x + origin_x, origin_y - self.displacement.y)

    def transform(self, interval):
        pass


class Line(Particle):
    """
    Draws a Line on the canvas from a vector.

    Only required params are duration and vector.

    :param duration: How long to stay on screen (seconds)
    :type duration: number
    :param vector: A vector to calculate the line from
    :type vector: :class:`Physics.Vector`
    :param color: Color of the line, default is gray-purple
    :type color: str
    :param width: Width of line, default is 1
    :type width: int

    """
    def __init__(self, duration, vector, color='#55443C', width=1, arrow=LAST):
        Particle.__init__(self, duration)
        self.vector = vector
        self.color = color
        self.width=width
        self.displacement = Physics.Vector(0, 0)
        self.arrow = arrow

    def draw(self):
        x1 = 0
        x2 = x1 + self.vector.x
        y1 = 0
        y2 = y1 + self.vector.y
        canvas = self.physics_canvas.canvas
        self.canvas_id = canvas.create_line(x1, y1, x2, -y2, fill=self.color, width=self.width, arrow=self.arrow)
        origin_x = self.physics_canvas.origin_x
        origin_y = self.physics_canvas.origin_y
        self.physics_canvas.canvas.move(self.canvas_id, self.displacement.x + origin_x, origin_y - self.displacement.y)

    def transform(self, interval):
        pass
