import os

import click
import pandas as pd
from bobleesj.utils.parsers.formula import Formula
from bobleesj.utils.sorters.elements import Elements
from bobleesj.utils.sources.oliynyk import Oliynyk
from bobleesj.utils.sources.oliynyk import Property as P

from app.util import folder, prompt

def run_sort_option(script_dir_path):
    sort_method = prompt.choose_sort_method()
    if sort_method in [1, 2, 3, 4]:
        formula_excel_path = folder.list_xlsx_files_with_formula(script_dir_path)
        if formula_excel_path:
            print(f"You've selected: {formula_excel_path}")
    dir_path, base_name = os.path.split(formula_excel_path)
    excel_filename = os.path.splitext(base_name)[0]
    df = pd.read_excel(formula_excel_path)
    # Read the Formula or formula column into a list of formulas
    formulas = _extract_formulas(df)
    if sort_method == 1:
        _run_sort_by_custom_label(formulas, df, dir_path, excel_filename)
    elif sort_method == 2:
        _run_sort_by_stoichiometry(formulas, df, dir_path, excel_filename)
    elif sort_method == 3:
        _run_sort_by_property(formulas, df, dir_path, excel_filename)


def _extract_formulas(df):
    if "Formula" in df.columns:
        return df["Formula"].tolist()
    elif "formula" in df.columns:
        return df["formula"].tolist()
    else:
        raise ValueError("No 'Formula' or 'formula' column found in the Excel file.")


def _save_and_update(df, formulas_sorted, dir_path, filename):
    df["Sorted Formula"] = formulas_sorted
    _save_sorted_to_excel(df, dir_path, filename)


def _run_sort_by_custom_label(formulas, df, dir_path, filename):
    elements = Elements(excel_path="data/sort/custom-labels.xlsx")
    formulas_sorted = [
        Formula(formula).sort_by_custom_label(elements.label_mapping)
        for formula in formulas
    ]
    filename = f"{filename}_by_custom_label"
    _save_and_update(df, formulas_sorted, dir_path, filename)


def _run_sort_by_stoichiometry(formulas, df, dir_path, filename):
    is_ascending, is_normalized = _ask_ascending_normalize()
    oliynyk = Oliynyk()
    formulas_sorted = [
        Formula(formula).sort_by_stoichiometry(
            oliynyk.get_property_data_for_formula(formula, P.MEND_NUM),
            ascending=is_ascending,
            normalize=is_normalized,
        )
        for formula in formulas
    ]
    filename = _add_suffixes(filename + "_by_stoichiometry", is_ascending, is_normalized)
    _save_and_update(df, formulas_sorted, dir_path, filename)


def _run_sort_by_property(formulas, df, dir_path, filename):
    selected_property = P.select()
    oliynyk = Oliynyk()
    is_ascending, is_normalized = _ask_ascending_normalize()
    formulas_sorted = [
        Formula(formula).sort_by_elemental_property(
            oliynyk.get_property_data_for_formula(formula, selected_property),
            ascending=is_ascending,
            normalize=is_normalized,
        )
        for formula in formulas
    ]
    filename = f"{filename}_by_property_{selected_property.name}"
    filename = _add_suffixes(filename, is_ascending, is_normalized)
    _save_and_update(df, formulas_sorted, dir_path, filename)


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
