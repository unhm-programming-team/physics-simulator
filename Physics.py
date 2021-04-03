import math

import Substance


class Vector:
    def __init__(self, angle, magnitude):
        """
        Represents direction and magnitude. Vectors can be broken into x and y components and
        reassembled from those components.
        :param angle: The angle, in radians
        :type angle: number
        :param magnitude: The magnitude of the Vector
        :type magnitude: number
        """
        self.angle = angle
        self.magnitude = magnitude
        self.y = 0
        self.x = 0
        self.calculate_components()

    def calculate_components(self):
        """
        Calculate components from angle and magnitude.
        """
        self.y = self.magnitude * math.sin(self.angle)
        self.x = self.magnitude * math.cos(self.angle)

    def calculate_angles(self):
        """
        Calculate angle from components.
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
        :returns: undefined
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


class VectorObject:
    """
    An object which stores its x,y position as a displacement vector.
    It has a width and height, and 'bounds' based on those values.
    In addition to displacement, it has vectors for velocity and acceleration.

    When it updates, it converts acceleration to velocity and velocity into displacement.

    It recalculates bounds as it needs to as the displacement vector changes for drawing.

    """
    def __init__(self, physics_canvas):
        """
        :param physics_canvas: Vector Object can tell Physics_Canvas when it needs to move.
        :type physics_canvas: class PhysicsCanvas
        """
        self.physics_canvas = physics_canvas
        self.canvas_id = 0
        self.width = 0
        self.height = 0
        self.x_0 = 0
        self.x_1 = 0
        self.y_0 = 0
        self.y_1 = 0
        self.displacement = Vector(0,0)
        self.velocity = Vector(0,0)
        self.acceleration = Vector(0,0)
        self.calculate_bounds()

    def calculate_bounds(self):
        """
        Sets the x1 and y1 to coordinates of a square around it.
        """
        self.x_0 = self.displacement.x - 1/2 * self.width
        self.x_1 = self.displacement.x + 1/2 * self.width
        self.y_0 = self.displacement.y - 1/2 * self.height
        self.y_1 = self.displacement.y + 1/2 * self.height

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
        self.physics_canvas.move_me(self)


class MassObject(VectorObject):
    """
    Extends VectorObject, so it has displacement, velocity, and acceleration.

    Also has a mass and a material.
    It calculates its volume(m^3) and side length(m) from its material density(kg/m^3) and mass(kg).
    """
    def __init__(self, physics_canvas, material=Substance.Material(), mass=10):
        """
        :type physics_canvas: class PhysicsCanvas
        :type material: class Substance.Material
        :type mass: number
        """
        VectorObject.__init__(self, physics_canvas)
        self.material = material
        self.mass = mass
        self.volume = mass / self.material.density
        self.side = self.volume**(1/3)
        self.width = self.side
        self.height = self.side
        self.calculate_bounds()


class Force(Vector):
    """
    A force which operates over time, executing a single force on the object once per sec.

    If constant is true, the force (such as gravity), acts continually on the object.


    """
    def __init__(self, angle, magnitude, duration=1.0, constant=False):
        Vector.__init__(self, angle, magnitude)
        self.force_magnitude = magnitude
        self.remaining = duration
        self.constant = constant

    @staticmethod
    def make_directional_force(direction, magnitude, duration=1.0, constant=False):
        vec = Vector.make_directional_vector(direction, magnitude)
        return Force(vec.angle, vec.magnitude, duration, constant)

    def update(self, interval):
        """
        Changes Vector.magnitude accordingly

        """
        if interval < self.remaining:
            interval = self.remaining - interval
        if self.remaining > 0:
            self.magnitude = self.force_magnitude * interval
            self.calculate_components()
            self.remaining -= interval
        if self.constant:
            self.remaining = 1


class ForceObject(MassObject):
    """
    Mass Object gives it mass and volume
    Force adds forces to the object
    """
    def __init__(self, physics_canvas, material=Substance.Material(), mass=1000):
        """
        :type physics_canvas:PhysicsCanvas
        :type material: Substance.Material
        :type mass: number
        """
        MassObject.__init__(self, physics_canvas, material, mass)
        self.forces = []
        self.net_force_vector = Vector(0,0)

    def update(self, interval):
        """
        Gets a new vector equal to multiplying acceleration by Velocity and adds it
        to the velocity, mutating the velocity vector. v = at + v_0
        Does the same for displacement. s = vt + s_0
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
        self.velocity.add(self.acceleration.scale_make(interval))
        self.displacement.add(self.velocity.scale_make(interval))
        self.calculate_bounds()
        self.physics_canvas.move_force_object(self)

