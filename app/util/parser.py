import re

import pandas as pd


def get_parsed_binary_formula_df(formulas):
    data = []
    for formula in formulas:
        parsed_formula = get_parsed_formula(formula)
        element_A = parsed_formula[0][0]
        element_B = parsed_formula[1][0]

        # Convert indices to float, default to 1.0 if empty
        element_A_index = (
            float(parsed_formula[0][1]) if parsed_formula[0][1] else 1.0
        )
        element_B_index = (
            float(parsed_formula[1][1]) if parsed_formula[1][1] else 1.0
        )

        normalized_formula = get_normalized_formula(formula)
        parsed_normalized_formula = get_parsed_formula(normalized_formula)
        element_A_normalized_index = (
            float(parsed_normalized_formula[0][1])
            if parsed_normalized_formula[0][1]
            else 1.0
        )
        element_B_normalized_index = (
            float(parsed_normalized_formula[1][1])
            if parsed_normalized_formula[1][1]
            else 1.0
        )

        # Append to data list
        data.append(
            [
                formula,
                element_A,
                element_B,
                element_A_index,
                element_B_index,
                element_A_normalized_index,
                element_B_normalized_index,
            ]
        )

    main_df = pd.DataFrame(
        data,
        columns=[
            "Formula",
            "Element A",
            "Element B",
            "Index_A",
            "Index_B",
            "Normalized_Index_A",
            "Normalized_Index_B",
        ],
    )
    return main_df


def get_parsed_ternary_formula_df(formulas):
    data = []
    for formula in formulas:
        parsed_formula = get_parsed_formula(formula)
        element_R = parsed_formula[0][0]
        element_M = parsed_formula[1][0]
        element_X = parsed_formula[2][0]

        # Convert indices to float, default to 1.0 if empty
        element_R_index = (
            float(parsed_formula[0][1]) if parsed_formula[0][1] else 1.0
        )
        element_M_index = (
            float(parsed_formula[1][1]) if parsed_formula[1][1] else 1.0
        )
        element_X_index = (
            float(parsed_formula[2][1]) if parsed_formula[2][1] else 1.0
        )

        normalized_formula = get_normalized_formula(formula)
        parsed_normalized_formula = get_parsed_formula(normalized_formula)
        element_R_normalized_index = (
            float(parsed_normalized_formula[0][1])
            if parsed_normalized_formula[0][1]
            else 1.0
        )
        element_M_normalized_index = (
            float(parsed_normalized_formula[1][1])
            if parsed_normalized_formula[1][1]
            else 1.0
        )
        element_X_normalized_index = (
            float(parsed_normalized_formula[2][1])
            if parsed_normalized_formula[2][1]
            else 1.0
        )

        # Append to data list
        data.append(
            [
                formula,
                element_R,
                element_M,
                element_X,
                element_R_index,
                element_M_index,
                element_X_index,
                element_R_normalized_index,
                element_M_normalized_index,
                element_X_normalized_index,
            ]
        )

    # Create a DataFrame
    main_df = pd.DataFrame(
        data,
        columns=[
            "Formula",
            "Element R",
            "Element M",
            "Element X",
            "Index_R",
            "Index_M",
            "Index_X",
            "Normalized_Index_R",
            "Normalized_Index_X",
            "Normalized_Index_M",
        ],
    )
    return main_df


def get_parsed_formula(formula):
    pattern = r"([A-Z][a-z]*)(\d*\.?\d*)"
    elements = re.findall(pattern, formula)
    return elements


def get_normalized_formula(formula):
    demical_places = 3
    index_sum = 0
    normalized_formula_parts = []
    parsed_formula_set = get_parsed_formula(formula)

    # Calculate the sum of all indices
    for element, element_index in parsed_formula_set:
        if element_index == "":
            index_sum += 1  # Treat missing indices as 1
        else:
            index_sum += float(element_index)

    for element, element_index in parsed_formula_set:
        if element_index == "":
            normalized_index = 1 / index_sum
        else:
            normalized_index = float(element_index) / index_sum

        normalized_formula_parts.append(
            f"{element}{normalized_index:.{demical_places}f}"
        )

    # Join all parts into one string for the normalized formula
    normalized_formula_str = "".join(normalized_formula_parts)
    return normalized_formula_str


def get_num_element(formula):
    elements = get_parsed_formula(formula)
    return len(elements)


def get_none_element_label_count(
    parsed_formula_set,
):
    none_element_label_count = 0
    for formula in parsed_formula_set:
        element_label = formula[-1]

        if element_label == "None":
            none_element_label_count += 1
    return none_element_label_count


def get_is_same_element_label(parsed_formula_set, num_elements):
    labels = [item[2] for item in parsed_formula_set if item[2]]

    if num_elements == 2:
        if labels[0] == labels[1]:
            return True

    if num_elements == 3:
        labels = [item[2] for item in parsed_formula_set if item[2]]
        if labels[0] == labels[1] and labels[0] == labels[2]:
            return True

    return False


def extract_tag_from_line(line):
    """Extracts a tag from a line based on the format provided."""
    # Remove any empty parts
    parts = [part.strip() for part in line.split("#") if part.strip()]
    if len(parts) >= 3:
        return parts[2]  # Return the CIF

    return None

def get_cif_structure(file_path):
    """Extracts the CIF structure from a file."""
    target_line_start = "_chemical_name_structure_type"

    with open(file_path, "r") as file:
        for line in file:
            if line.strip().startswith(target_line_start):
                structure = line.split(target_line_start)[-1].strip()
                return structure

    return "Structure not found"

def get_formula_from_cif(file_path):
    """Simply parse the formula from a CIF file Remove "'", empty space
    Order alphabetically."""

    target_line_start = "_chemical_formula_sum"

    with open(file_path, "r") as file:
        for line in file:
            if line.strip().startswith(target_line_start):
                # Extract the formula part, assuming it's after the key
                formula = (
                    line.split(target_line_start)[-1].strip().replace("'", "")
                )
                formula = formula.replace(" ", "")

                return formula
    return "Formula not found"


def get_cif_entry_id(cif_file_path: str) -> str:
    database_code = None

    with open(cif_file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("#_database_code") or line.startswith(
                "_database_code"
            ):
                # Split the line by whitespace to get the key and value
                parts = line.split()
                if len(parts) == 2:
                    database_code = parts[1]
                    break

    return database_code
