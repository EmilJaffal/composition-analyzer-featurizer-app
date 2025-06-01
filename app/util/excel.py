import os

import pandas as pd

from app.util import parser


def select_directory_and_file(script_directory):
    excel_path = choose_excel_file(script_directory)
    if not excel_path:
        print("No Excel file selected.")
        return None

    return excel_path


def choose_excel_file(script_directory):
    """" Lets the user choose an Excel file from the specified directory."""
    files = [f for f in os.listdir(script_directory) if f.endswith(".xlsx")]
    # Sort the files alphabetically
    files.sort()

    if not files:
        print("No Excel files found in the current path!")
        return None

    print("\nAvailable Excel files (not in folders):")
    for idx, file_name in enumerate(files, start=1):
        print(f"{idx}. {file_name}")

    while True:
        try:
            prompt = "\nEnter the number corresponding to the Excel file: "
            choice = int(input(prompt))
            if 1 <= choice <= len(files):
                return os.path.join(script_directory, files[choice - 1])
            else:
                print(f"Please enter a number between 1 and {len(files)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def choose_excel_sheet(excel_path):
    """Lets the user choose a sheet from the Excel file."""

    xls = pd.ExcelFile(excel_path)
    sheets = xls.sheet_names

    # Display available sheets
    print("\nAvailable sheets in the Excel file:")
    for idx, sheet_name in enumerate(sheets, start=1):
        print(f"{idx}. {sheet_name}")

    # User choice
    while True:
        try:
            prompt = "\nEnter the number corresponding to the Excel sheet: "
            choice = int(input(prompt))
            if 1 <= choice <= len(sheets):
                return sheets[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(sheets)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def load_data_from_excel(excel_path):
    chosen_sheet_name = choose_excel_sheet(excel_path)
    column_name = "Entry"
    return (
        load_excel_data_to_set(excel_path, column_name, chosen_sheet_name),
        chosen_sheet_name,
    )


def load_excel_data_to_set(excel_path, column_name, sheet_name):
    """Load data from a specific column of an Excel file into a set."""
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    # Convert all values to lowercase and strip whitespace, then add to set
    return set(df[column_name].values)


def gather_cif_ids_from_files(folder_info):
    files_lst = [
        os.path.join(folder_info, file)
        for file in os.listdir(folder_info)
        if file.endswith(".cif")
    ]

    cif_ids = set()
    for file_path in files_lst:
        cif_id = parser.get_cif_entry_id(file_path)
        try:
            cid_id = int(cif_id)
            cif_ids.add(cid_id)
        except ValueError:
            print(f"Error: Invalid CIF ID in {os.path.basename(file_path)}")
            continue

    return cif_ids, len(files_lst)
