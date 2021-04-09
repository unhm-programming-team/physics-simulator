
class VectorObject:
    """
    An object which stores its x,y position as a displacement vector.
    It has a width and height, and 'bounds' based on those values.
    In addition to displacement, it has vectors for velocity and acceleration.

    When it updates, it converts acceleration to velocity and velocity into displacement.

    It recalculates bounds as it needs to as the displacement vector changes for drawing.

    """
    def __init__(self):
        """
        :param physics_canvas: Vector Object can tell Physics_Canvas when it needs to move.
        :type physics_canvas: class PhysicsCanvas
        """
        self.physics_canvas = 0 # added by physics canvas at time of adding
        self.canvas_id = 0  # changed by physics canvas at time of drawing
        """Used by the tkinter canvas to reference the shape linked to this object"""
        self.width = 0
        self.height = 0
        self.x_side = 0
        self.y_side = 0
        self.side = 0
        self.x_0 = 0
        self.x_1 = 0
        self.y_0 = 0
        self.y_1 = 0
        self.displacement = Vector(0,0)
        """offset from origin"""
        self.velocity = Vector(0,0)
        """speed, m/s"""
        self.acceleration = Vector(0,0)
        """m/s^2"""


    def calculate_sides_from_width_height(self):
        """
        Will later probably calculate different sizes for rects at least

        Mutating function that sets self.side from self.width/2, probably only needs to be called once in particular circumstances.
        """
        self.side = self.width/2

    def update(self, interval):
        """
        Gets a new vector equal to multiplying acceleration by Velocity and adds it
        to the velocity, mutating the velocity vector. v = at + v_0
        Does the same for displacement. s = vt + s_0
        Tells physicsCanvas to move the rendering of the oval.
        :param interval: The time since last update.
        :type interval: seconds
        """
        self.velocity.add(self.acceleration.scale_make(interval))
        self.displacement.add(self.velocity.scale_make(interval))
        self.physics_canvas.move_physics_object(self)
        if not self.check_collision(interval):
            self.displacement.add(self.velocity)
            self.physics_canvas.move_physics_object(self)

    def collide(self, other_object, my_next_displacement, other_next_displacement, interval):
        """
        Called by the check_collision function. Next displacements calculated there are passed as parameters to avoid
        redundant calculations.

        :param other_object: The colliding object
        :type other_object: ForceObject
        :param my_next_displacement: Displacement vector that would realize if no collision
        :type my_next_displacement: Vector
        :param other_next_displacement: Displacement vector for other object that would realize if no collision
        :type other_next_displacement: Vector
        :param interval: Interval of distance move, second(s)
        :type interval: number
        """
        line1 = Utility.get_line(self.displacement.x, self.displacement.y, my_next_displacement.x, my_next_displacement.y)
        line2 = Utility.get_line(other_object.displacement.x, other_object.displacement.y, other_next_displacement.x, other_next_displacement.y)
        collision_x, collision_y = Utility.find_intersecting_point(line1, line2)  # point of collision
        if other_object.displacement.x < collision_x:  # these ifs put colliders on appropriate side
            other_object.displacement.x = collision_x - other_object.side
            self.displacement.x = collision_x + self.side
        elif other_object.displacement.x > collision_x:
            other_object.displacement.x = collision_x + other_object.side
            self.displacement.x = collision_x - self.side
        if other_object.displacement.y < collision_y:
            other_object.displacement.y = collision_y - other_object.side
            self.displacement.y = collision_y + self.side
        elif other_object.displacement.y > collision_y:
            other_object.displacement.y = collision_y + other_object.side
            self.displacement.y = collision_y - self.side
        self.displacement.calculate_angles()
        other_object.displacement.calculate_angles()
        self.velocity = Vector(0,0)
        # self.displacement.add(self.velocity)
        other_object.velocity = Vector(0,0)
        self.physics_canvas.move_physics_object(self)

    def check_collision(self, interval):
        """
        The way collision is checked is that the next displacement from the velocity is calculated.

        For each other extant physics object on the canvas, the next displacement from velocity is calculated.

        If the lines between the displacements cross, the vectors have 'collided'.

        This function returns True or False and is used in the update function. If collision doesn't happen,
        the update function handles simple movement.

        :param interval:
        :return: Whether collision happened
        :rtype: bool
        """
        next_displacement = self.displacement.add_make(self.velocity) # add radius/side length here?
        for p in self.physics_canvas.physics_objects:
            if p != self:
                other_next_displacement = p.displacement.add_make(p.velocity)
                y_cross = False
                if self.displacement.y <= p.displacement.y:
                    if next_displacement.y + self.y_side >= other_next_displacement.y - p.y_side:
                        y_cross = True
                elif self.displacement.y >= p.displacement.y:
                    if next_displacement.y - self.y_side <= other_next_displacement.y + p.y_side:
                        y_cross = True
                x_cross = False
                if self.displacement.x <= p.displacement.x:
                    if next_displacement.x + self.x_side >= other_next_displacement.x - p.x_side:
                        x_cross = True
                elif self.displacement.x >= p.displacement.x:
                    if next_displacement.x - self.x_side <= other_next_displacement.x + p.x_side:
                        x_cross = True

                if x_cross and y_cross:
                    self.collide(p, next_displacement, other_next_displacement, interval)
                    return True
        return False


class MassObject(VectorObject):
    """
    Extends VectorObject, so it has displacement, velocity, and acceleration.

    Also has a mass and a material.
    It calculates its volume(m^3) and side length(m) from its material density(kg/m^3) and mass(kg).

    :param physics_canvas: The PhysicsCanvas object where this will be added
    :type physics_canvas: :class:`Ui.PhysicsCanvas`
    :param material: Used to calculate dimensions based on density and mass
    :type material: Substance.Material
    :param mass: kilograms
    :type mass: number
    """
    def __init__(self, material=Substance.Material(), mass=10):
        VectorObject.__init__(self)
        self.material = material
        self.mass = mass
        self.volume = mass / self.material.density
        self.side = self.volume**(1/3)
        self.width = self.side
        self.height = self.side


class ForceObject:
    """
    An object which
    """
    def __init__(self, material=Substance.Material(), mass=1000):
        """
        :type physics_canvas:PhysicsCanvas
        :type material: Substance.Material
        :type mass: number
        """
        MassObject.__init__(self, material, mass)
        self.forces = []
        """ Currently active forces affecting this object """
        self.dependent_force_generators = []
        """ Force generators like :class:`Physics.GravitationalForceGenerator`"""
        self.net_force_vector = Vector(0,0)

    def update(self, interval):
        """
        Gets a new vector equal to multiplying acceleration by Velocity and adds it
        to the velocity, mutating the velocity vector. :math:`v = at + v_0`
        Does the same for displacement. :math:`s = vt + s_0`
        Tells physicsCanvas to move the rendering of the oval.
        :param interval: The time since last update.
        :type interval: number
        """
        self.net_force_vector = Vector(0, 0)
        non_expired_forces = []
        for i in range(0, len(self.forces)):  # get the net force for this interval
            force = self.forces[i]
            force.update(interval)
            self.net_force_vector.add(force)
            if force.remaining > 0:
                non_expired_forces.append(force)
        self.forces = non_expired_forces
        self.acceleration = Vector(self.net_force_vector.angle, self.net_force_vector.magnitude/self.mass)
        self.velocity.add(self.acceleration)
        if not self.check_collision(interval):
            self.displacement.add(self.velocity)
            self.physics_canvas.move_physics_object(self)

    def clear_forces(self):
        """
        Clears forces from self.dependent_force_generators by calling remove() on each
        """
        for f in self.dependent_force_generators:
            f.remove()