def check_for_digits(val):
    for c in str(val):
        if c.isdigit():
            return True
    return False
