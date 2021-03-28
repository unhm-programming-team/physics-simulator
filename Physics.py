import math


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


class PhysicsObject:
    def __init__(self, physics_canvas):
        self.physics_canvas = physics_canvas
        self.canvas_id = 0
        self.width = 0
        self.height = 0
        self.displacement = Vector(0,0)
        self.velocity = Vector(0,0)
        self.acceleration = Vector(0,0)

