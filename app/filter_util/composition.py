import os

import click
import pandas as pd


def numerical_and_elemental_filtering(filtered_file_path, invalid_formulas_copy):
    filter_choice = click.prompt(
        "Would you like to filter based on either numerical or elemental composition? [Y/n]",
        type=str,
    )

    if filter_choice.lower() == "y":
        filtering_type = click.prompt(
            "Numerical filtering [1] will separate your sorted dataframe based on"
            " unary/binary/ternary/quaternary entries, while elemental filtering [2]"
            " will remove entries with elements you don't want. Enter the corresponding number",
            type=int,
        )

        if filtering_type == 1:
            numerical_df = pd.read_excel(filtered_file_path)

            # Group the DataFrame by the 'System' column and iterate over the groups
            for system, group in numerical_df.groupby("System"):
                # Append system name to the base filename
                base_name = os.path.splitext(os.path.basename(filtered_file_path))[0]
                file_name = f"{base_name}_{system.lower()}.xlsx"

                # Get the directory of the input file
                input_directory = os.path.dirname(filtered_file_path)

                # Construct the output file path
                output_file_path = os.path.join(input_directory, file_name)

                group.to_excel(output_file_path, index=False)

                click.echo(f"Entries for {system} saved to: {output_file_path}")

        if filtering_type == 2:
            # Extract unique elements from the DataFrame
            unique_elements = set()
            for index, row in invalid_formulas_copy.iterrows():
                unique_elements.update(row["Elements"])
            available_elements = ", ".join(sorted(unique_elements))

            while True:
                elements_to_exclude = click.prompt(
                    f"Please input elements to exclude, separated by commas. Available elements: {available_elements}. Enter 'q' to quit.",
                    type=str,
                )
                if elements_to_exclude.lower() == "q":
                    break
                elements_to_exclude = [
                    elem.strip() for elem in elements_to_exclude.split(",")
                ]
                # Check if all entered elements are valid
                if all(elem in unique_elements for elem in elements_to_exclude):
                    elemental_df = invalid_formulas_copy.copy()

                    filtered_entries = []
                    removed_entries = []

                    # Loop through the DataFrame and filter entries
                    for index, row in elemental_df.iterrows():
                        # Check if any of the specified elements are present in the row
                        if any(
                            element in elements_to_exclude
                            for element in row["Elements"]
                        ):
                            removed_entries.append(row)
                        else:
                            filtered_entries.append(row)

                    elemental_filtered = pd.DataFrame(filtered_entries)
                    elemental_removed = pd.DataFrame(removed_entries)

                    elemental_filtered.reset_index(drop=True, inplace=True)
                    elemental_removed.reset_index(drop=True, inplace=True)

                    # Get the directory and base name of the input file
                    input_directory = os.path.dirname(filtered_file_path)
                    base_name = os.path.splitext(os.path.basename(filtered_file_path))[
                        0
                    ]

                    # Construct the output file paths
                    filtered_file = os.path.join(
                        input_directory,
                        f"{base_name}_elemental_filtered.xlsx",
                    )
                    removed_file = os.path.join(
                        input_directory, f"{base_name}_elemental_removed.xlsx"
                    )

                    elemental_filtered.to_excel(filtered_file, index=False)
                    elemental_removed.to_excel(removed_file, index=False)

                    click.echo(f"Filtered entries saved to: {filtered_file}")
                    click.echo(f"Removed entries saved to: {removed_file}")
                    break
                else:
                    click.echo(
                        "Invalid entry, check the available elements list again."
                    )


def numerical_classification(invalid_formulas):
    """Classify formulas based on the number of elements."""

    click.secho("Classifying your dataframe", fg="cyan")
    invalid_formulas_copy = invalid_formulas.copy()
    invalid_formulas_copy["System"] = None
    for index, row in invalid_formulas_copy.iterrows():
        num_elements = len(row["Elements"])
        if num_elements == 1:
            invalid_formulas_copy.loc[index, "System"] = "Unary"
        elif num_elements == 2:
            invalid_formulas_copy.loc[index, "System"] = "Binary"
        elif num_elements == 3:
            invalid_formulas_copy.loc[index, "System"] = "Ternary"
        elif num_elements == 4:
            invalid_formulas_copy.loc[index, "System"] = "Quaternary"
    return invalid_formulas_copy
