import os
import warnings

import click
import pandas as pd
from CAF.features import generator

from app.util import folder

"""
Ignore warnings for Pandas
"""
warnings.simplefilter("ignore")


def run_feature_option(script_dir_path):
    # User select the Excel file
    formula_excel_path = folder.list_xlsx_files_with_formula(script_dir_path)
    if formula_excel_path:
        print(f"Selected Excel file: {formula_excel_path}")
    else:
        print("No Excel file was found. Exiting.")
        return

    # list Excel files containing with "formula" columns
    _, base_name = os.path.split(formula_excel_path)
    base_name_no_ext = os.path.splitext(base_name)[0]
    df = pd.read_excel(formula_excel_path)
    try:
        col = next(c for c in df.columns if c.lower() == "formula")
    except StopIteration:
        print("No formula column found. Exiting.")
        return

    formulas = df[col]

    # User select whether to add normalized compositional one-hot encoding
    # is_encoding_added = click.confirm(
    #     "\nDo you want to include normalized composition vector? (Default is N)",
    #     default=False,
    # )

    # if is_encoding_added:
    #     is_all_element_displayed = click.confirm(
    #         "\nDo you want to include all elements in the composition vector or"
    #         " only the ones present in the dataset? (Default is Y)",
    #         default=True,
    #     )

    add_extended_features = click.confirm(
        "\nDo you want to save additional files containing features with"
        "\nmathematical operations? Ex) +, -, *, /, exp, square, cube, etc."
        "\n(Default is N)",
        default=False,
    )

    generator.get_composition_features(
        formulas,
        extended_features=add_extended_features,
        file_prefix=base_name_no_ext,
    )
