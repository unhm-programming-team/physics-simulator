def validate_number_input(inp):
    """
    Validates that a string input can be converted to a number.

    Also confirms it is POSITIVE

    :param inp: The number to test
    :return: true or false
    :rtype: bool
    """
    true_false = True
    try:
        x = float(inp)
        if x < 0.000001:
            true_false = False
    except ValueError:
        true_false = False
    return true_false


def get_line(x1, y1, x2, y2):
    """
    Finds slope and intercept of a line given two points
    :param x1: the old x, old displacement
    :param y1: the old y, old displacement
    :param x2: the target x, new displacement
    :param y2: the target y, new displacement
    :return: A tuple (slope, intercept, vertical, endpoint), where vertical is False if not vertical and endpoint is x2, y2
    :rtype: Tuple
    """
    slope = 0
    intercept = 0
    rise = y2 - y1
    run = x2 - x1
    vertical = False
    end_point = (x2, y2)
    if x2 == x1:
        vertical = True
    else:
        slope = rise/run
        intercept = y1 - slope*x1
    return slope, intercept, vertical, end_point


def find_intersecting_point(line1, line2):
    """
    Finds the intersecting points between two line
    :param line1: A tuple of the form (slope, intercept, vertical, (endpoint_x, endpoint_y))
    :type line1: Tuple
    :param line2:  A tuple of the form (slope, intercept, vertical, (endpoint_x, endpoint_y))
    :type line2: Tuple
    :return: A tuple of (x,y) corresponding to the intersecting point OR False, if they are parallel
    :rtype: Tuple
    """
    print(f"line1: {line1}")
    print(f"line2: {line2}")
    slope1, intercept1, vertical1, end_point1 = line1
    slope2, intercept2, vertical2, end_point2 = line2
    x1, y1 = end_point1
    x2, y2 = end_point2
    intersect_x = 0
    intersect_y = 0
    if vertical1 and vertical2:
        if x1 != x2:
            intersect_x = (x1+x2)/2
            intersect_y = (y2+y1)/2
        else:
            intersect_x = x1
            intersect_y = (y2+y1)/2
    else:
        if round(slope1, 3) == round(slope2, 3):
            intersect_x = (x1+x2)/2
            intersect_y = (y2+y1)/2
        else:
            intersect_x = (intercept2-intercept1)/(slope1-slope2)
            intersect_y = slope1*intersect_x + intercept1
            intersect_y2 = slope2*intersect_x + intercept2
    return intersect_x, intersect_y


def center(win):
    """
    Centers the window by setting the geometry
    :param win: root window
    :type win: Tkinter.Tk
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

