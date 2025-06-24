import os

import click
import pandas as pd

from app.util import parser


def get_excel_df(file_path):
    """Process data from an Excel sheet."""
    # Read the Excel file into a DataFrame
    data = pd.read_excel(file_path)
    return data


def parse_entry_formula(folder_path):
    entries = []
    formulas = []
    structures = []

    # Loop through the directory and its subdirectories
    for root, _, files in os.walk(folder_path):
        for file in files:
            # Check if the file is a CIF file
            if file.endswith(".cif"):
                # Get the full path of the CIF file
                file_path = os.path.join(root, file)
                # Get the formula from the CIF file
                formula = parser.get_formula_from_cif(file_path)
                entry = parser.get_cif_entry_id(file_path)
                structure = parser.get_cif_structure(file_path)
                entries.append(entry)
                formulas.append(formula)
                structures.append(structure)

    data = pd.DataFrame(
        {"Entry": entries, "Formula": formulas, "Structure": structures}
    )
    return data


def compile_element_counts(df, output_dir_path, excel_file_path):
    """Compile the total number of elements in the DataFrame."""
    element_counts = {}
    for i in range(1, (len(df.columns) // 2) + 1):
        element_col = f"Element {i}"
        count_col = f"# Element {i}"
        if element_col not in df.columns or count_col not in df.columns:
            continue
        for _, row in df.iterrows():
            element = row[element_col]
            count = row[count_col]
            if pd.notnull(element) and pd.notnull(count):
                element_counts[element] = element_counts.get(element, 0) + 1

    df = pd.DataFrame(
        list(element_counts.items()), columns=["Element", "# Element"]
    )
    base_name = os.path.splitext(os.path.basename(excel_file_path))[0]
    file_name = f"{base_name}_element_count.xlsx"
    file_path = os.path.join(output_dir_path, file_name)

    df = df.sort_values(by="# Element", ascending=False)
    df.to_excel(file_path, index=False)
    click.secho(f"Element counts saved to: {file_path}", fg="cyan")
    click.secho("Element counting is completed", fg="cyan")

    # Print the results to the terminal
    df.index = df.index + 1
    print(df.head(10).to_string(index=False))

    return df
