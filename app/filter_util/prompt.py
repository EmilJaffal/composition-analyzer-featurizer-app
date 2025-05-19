import os

import click
import pandas as pd

from app.filter_util.parser import parse_formula1
from app.filter_util.processor import parse_entry_formula


def sort_formulas_in_excel_or_folder(script_dir, available_files):
    available_folders = [
        folder
        for folder in available_files
        if os.path.isdir(os.path.join(script_dir, folder))
        and any(
            file.endswith(".cif")
            for file in os.listdir(os.path.join(script_dir, folder))
        )
    ]

    excel_sheets = [f for f in available_files if f.endswith(".xlsx")]
    cif_folders = [
        f for f in available_folders if os.path.isdir(os.path.join(script_dir, f))
    ]

    if not excel_sheets and not cif_folders:
        click.secho(
            "No Excel sheets or CIF folders available in the script's directory.",
            fg="cyan",
        )
        return

    choice = click.prompt(
        "Do you want to filter an Excel sheet/CIFs [1] or"
        " do you have a filtered sheet ready [2]? Enter the number"
        " corresponding to your choice",
        type=int,
    )

    if choice == 1:
        click.secho("Available folders containing .cif files:", fg="cyan")
        for idx, folder in enumerate(cif_folders, start=1):
            click.echo(f"{idx}. {folder}")
        excel_sheets.sort()  # Sort the list alphabetically
        click.secho("Available .xlsx files:", fg="cyan")
        for idx, sheet in enumerate(excel_sheets, start=len(cif_folders) + 1):
            click.echo(f"{idx}. {sheet}")

        choice = click.prompt("Enter the number corresponding to your choice", type=int)

        if 1 <= choice <= len(cif_folders):
            cif_dir_path = os.path.join(script_dir, cif_folders[choice - 1])
            df = parse_entry_formula(cif_dir_path)
            df.index = df.index + 1
            click.secho("Data processed from CIF folder:", fg="cyan")
            print(df.head(5))
            print(df.tail(5))

            # Save raw data to Excel sheet if it is a CIF folder
            file_name = os.path.basename(cif_dir_path)
            output_folder = os.path.join(script_dir)
            os.makedirs(output_folder, exist_ok=True)

            # Parse formulas and append elements and counts to DataFrame
            click.secho(
                "Currently processing elements of your sheet",
                fg="cyan",
            )

            df_copy = df.copy()

            # Apply the function to each row in the DataFrame
            df_copy[["Elements", "Counts"]] = (
                df_copy["Formula"].apply(parse_formula1).apply(pd.Series)
            )

            # Split the lists into separate columns
            for i in range(max(map(len, df_copy["Elements"]))):
                df_copy[f"Element {i+1}"] = df_copy["Elements"].str[i]
                df_copy[f"# Element {i+1}"] = df_copy["Counts"].apply(
                    lambda x: x[i] if len(x) > i else None
                )

            # Drop temporary columns
            df_copy.drop(["Elements", "Counts"], axis=1, inplace=True)

            click.secho(
                "Elements and counts appended to DataFrame:",
                fg="cyan",
            )
            print(df_copy.head(5))
            print(df_copy.tail(5))

            # Save DataFrame to Output folder
            output_file_name = f"{file_name}_elements_sorted.xlsx"
            output_file_path = os.path.join(output_folder, output_file_name)
            df_copy.to_excel(output_file_path, index=False)
            click.secho(
                f"Appended DataFrame saved to: {output_file_path}",
                fg="cyan",
            )

        elif len(cif_folders) < choice <= len(cif_folders) + len(excel_sheets):
            sheet_idx = choice - len(cif_folders) - 1
            file_name = excel_sheets[sheet_idx]
            file_path = os.path.join(script_dir, file_name)
            df = pd.read_excel(file_path)
            click.secho("Data processed from Excel sheet:", fg="cyan")
            click.echo(df)

            # Parse formulas and append elements and counts to DataFrame
            click.secho(
                "Currently processing elements of your sheet",
                fg="cyan",
            )

            df_copy = df.copy()

            # Apply the function to each row in the DataFrame
            df_copy[["Elements", "Counts"]] = (
                df_copy["Formula"].apply(parse_formula1).apply(pd.Series)
            )

            # Split the lists into separate columns
            for i in range(max(map(len, df_copy["Elements"]))):
                df_copy[f"Element {i+1}"] = df_copy["Elements"].str[i]
                df_copy[f"# Element {i+1}"] = df_copy["Counts"].apply(
                    lambda x: x[i] if len(x) > i else None
                )

            # Drop temporary columns
            df_copy.drop(["Elements", "Counts"], axis=1, inplace=True)
            df_copy.index = df_copy.index + 1
            click.secho(
                "Elements and counts appended to DataFrame:",
                fg="cyan",
            )
            click.echo(df_copy)

            # Save DataFrame to the same directory as the input Excel sheet
            output_folder = os.path.dirname(file_path)
            os.makedirs(output_folder, exist_ok=True)

            output_file_name = f"{os.path.splitext(file_name)[0]}_elements_sorted.xlsx"
            output_file_path = os.path.join(output_folder, output_file_name)
            df_copy.to_excel(output_file_path, index=False)
            click.secho(
                f"Appended DataFrame saved to: {output_file_path}",
                fg="cyan",
            )

        else:
            click.secho("Invalid choice.", fg="red")

    elif choice == 2:
        # Here you can implement the logic for handling a filtered sheet
        pass
    else:
        click.secho("Invalid choice.", fg="red")


def dataframe_to_dict(results, elements):
    """Convert DataFrame to dictionary with Element as keys and # Element as
    values.

    Args:
    results (DataFrame): DataFrame with 'Element' and '# Element' columns.
    elements (list): List of all elements to include in the dictionary.

    Returns:
    dict: Dictionary with Element as keys and # Element as values.
    """
    # Initialize an empty dictionary with all elements and counts set to 0
    d = {element: 0 for element in elements}

    # Iterate through DataFrame rows and update the counts
    for index, row in results.iterrows():
        d[row["Element"]] = row["# Element"]

    return d
