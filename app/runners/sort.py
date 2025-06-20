import os

import click
import pandas as pd
from bobleesj.utils.sources.oliynyk import Oliynyk, Property
from CAF.sort import custom, property, stoichiometry

from app.util import folder, prompt


def run_sort_option(script_dir_path):
    sort_method = prompt.choose_sort_method()
    if sort_method in [1, 2, 3, 4]:
        formula_excel_path = folder.list_xlsx_files_with_formula(
            script_dir_path
        )
        if formula_excel_path:
            print(f"You've selected: {formula_excel_path}")
    dir_path, base_name = os.path.split(formula_excel_path)
    excel_filename = os.path.splitext(base_name)[0]
    df = pd.read_excel(formula_excel_path)

    # Read the Formula or formula column into a list of formulas
    if "Formula" in df.columns:
        formulas = df["Formula"].tolist()
    elif "formula" in df.columns:
        formulas = df["formula"].tolist()
    else:
        raise ValueError(
            "No 'Formula' or 'formula' column found in the Excel file."
        )

    if sort_method == 1:
        _run_sort_by_custom_label(formulas, df, dir_path, excel_filename)
    if sort_method == 2:
        _run_sort_by_stoichiometry(formulas, df, dir_path, excel_filename)
    if sort_method == 3:
        _run_run_sort_by_property(formulas, df, dir_path, excel_filename)


def _run_sort_by_custom_label(formulas, df, dir_path, filename):
    custom_labels = custom.get_custom_labels_from_excel(
        "data/sort/custom-labels.xlsx"
    )
    formulas_sorted = []
    for formula in formulas:
        formula_sorted = custom.sort(formula, custom_labels)
        formulas_sorted.append(formula_sorted)
    df["Sorted Formula"] = formulas_sorted
    filename = f"{filename}_by_custom_label"
    _save_sorted_to_excel(df, dir_path, filename)


def _run_sort_by_stoichiometry(formulas, df, dir_path, filename):
    is_ascending, is_normalized = _ask_ascending_normalize()
    formulas_sorted = []
    for formula in formulas:
        formula_sorted = stoichiometry.sort(
            formula, Oliynyk(), is_ascending, is_normalized
        )
        formulas_sorted.append(formula_sorted)
    df["Sorted Formula"] = formulas_sorted
    filename = _add_suffixes(
        filename, "by_stoichiometry", is_ascending, is_normalized
    )
    _save_sorted_to_excel(df, dir_path, filename)


def _run_run_sort_by_property(formulas, df, dir_path, filename):
    selected_property = Property.select()
    oliynyk = Oliynyk()
    is_ascending, is_normalized = _ask_ascending_normalize()
    formulas_sorted = []
    for formula in formulas:
        formula_sorted = property.sort(
            formula, selected_property, oliynyk, is_ascending, is_normalized
        )
        formulas_sorted.append(formula_sorted)
    df["Sorted Formula"] = formulas_sorted
    filename = f"{filename}_by_property_{selected_property.name}"
    filename = _add_suffixes(filename, is_ascending, is_normalized)
    _save_sorted_to_excel(df, dir_path, filename)


def _add_suffixes(filename, is_ascending, is_normalized, method=None):
    if method:
        filename += "_" + method
    if not is_ascending:
        filename += "_descend"
    if is_normalized:
        filename += "_norm"
    return filename


def _ask_ascending_normalize():
    is_ascending = _ascend_order()
    is_normalized = _normalize_formula()
    return is_ascending, is_normalized


def _save_sorted_to_excel(df, dir_path, filename):
    output_path = os.path.join(dir_path, f"{filename}.xlsx")
    df.to_excel(output_path, index=False)
    print(f"Sorted formulas saved to {output_path}")


def _ascend_order():
    is_ascending_order = click.confirm(
        "\nWould you like to sort the indices in ascending order? "
        "(Default is Y)",
        default=True,
    )
    return is_ascending_order


def _normalize_formula():
    is_indices_as_fractions = click.confirm(
        "\nWould you like to convert indices into fractions? (Default is N)",
        default=False,
    )
    return is_indices_as_fractions
