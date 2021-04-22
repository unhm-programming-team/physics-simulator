"""
Contains a list, Options, for easy changing of in-game options.

At some point, this might be broken into several lists.


"""

Options = {
    'title': 'Physics Simulator',
    'gravity': False, # starting val
    'air resistance': False,
    'air density': 1.225,  # 1.225 is earth
    'zoom': 1, # not yet implemented
    'canvas height': 800, # pixels
    'canvas width': 800,
    'update interval': 0.02,  # seconds
    'default mass': 10000000,  # kilograms
    'key force magnitude': 100000,  # newtons
    'key force duration': 1,
    'canvas border type': 'ridge',  # keywords only
    'canvas border width': 4,
    'canvas background color': '#E3F3FF',
    'canvas axis color': 'green',
    'canvas left physics adjustment': 5,  # in pixels
    'canvas right physics adjustment': 3,
    'canvas top physics adjustment': 5,
    'canvas bottom physics adjustment': 3,
    'object popup update interval': 1,  # in seconds
    'canvas select radius': 5,
    'windows transparent color': '#F3F4FF',
    'velocity zero limit': 5,
    'net force zero limit': 5
}
"""
"""