from app.filter_util.data import get_element_list

elements = get_element_list()

invalid_symbols = [
    char
    for char in set("".join(elements))
    if char.isalpha() and char.upper() not in elements and char != "."
]


def parse_formula2(formula):
    elements_list = []
    counts_list = []
    error = None  # Initialize variable to store the error message
    current_element = ""
    current_count = ""
    for i, char in enumerate(formula, start=1):
        if char.isdigit():  # if character is a number
            current_count += char
        elif char.isupper():  # if character is uppercase letter
            if current_element:
                if (
                    current_element.capitalize() in elements
                ):  # Check both capital and lowercase versions
                    elements_list.append(current_element.capitalize())
                    counts_list.append(int(current_count) if current_count else 1)
                    current_count = ""
                    current_element = char
                else:
                    error = f"'{current_element}' is not a valid element"
                    break
            else:
                current_element = char
        elif char.islower():  # if character is lowercase letter
            current_element += char
        elif char in invalid_symbols:  # if character is an invalid symbol
            error = f"'{char}' is not a valid symbol"
            break
        elif char == ".":  # Skip the '.' character
            continue
        else:  # if character is not recognized
            error = f"'{char}' is not recognized"
            break
    if (
        current_element.capitalize() in elements
    ):  # Check both capital and lowercase versions
        elements_list.append(current_element.capitalize())
        counts_list.append(int(current_count) if current_count else 1)
    else:
        error = f"'{current_element}' is not a valid element"
    return elements_list, counts_list, error


def parse_formula1(formula):
    elements_list = []
    counts_list = []
    current_element = ""
    current_count = ""
    for char in formula:
        if char.isdigit() or char == ".":  # if character is a digit or a period
            current_count += char
        elif char.isupper():  # if character is uppercase letter
            if current_element:
                elements_list.append(current_element)
                counts_list.append(
                    float(current_count)
                    if current_count and current_count != "."
                    else 1
                )
                current_count = ""
            current_element = char
        elif char.islower():  # if character is lowercase letter
            current_element += char
    # Add the last element and count
    if current_element:
        elements_list.append(current_element)
        counts_list.append(
            float(current_count) if current_count and current_count != "." else 1
        )
    return elements_list, counts_list
