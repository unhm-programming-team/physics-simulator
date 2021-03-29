"""
This will have classes related to material properties

Densities should be given in kilograms / cubic meter
"""


class Material:
    def __init__(self, density=1, color='#bf40b3'):
        self.density = density
        self.color = color  # pink debug color for blank materials


MATERIALS = {
    "silver": Material(10490, "#bbbbbb"),
    "chalk": Material(2499, '#B7AFA4'),
    "maple": Material(700,'#7D3721'),
    "cork": Material(240, '#C8985E')
}
