"""
This will have classes related to material properties

Densities should be given in kilograms / cubic meter
"""


class Material:
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
