import os
import textwrap

import pandas as pd

from app.util import excel


def combine_features_with_database_excel(script_dir_path):
    print_combine_entry_intro_prompt()
    print("Choose a file with featurized content.")
    featurized_file_path = excel.select_directory_and_file(script_dir_path)
    cif_set_feat, featurized_sheet_name = excel.load_data_from_excel(
        featurized_file_path
    )

    print("\nNext, choose another file.")
    database_file_path = excel.select_directory_and_file(script_dir_path)
    cif_set_db, database_sheet_name = excel.load_data_from_excel(
        database_file_path
    )

    common_cif_IDs = cif_set_feat.intersection(cif_set_db)
    if not common_cif_IDs:
        print("No common_cif_IDs CIF IDs found.")
        return

    merge_excel_data(
        featurized_file_path,
        featurized_sheet_name,
        database_file_path,
        database_sheet_name,
        common_cif_IDs,
    )


def merge_excel_data(
    featurized_file_path,
    featurized_sheet_name,
    database_file_path,
    database_sheet_name,
    common_cif_ids,
):
    ext1 = os.path.splitext(featurized_file_path)[1].lower()
    ext2 = os.path.splitext(database_file_path)[1].lower()

    # Read inputs
    if ext1 == ".csv":
        df1 = pd.read_csv(featurized_file_path)
    else:
        df1 = pd.read_excel(
            featurized_file_path, sheet_name=featurized_sheet_name
        )
    if ext2 == ".csv":
        df2 = pd.read_csv(database_file_path)
    else:
        df2 = pd.read_excel(database_file_path, sheet_name=database_sheet_name)

    # Strip whitespace from column names
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # Normalize special column names for merging
    normalize = {
        "entry": "Entry",
        "formula": "Formula",
        "structure": "Structure",
    }
    df1 = df1.rename(
        columns={
            c: normalize[c.strip().lower()]
            for c in df1.columns
            if c.strip().lower() in normalize
        }
    )
    df2 = df2.rename(
        columns={
            c: normalize[c.strip().lower()]
            for c in df2.columns
            if c.strip().lower() in normalize
        }
    )

    # Ensure merge key exists in both
    if "Entry" not in df1.columns or "Entry" not in df2.columns:
        raise KeyError(
            "Missing 'Entry' column in one of the datasets after "
            "normalization."
        )

    # Filter to common_cif_ids
    df1 = df1[df1["Entry"].isin(common_cif_ids)]
    df2 = df2[df2["Entry"].isin(common_cif_ids)]

    # Drop duplicated special columns from df2 (only Formula, Structure)
    df1_cols_lower = {c.lower() for c in df1.columns}
    drop_special = [
        c
        for c in df2.columns
        if c.lower() in ("formula", "structure")
        and c.lower() in df1_cols_lower
    ]
    if drop_special:
        df2 = df2.drop(columns=drop_special)

    # Merge on Entry
    merged = pd.merge(df1, df2, on="Entry", how="inner")

    # Reorder: Entry, Formula, Structure at front if present
    front = ["Entry"]
    for col in ["Formula", "Structure"]:
        if col in merged.columns:
            front.append(col)
    rest = [c for c in merged.columns if c not in front]
    merged = merged[front + rest]

    # Display and save
    merged.index = merged.index + 1
    print(merged.head(20))

    featurized_basename = os.path.splitext(
        os.path.basename(featurized_file_path)
    )[0]
    database_basename = os.path.splitext(os.path.basename(database_file_path))[
        0
    ]
    merged_ext = ".csv" if ext1 == ".csv" and ext2 == ".csv" else ".xlsx"
    out_name = f"{featurized_basename}_{database_basename}_merged{merged_ext}"

    if merged_ext == ".csv":
        merged.to_csv(out_name, index=False)
    else:
        merged.to_excel(out_name, index=False)
    print(f"Merged data saved to {out_name}")


def print_combine_entry_intro_prompt():
    introductory_paragraph = textwrap.dedent(
        """\
        ===
        Welcome to the CIF-File Matching Tool!

        You will be required to provide a file (Excel or CSV) that contains
        CIF IDs.

        Upon completion, the script will match the column called \"Entry\" and
        merge
        the chosen featurizer file with another file.

        Ensure both files contain a CIF entry number, e.g., 314123, associated
        with a column.

        Let's get started!
        ===
        """
    )
    print(introductory_paragraph)
