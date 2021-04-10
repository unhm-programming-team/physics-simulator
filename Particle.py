import Physics

import math

class Particle:
    def __init__(self, duration=1):
        self.physics_canvas = None
        self.canvas_id = 0
        self.displacement = Physics.Vector(0,0)
        self.time_remaining = duration

    def update(self, interval):
        self.time_remaining -= interval
        if self.time_remaining <= 0:
            self.physics_canvas.canvas.delete(self.canvas_id)
            index = self.physics_canvas.particles.index(self)
            self.physics_canvas.particles.pop(index)
        else:
            self.transform(interval)

    def add_to(self, physics_canvas):
        physics_canvas.particles.append(self)
        self.physics_canvas = physics_canvas
        self.draw()

    def draw(self):
        """
        Draws it on the physics canvas, called by `self.add_to` once Particle is added in other ways.

        Overwrite this method on inheriting particles.
        """
        x = self.displacement.x + self.physics_canvas.origin_x
        y = self.displacement.y + self.physics_canvas.origin_y
        self.canvas_id = self.physics_canvas.canvas.create_rectangle(x-10,y+10,x+10,y-10, fill='black')  # e.g.

    def transform(self, interval):
        """
        Called by update once duration time is handled

        Overwrite this method on inheriting particles

        :param interval: interval, seconds
        :type interval: number
        """
        c = self.physics_canvas.canvas
        c.scale(self.canvas_id, 0,0, 1.01, 1.01)


class Triangle(Particle):
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
    def __init__(self, duration, x1, y1, x2, y2, color='#55443C'):
        Particle.__init__(self, duration)
        self.points = (x1, y1, x2, y2)
        self.color = color
        self.displacement = Physics.Vector(0, 0)

    def draw(self):
        x1, y1, x2, y2 = self.points
        self.canvas_id = self.physics_canvas.canvas.create_line(x1,y1,x2,y2, fill=self.color)
        origin_x = self.physics_canvas.origin_x
        origin_y = self.physics_canvas.origin_y
        self.physics_canvas.canvas.moveto(self.canvas_id, self.displacement.x + origin_x, origin_y - self.displacement.y)

    def transform(self, interval):
        pass
