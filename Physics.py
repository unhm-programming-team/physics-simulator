"""Physics contains the objects relating to mathematical calculations, such as Vectors, Forces, and PhysicsObjects.
There are no UI components in this module.

All displacements are calculated on an abstract plane - :class:`Ui.PhysicsCanvas` is responsible for translating to
canvas coordinates.

One semi-exception - PhysicsObjects handle their own collision detection, and they do that by referencing the
collection of PhysicsObjects in PhysicsCanvas.

All the physics logic and calculation should be handled here.
 """

import math

import Substance, Utility


class Vector:
    """
    Represents direction and magnitude. Vectors can be broken into x and y components and reassembled from those
    components.

    :param angle: The angle, in radians
    :type angle: number
    :param magnitude: The magnitude of the Vector
    :type magnitude: number
    """
    def __init__(self, angle, magnitude):
        """
        constructor
        """
        self.angle = angle
        self.magnitude = magnitude
        self.y = 0
        self.x = 0
        self.calculate_components()

    def calculate_components(self):
        """
        Calculates components from angle and magnitude.

        :math:`y = \\text{vector}_\\text{mag} * \\sin{\\theta}`

        :math:`x = \\text{vector}_\\text{mag} * \\cos{\\theta}`

        """
        self.y = self.magnitude * math.sin(self.angle)
        self.x = self.magnitude * math.cos(self.angle)

    def calculate_angles(self):
        """
        Calculates angle and mag from components.

        :math:`\\theta= \\arctan{(\\frac{y}{x})}`

        :math:`\\text{mag} = \\sqrt{x^2+y^2}`

        """
        y = self.y
        x = self.x
        self.angle = math.atan2(y, x)
        self.magnitude = math.sqrt(x*x + y*y)

    @staticmethod
    def make_vector_from_components(x, y):
        """
        Static: Create a new Vector from x and y values.
        :param x: The x component
        :type x: number
        :param y: The y component
        :type y: number
        :returns: A brand new Vector
        :rtype: Vector
        """
        angle = math.atan2(y, x)
        magnitude = math.sqrt(x*x + y*y)
        return Vector(angle, magnitude)

    def add_make(self, other_vector):
        """
        Use this to have a new vector return from the addition and the input vectors to be unchanged.

        No existing Vector will mutate.

        :param other_vector: A vector to add to this one.
        :type other_vector: Vector
        :returns: A brand new Vector
        :rtype: Vector
        """
        new_x = other_vector.x + self.x
        new_y = other_vector.y + self.y
        return Vector.make_vector_from_components(new_x, new_y)

    def subtract_make(self, other_vector):
        """
        Use this to have a new vector return from the subtraction and the input vectors to be unchanged.

        No existing Vector will mutate.

        :param other_vector: A vector to subtract FROM this one.
        :type other_vector: Vector
        :returns: A brand new Vector
        :rtype: Vector
        """
        new_x = self.x - other_vector.x
        new_y = self.y - other_vector.y
        return Vector.make_vector_from_components(new_x,new_y)

    def add(self, other_vector):
        """
        Use this to MUTATE this Vector by adding another Vector to it.

        The other Vector will be unchanged.

        :param other_vector: A vector to add to this one.
        :type other_vector: Vector
        """
        self.x += other_vector.x
        self.y += other_vector.y
        self.calculate_angles()

    def subtract(self, other_vector):
        """
        Use this to MUTATE this Vector by subtracting another Vector from it.

        The other Vector will be unchanged.

        :param other_vector: A vector to subtract from this one.
        :type other_vector: Vector
        """
        self.x -= other_vector.x
        self.y -= other_vector.y
        self.calculate_angles()

    def rotate(self, radians):
        """
        Mutates this Vector by adding radians to its angle and recalculating its components.

        :param radians: Radians to add to this Vector's angle.
        :type radians: number
        """
        new_angle = self.angle + radians
        twoPi = math.pi * 2
        if new_angle > twoPi:
            new_angle = -twoPi
        else:
            new_angle = twoPi - new_angle
        self.angle = new_angle
        self.calculate_components()

    def scale(self, scalar):
        """
        Mutates this Vector by multiplying its magnitude by the scalar.

        :param scalar: Scalar to multiply this Vector's angle by.
        :type scalar: number
        """
        self.magnitude *= scalar
        self.calculate_components()

    def scale_make(self, scalar):
        """
        Creates a new Vector of a magnitude equal to this Vector's magnitude multiplied by the scalar,
        and returns the new Vector..

        :param scalar: Scalar to multiply this Vector's angle by.
        :type scalar: number
        :returns: A brand new Vector
        :rtype: Vector
        """
        self.magnitude *= scalar
        new_magnitude = self.magnitude * scalar
        return Vector(self.angle, new_magnitude)

    def normal_make(self):
        """
        Returns a new magnitude 1 vector in the same angle.

        :return: new Vector
        :rtype: Vector
        """
        x = self.x / self.magnitude
        y = self.y / self.magnitude
        return Vector.make_vector_from_components(x, y)

    @staticmethod
    def make_directional_vector(direction='S', magnitude=1):
        """
        Static method which creates a directional Vector from compass coordinates passed as a character.

        Direction string controls vector angle.
        I.e.:
        'E': 0 radians (0 degrees)
        'W': 3.1415 radians (180 degrees)

        Valid directions are e,ne,n,nw,w,sw,s,se

        :param direction: character for direction
        :type direction: str
        :param magnitude: vector magnitude
        :type magnitude: number
        """
        angle = 0
        case = direction.upper()
        if case == 'N':
            angle = 1.5707963267948966  # don't know if this improves processing time
        elif case == 'NW':
            angle = 2.356194490192345  # but i wanted to write the radians out
        elif case == 'W':
            angle = 3.141592653589793
        elif case == 'SW':
            angle = 3.9269908169872414
        elif case == 'S':
            angle = 4.71238898038469
        elif case == 'SE':
            angle = 5.497787143782138
        elif case == 'E':
            angle = 0
        elif case == 'NE':
            angle = 0.7853981633974483
        return Vector(angle, magnitude)


class Force(Vector):
    """
    A force which operates over time, executing a single force on the object once per sec.

    If constant is true, the force does not deplete and will continue acting on the object.

    PhysicsObjects have lists of forces currently operating on them. As the PhysicsObject updates, it gets a Vector
    representing a force for each force acting on it. That force is scaled based on the time of the update interval.
    It also reduces the 'remaining' attribute of the Force until the Force is depleted.

    :param angle: Angle in radians
    :type angle: number
    :param magnitude: Magnitude in Newtons (per second)
    :type magnitude: number
    :param duration: Seconds force is exerted for
    :type duration: number
    :param constant: Whether force depletes or not
    :type constant: bool
    """
    def __init__(self, angle, magnitude, duration=1.0, constant=False):
        Vector.__init__(self, angle, magnitude)
        self.force_magnitude = magnitude
        self.remaining = duration
        self.constant = constant

    @staticmethod
    def make_directional_force(direction, magnitude, duration=1.0, constant=False):
        """
        Similar to `Vector.make_directional_vector`, creates a force in a cardinal direction.

        :param direction: N,S,E,W,NE,SE,NW,SW
        :type direction: str
        :param magnitude: In Newtons
        :type magnitude: number
        :param duration: In seconds
        :type duration: number
        :param constant: Whether force depletes
        :type constant: boolean
        :return: A new force
        :rtype: Force
        """
        vec = Vector.make_directional_vector(direction, magnitude)
        return Force(vec.angle, vec.magnitude, duration, constant)

    def update(self, interval):
        """
        Scales the current vector magnitude to the interval, so that `self.force_magnitude` is delivered each second;
        if updates occur more frequently than once a second, this causes this forces temporary magnitude to be lower
        to account for that.

        :param interval: Time since last update, in seconds.
        :type interval: number

        """
        if interval < self.remaining:
            interval = self.remaining - interval
        if self.remaining > 0:
            self.magnitude = self.force_magnitude * interval
            self.calculate_components()
            self.remaining -= interval
        if self.constant:
            self.remaining = 1


class GravitationalForceGenerator:
    """
    Connects two objects together with 'gravity'. Currently not accurately implemented, because planetary scales make
    for poor visibility on the UI.

    Three objects keep a reference to a gravitational force; the `class:Ui.PhysicsCanvas` object and each
    `class:Physics.ForceObject` that are connected with the gravity.

    When remove() is called on a GravitationalForceGenerator, it removes each of these references so it will no
    longer be updated.

    GraviationalForceGenerator is updated directly by  `class:Ui.PhysicsCanvas`; each update, it calculates the
    appropriate graviational pull for its two reference ForceObjects, then adds a force of the appropriate angle and
    magnitude to their force lists.

    :param planet: An object to connect with gravity
    :type planet: ForceObject
    :param moon: An object to connect with gravity
    :type moon: ForceObject

    """
    def __init__(self, planet, moon):
        self.planet = planet
        self.moon = moon
        self.planet.dependent_force_generators.append(self)
        self.moon.dependent_force_generators.append(self)
        self.grav_sum = planet.mass * moon.mass # omitted - the gravitational constant
        self.remaining = 1

    def update(self, interval):
        """
        Gets the location of self.planet and self.moon, figures out F_G between them, then adds opposite forces to
        each one reduced by the interval.

        :math:`F_G = \\frac{Gm_1m_2}{r^2}`

        :param interval: Update time, seconds :type interval: number
        """
        planet_off_x = self.moon.displacement.x - self.planet.displacement.x
        planet_off_y = self.moon.displacement.y - self.planet.displacement.y
        planet_vector = Vector.make_vector_from_components(planet_off_x, planet_off_y)
        reversed_vector = Vector.make_vector_from_components(planet_off_x*-1, planet_off_y*-1)
        force_magnitude = (1000000/planet_vector.magnitude)*interval # not accurate gravitational force
        self.planet.forces.append(Force(planet_vector.angle, force_magnitude))
        self.moon.forces.append(Force(reversed_vector.angle, force_magnitude))

    def remove(self):
        moon_forces = self.moon.dependent_force_generators
        moon_i = moon_forces.index(self)
        planet_forces = self.planet.dependent_force_generators
        planet_i = planet_forces.index(self)
        moon_forces.pop(moon_i)
        planet_forces.pop(planet_i)
        main_list = self.planet.physics_canvas.interacting_forces
        main_i = main_list.index(self)
        main_list.pop(main_i)


class PhysicsObject:
    """
    An object which has vectors for acceleration, velocity, and displacement.

    Abstracts the physics calculations - :class:`Ui.PhysicsCanvas` is responsible for the rendering, and translating
    the displacement of the PhysicsObject into the Tkinter Canvas coordinate space.

    Each update, it determines how much force should be applied based on the interval and the list of forces
    currently affecting this object.

    From the net force and mass, it calculates acceleration. From the acceleration, it calculates velocity. From
    velocity, displacement is calculated.

    :math:`F_{net} = \\sum{F}\\text{   Newtons}`

    :math:`a = \\frac{F_\\text{net}}{m}\\text{   m/s}^2`

    :math:`v = at + v_0 \\text{   m/s}`

    :math:`s = vt + s_0 = \\frac{1}{2}at^2+v_0t+s_0 \\text{   m}`

    :param material: The material from :class:`Substance.Material` used in this object. Determines its color and size based on the material density.

    :type material: :class:`Substance.Material`

    :param mass: The mass of the object. (kg)

    :type mass: Number

    """
    def __init__(self, material, mass):
        self.physics_canvas = None  # added by physics canvas at time of adding
        """Reference to canvas added when object rendered on canvas"""
        self.canvas_id = None  # set by physics canvas at time of drawing
        """Used by the tkinter canvas to reference the shape linked to this object"""
        self.displacement = Vector(0,0)
        """A vector of positional offset from the 0,0 of world origin"""
        self.velocity = Vector(0,0)
        """A vector of velocity magnitude and angle"""
        self.acceleration = Vector(0,0)
        """A vector of acceleration magnitude and angle"""
        self.material = material
        """The material the PhysicsObject is made of"""
        self.mass = mass
        """mass in kg"""
        self.volume = mass / self.material.density
        self.side = self.volume**(1/3)
        """ Length of a side in m"""
        self.width = self.side
        """ width in m"""
        self.height = self.side
        """ height in m """
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
                    if next_displacement.y + self.side >= other_next_displacement.y - p.side:
                        y_cross = True
                elif self.displacement.y >= p.displacement.y:
                    if next_displacement.y - self.side <= other_next_displacement.y + p.side:
                        y_cross = True
                x_cross = False
                if self.displacement.x <= p.displacement.x:
                    if next_displacement.x + self.side >= other_next_displacement.x - p.side:
                        x_cross = True
                elif self.displacement.x >= p.displacement.x:
                    if next_displacement.x - self.side <= other_next_displacement.x + p.side:
                        x_cross = True

                if x_cross and y_cross:
                    self.collide(p, next_displacement, other_next_displacement, interval)
                    return True
        return False

    def clear_forces(self):
        """
        Clears forces from self.dependent_force_generators by calling remove() on each

        """
        for f in self.dependent_force_generators:
            f.remove()




