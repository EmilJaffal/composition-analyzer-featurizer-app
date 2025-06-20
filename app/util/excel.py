import os

import pandas as pd

from app.util import parser


def select_directory_and_file(script_directory):
    excel_path = choose_excel_file(script_directory)
    if not excel_path:
        print("No file selected.")
        return None
    return excel_path


def choose_excel_file(script_directory):
    """Lets the user choose an Excel or CSV file from the specified
    directory."""
    files = [
        f
        for f in os.listdir(script_directory)
        if f.endswith(".xlsx") or f.endswith(".csv")
    ]
    files.sort()
    if not files:
        print("No Excel or CSV files found in the current path!")
        return None
    print("\nAvailable Excel/CSV files:")
    for idx, file_name in enumerate(files, start=1):
        print(f"{idx}. {file_name}")
    while True:
        try:
            choice = int(input("\nEnter the number corresponding to the file: "))
            if 1 <= choice <= len(files):
                return os.path.join(script_directory, files[choice - 1])
            print(f"Please enter a number between 1 and {len(files)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def choose_excel_sheet(excel_path):
    """Lets the user choose a sheet from the Excel file; returns None for
    CSV."""
    if excel_path.lower().endswith(".csv"):
        return None
    xls = pd.ExcelFile(excel_path)
    sheets = xls.sheet_names
    print("\nAvailable sheets:")
    for idx, sheet_name in enumerate(sheets, start=1):
        print(f"{idx}. {sheet_name}")
    while True:
        try:
            choice = int(input("\nEnter the number corresponding to the Excel sheet: "))
            if 1 <= choice <= len(sheets):
                return sheets[choice - 1]
            print(f"Please enter a number between 1 and {len(sheets)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def load_data_from_excel(excel_path):
    column_name = "Entry"
    ext = os.path.splitext(excel_path)[1].lower()
    if ext == ".csv":
        return load_csv_data_to_set(excel_path, column_name), None
    sheet = choose_excel_sheet(excel_path)
    return load_excel_data_to_set(excel_path, column_name, sheet), sheet


def load_excel_data_to_set(excel_path, column_name, sheet_name):
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    return set(df[column_name].values)


def load_csv_data_to_set(csv_path, column_name):
    df = pd.read_csv(csv_path)
    return set(df[column_name].values)


def gather_cif_ids_from_files(folder_info):
    files_lst = [
        os.path.join(folder_info, f)
        for f in os.listdir(folder_info)
        if f.endswith(".cif")
    ]
    cif_ids = set()
    for file_path in files_lst:
        cif_id = parser.get_cif_entry_id(file_path)
        try:
            cid_id = int(cif_id)
            cif_ids.add(cid_id)
        except ValueError:
            print(f"Error: Invalid CIF ID in {os.path.basename(file_path)}")
    return cif_ids, len(files_lst)
