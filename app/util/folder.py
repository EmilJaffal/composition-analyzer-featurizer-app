import glob
import os
from os.path import join

import pandas as pd


def list_xlsx_files_with_formula(script_dir_path):
    """List Excel files in the given dir 'Formula' with column."""
    excel_files_with_paths = []

    # Scan the directory for .xlsx files
    excel_files = [
        file for file in os.listdir(script_dir_path) if file.endswith(".xlsx")
    ]

    if not excel_files:
        return None

    for file in excel_files:
        file_path = os.path.join(script_dir_path, file)
        try:
            # Attempt to read the first column of the Excel file
            df = pd.read_excel(file_path, nrows=0)  # Read only headers
            if any(col.lower() == "formula" for col in df.columns):
                excel_files_with_paths.append(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    # Sorting the files by their base filename alphabetically
    excel_files_with_paths.sort(key=lambda x: os.path.basename(x).lower())

    print("\nAvailable Excel files with 'Formula' column:")
    for idx, file_path in enumerate(excel_files_with_paths, start=1):
        print(f"{idx}. {os.path.basename(file_path)}")  # Display only the file name

    while True:
        try:
            choice = int(
                input(
                    "\nEnter the number corresponding to the Excel file you wish to select: "
                )
            )
            if 1 <= choice <= len(excel_files_with_paths):
                return excel_files_with_paths[choice - 1]  # Return the full file path
            else:
                print(
                    f"Please enter a number between 1 and {len(excel_files_with_paths)}."
                )
        except ValueError:
            print("Invalid input. Please enter a number.")


def choose_dir(script_directory, ext=".cif"):
    """Allows the user to select a directory from the given path."""

    directories = [
        d
        for d in os.listdir(script_directory)
        if os.path.isdir(join(script_directory, d))
        and any(file.endswith(ext) for file in os.listdir(join(script_directory, d)))
    ]

    if not directories:
        print("No directories found in the current path containing .cif files!")
        return None
    print(f"\nAvailable folders containing {ext} files:")
    for idx, dir_name in enumerate(directories, start=1):
        if ext == ".cif":
            num_of_cif_files = get_cif_file_count_from_directory(dir_name)
            print(f"{idx}. {dir_name}, {num_of_cif_files} files")
        else:
            print(f"{idx}. {dir_name}")
    while True:
        try:
            choice = int(
                input(
                    "\nEnter the number corresponding to the folder containing .cif files: "
                )
            )
            if 1 <= choice <= len(directories):
                return join(script_directory, directories[choice - 1])
            else:
                print(f"Please enter a number between 1 and {len(directories)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def save_to_csv_directory(folder_info, df, base_filename):
    """Saves the dataframe as a CSV inside a 'csv' sub-directory of the
    provided folder."""

    csv_directory = join(folder_info, "csv")
    if not os.path.exists(csv_directory):
        os.mkdir(csv_directory)

    # Extract the name of the chosen folder
    folder_name = os.path.basename(folder_info)

    # Set the name for the CSV file based on the chosen folder
    csv_filename = f"{folder_name}_{base_filename}.csv"

    # Save the DataFrame to the desired location
    df.to_csv(join(csv_directory, csv_filename), index=False)

    print(csv_filename, "saved")


def get_cif_file_count_from_directory(directory):
    """Helper function to count .cif files in a given directory."""
    return len(glob.glob(join(directory, "*.cif")))
