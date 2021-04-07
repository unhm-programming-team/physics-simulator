"""
This module will have info relating to game options

Should work it into the UI so that some or all of these options can be toggled.

Maybe options could be saved/loaded
"""


Options = {
    'title': 'Physics Simulator',
    'gravity': False, # not yet implemented
    'zoom': 1, # not yet implemented
    'canvas height': 500, # pixels
    'canvas width': 500,
    'update interval': 0.05,  # seconds
    'default mass': 10000000,  # kilograms
    'key force magnitude': 1000000,  # newtons
    'key force duration': 1,
    'canvas border type': 'ridge',  # keywords only
    'canvas border width': 4,
    'canvas background color': '#E3F3FF',
    'canvas left physics adjustment': 5,  # in pixels
    'canvas right physics adjustment': 3,
    'canvas top physics adjustment': 5,
    'canvas bottom physics adjustment': 3,
    'object popup update interval': 1,  # in seconds
    'canvas select radius': 5,
    'windows transparent color': '#F3F4FF'
}
