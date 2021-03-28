def validate_number_input(inp):
    true_false = True
    try:
        float(inp)
    except ValueError:
        true_false = False
    return true_false
