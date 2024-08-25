def r44(value):
    return f"{round(value, 3):.3f}"

def human_format_number(number):
    if number > -100 and number < 100:
        return r44(number)
    # Determine the sign of the number
    sign = '-' if number < 0 else ''
    # Work with the absolute value of the number
    abs_number = abs(number)
    
    if abs_number < 100:
        return f"{sign}{abs_number}"
    elif 100 <= abs_number < 100000:
        return f"{sign}{abs_number / 1000:.1f}K"
    elif 100000 <= abs_number < 100000000:
        return f"{sign}{abs_number / 1000000:.1f}M"
    elif 100000000 <= abs_number < 1000000000000:
        return f"{sign}{abs_number / 1000000000:.1f}B"
    elif 1000000000000 <= abs_number < 1000000000000000:
        return f"{sign}{abs_number / 1000000000000:.1f}T"
    else:
        return number

def human_format_number2(number):
    if number > -100 and number < 100:
        return r44(number)
    # Determine the sign of the number
    sign = '-' if number < 0 else ''
    # Work with the absolute value of the number
    abs_number = abs(number)
    
    if abs_number < 100:
        return f"{sign}{abs_number}"
    elif 100 <= abs_number < 100000:
        return f"{sign}{abs_number / 1000:.2f}K"
    elif 100000 <= abs_number < 100000000:
        return f"{sign}{abs_number / 1000000:.2f}M"
    elif 100000000 <= abs_number < 1000000000000:
        return f"{sign}{abs_number / 1000000000:.2f}B"
    elif 1000000000000 <= abs_number < 1000000000000000:
        return f"{sign}{abs_number / 1000000000000:.2f}T"
    else:
        return number
