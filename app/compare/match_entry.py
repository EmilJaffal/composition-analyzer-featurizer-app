import os
import shutil

import pandas as pd

from app.util import excel, prompt


def get_new_excel_with_matching_entries(cif_dir_path, script_dir_path):
    prompt.print_match_option()

    excel_path = excel.select_directory_and_file(script_dir_path)
    cif_ids_in_excel, chosen_sheet_name = excel.load_data_from_excel(
        excel_path
    )
    cif_ids_in_files, _ = excel.gather_cif_ids_from_files(cif_dir_path)

    # Filter and save new Excel file
    filter_excel(excel_path, cif_ids_in_files, chosen_sheet_name)

    # Move CIF files to subfolders based on match status
    filter_cif_files(cif_dir_path, cif_ids_in_files, cif_ids_in_excel)

    # Generate and save report
    generate_and_save_report(
        cif_dir_path,
        cif_ids_in_excel,
        cif_ids_in_files,
        script_dir_path,
    )


def filter_cif_files(cif_dir_path, cif_ids_in_files, cif_id_set_from_excel):
    matched_dir = os.path.join(cif_dir_path, "matched")
    unmatched_dir = os.path.join(cif_dir_path, "unmatched")
    os.makedirs(matched_dir, exist_ok=True)
    os.makedirs(unmatched_dir, exist_ok=True)

    for cif_id in cif_ids_in_files:
        source_path = os.path.join(cif_dir_path, str(cif_id) + ".cif")
        try:
            if cif_id in cif_id_set_from_excel:
                shutil.move(source_path, matched_dir)
            else:
                shutil.move(source_path, unmatched_dir)
        except FileNotFoundError:
            print(f"File not found: {source_path}")
        except Exception as e:
            print(f"Error moving {source_path}: {e}")

    print(f"Matched CIF files moved to: {matched_dir}")
    print(f"Unmatched CIF files moved to: {unmatched_dir}")


def generate_and_save_report(
    folder_info,
    cid_id_set_from_excel,
    cif_ids_in_files,
    script_directory,
):
    """Generates and saves a report of missing CIF IDs compared."""
    folder_name = os.path.basename(folder_info)
    cif_id_not_found_list = cid_id_set_from_excel - cif_ids_in_files

    if cif_id_not_found_list:
        print("Missing CIF IDs:")
        for cif_id in cif_id_not_found_list:
            print(cif_id)
    else:
        print("All CIF files in the Excel sheet exists in the folder")

    print("\nSummary:")
    print(
        f"- {len(cif_id_not_found_list)} entries from the Excel sheet are missing.\n"
    )

    df_missing = pd.DataFrame(
        list(cif_id_not_found_list), columns=["Missing CIF IDs"]
    )

    csv_filename = f"{folder_name}_missing_files.csv"
    csv_path = os.path.join(script_directory, csv_filename)

    df_missing.to_csv(csv_path, index=False)
    print(f"\nMissing CIF IDs saved to {csv_filename}.")


def filter_excel(excel_path, cif_ids_in_files, chosen_sheet_name):
    """Filters the original Excel sheet to only include the rows the
    cif_ids_in_files and saves the modified DF to a new Excel file."""
    df_original = pd.read_excel(excel_path, sheet_name=chosen_sheet_name)

    # Filter the dataframe
    df_filtered = df_original[df_original["Entry"].isin(cif_ids_in_files)]

    # Create the new filename
    base_name, ext = os.path.splitext(os.path.basename(excel_path))
    new_filename = base_name + "_filtered" + ext
    new_excel_path = os.path.join(os.path.dirname(excel_path), new_filename)

    # Save to the new Excel file
    df_filtered.to_excel(new_excel_path, index=False)
    print(f"\nFiltered Excel sheet saved to {new_filename}.")

    return new_excel_path
