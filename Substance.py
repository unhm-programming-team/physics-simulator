"""
Classes related to material properties
"""


class Material:
    """
    A material is a broad reference to a material type

    :param density: The density, in kg / m^3
    :type density: number
    :param color: The color the material should render as
    :type color: color string
    :param name: The name of the material
    :type name: str
    """
    def __init__(self, density=1, color='#bf40b3', name='unnamed'):
        self.density = density
        self.color = color  # pink debug color for blank materials
        self.name = name


MATERIALS = {
    "silver": Material(10490, "#bbbbbb", 'silver'),
    "chalk": Material(2499, '#B7AFA4', 'chalk'),
    "maple": Material(700,'#7D3721', 'maple'),
    "cork": Material(240, '#C8985E', 'cork')
}
"""
Add new materials to this list to have them appear as options in application selection menus.
"""
