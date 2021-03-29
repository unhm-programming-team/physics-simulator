import math

import Substance


class Vector:
    def __init__(self, angle, magnitude):
        """
        Represents direction and size
        :param angle: Radians
        :param magnitude: Pixels
        """
        self.angle = angle
        self.magnitude = magnitude
        self.y = 0
        self.x = 0
        self.calculate_components()

    def calculate_components(self):
        self.y = self.magnitude * math.sin(self.angle)
        self.x = self.magnitude * math.cos(self.angle)

    def calculate_angles(self):
        y = self.y
        x = self.x
        self.angle = math.atan2(y, x)
        self.magnitude = math.sqrt(x*x + y*y)

    @staticmethod
    def make_vector_from_components(x, y):
        angle = math.atan2(y, x)
        magnitude = math.sqrt(x*x + y*y)
        return Vector(angle, magnitude)

    def add_make(self, other_vector):
        new_x = other_vector.x + self.x
        new_y = other_vector.y + self.y
        return Vector.make_vector_from_components(new_x, new_y)

    def subtract_make(self, other_vector):
        new_x = self.x - other_vector.x
        new_y = self.y - other_vector.y
        return Vector.make_vector_from_components(new_x,new_y)

    def add(self, other_vector):
        self.x += other_vector.x
        self.y += other_vector.y
        self.calculate_angles()

    def subtract(self, other_vector):
        self.x -= other_vector.x
        self.y -= other_vector.y
        self.calculate_angles()

    def rotate(self, radians):
        new_angle = self.angle + radians
        twoPi = math.pi * 2
        if new_angle > twoPi:
            new_angle = -twoPi
        else:
            new_angle = twoPi - new_angle
        self.angle = new_angle
        self.calculate_components()

    def scale(self, scalar):
        self.magnitude *= scalar
        self.calculate_components()

    def scale_make(self, scalar):
        new_magnitude = self.magnitude * scalar
        return Vector(self.angle, new_magnitude)

    @staticmethod
    def make_directional_vector(direction='S', magnitude=1):
        """
        4 cardinals, nw, ne, se, sw
        :param direction:
        :type dirction: str
        :param magnitude:
        :return:
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
    Displacement should be meters, velocity meters/s, acceleration meters/s^2
    """
    def __init__(self, physics_canvas):
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
        self.x_0 = self.displacement.x - 1/2 * self.width
        self.x_1 = self.displacement.x + 1/2 * self.width
        self.y_0 = self.displacement.y - 1/2 * self.height
        self.y_1 = self.displacement.y + 1/2 * self.height

    def update(self, interval):
        self.velocity.add(self.acceleration.scale_make(interval))
        self.displacement.add(self.velocity.scale_make(interval))
        self.physics_canvas.move_me(self)


class MassObject(VectorObject):
    def __init__(self, physics_canvas, material=Substance.Material(), mass=10):
        VectorObject.__init__(self, physics_canvas)
        self.material = material
        self.mass = mass
        self.volume = mass / self.material.density
        self.side = self.volume**(1/3)
        self.width = self.side
        self.height = self.side
        self.calculate_bounds()



