def validate_number_input(inp):
    """
    Validates that a string input can be converted to a number

    Probably can remove this once we get rid of parts of the DebugTab

    :param inp: The number to test
    :return: true or false
    :rtype: bool
    """
    true_false = True
    try:
        float(inp)
    except ValueError:
        true_false = False
    return true_false
