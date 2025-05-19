import os
import textwrap

import pandas as pd

from app.util import excel


def combine_features_with_database_excel(script_dir_path):
    print_combine_entry_intro_prompt()
    print("Choose an Excel file with featurized content.")
    featurized_excel_path = excel.select_directory_and_file(script_dir_path)

    # Choose the featurizer Excel file
    (
        cif_id_set_from_featurized_excel,
        featurized_excel_sheet_name,
    ) = excel.load_data_from_excel(featurized_excel_path)

    print("\nNext, choose another Excel file.")
    database_excel_path = excel.select_directory_and_file(script_dir_path)

    # Choose the database Excel file
    (
        cif_id_set_from_database_excel,
        database_excel_sheet_name,
    ) = excel.load_data_from_excel(database_excel_path)

    # Check entries that are common to one another
    common_cif_ids = cif_id_set_from_featurized_excel.intersection(
        cif_id_set_from_database_excel
    )
    if not common_cif_ids:
        print("No common CIF IDs found.")
        return

    merge_excel_data(
        featurized_excel_path,
        featurized_excel_sheet_name,
        database_excel_path,
        database_excel_sheet_name,
        common_cif_ids,
    )
    # Use the common cif ids to combine the entries together


def merge_excel_data(
    featurized_excel_path,
    featurized_sheet_name,
    database_excel_path,
    database_sheet_name,
    common_cif_ids,
):
    # Load the Excel files into pandas DataFrames
    featurized_df = pd.read_excel(
        featurized_excel_path, sheet_name=featurized_sheet_name
    )
    database_df = pd.read_excel(database_excel_path, sheet_name=database_sheet_name)

    # Filter DataFrames to include only rows with common CIF IDs
    featurized_df = featurized_df[featurized_df["Entry"].isin(common_cif_ids)]
    database_df = database_df[database_df["Entry"].isin(common_cif_ids)]

    # Assuming 'Entry' is the common column and you want to merge using an inner join
    merged_df = pd.merge(featurized_df, database_df, on="Entry", how="inner")

    # Print the first 20 rows of the merged dataframe to inspect it
    merged_df.index = merged_df.index + 1
    print(merged_df.head(20))

    # Generate the merged output file name
    featurized_basename = os.path.splitext(os.path.basename(featurized_excel_path))[0]
    database_basename = os.path.splitext(os.path.basename(database_excel_path))[0]
    merged_output_filename = f"{featurized_basename}_{database_basename}_merged.xlsx"

    # Output the merged DataFrame to an Excel file
    merged_df.to_excel(merged_output_filename, index=False)
    print(f"Merged data saved to {merged_output_filename}")


def print_combine_entry_intro_prompt():
    introductory_paragraph = textwrap.dedent(
        """\
        ===
        Welcome to the CIF-Excel Matching Tool!

        You will be required to provide an Excel file that contains CIF IDs.

        Upon completion, the script will match the column called "Entry" and merge
        the chosen featurizer Excel with another Excel file.

        Ensure both Excel files contain a CIF entry number, e.g., 314123, associated
        with a column.

        Let's get started!
        ===
        """
    )
    print(introductory_paragraph)
