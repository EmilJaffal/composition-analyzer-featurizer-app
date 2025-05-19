import os

import click
from app.runners import feature, filter, match, merge, sort


# Function to run the selected option
def run_selected_option(option, script_dir_path):
    if option == 1:
        filter.run_filter_option(script_dir_path)
    elif option == 2:
        sort.run_sort_option(script_dir_path)
    elif option == 3:
        feature.run_feature_option(script_dir_path)
    elif option == 4:
        match.run_match_option(script_dir_path)
    elif option == 5:
        merge.run_merge_option(script_dir_path)
    else:
        click.echo("Invalid option. Please choose 1, 2, 3, 4, or 5.")


@click.command()
def main():
    # Display options
    click.echo("\nOptions:")
    click.echo("  1: Filter chemical formulas and generate periodic table heatmap")
    click.echo("  2: Sort chemical formulas in an Excel file")
    click.echo("  3: Create compositional features for formulas in an Excel file")
    click.echo("  4: Match .cif files in a folder against an Excel file")
    click.echo("  5: Merge two Excel files based on id/entry")

    # Prompt user for input
    option = click.prompt(
        "Please enter the number of the option you want to run",
        type=int,
    )

    # Validate input
    while option not in [1, 2, 3, 4, 5]:
        click.echo("Invalid option. Please choose 1, 2, 3, 4, or 5.")
        option = click.prompt(
            "Please enter the number of the option you want to run",
            type=int,
        )

    script_dir_path = os.path.dirname(os.path.abspath(__file__))
    run_selected_option(option, script_dir_path)


if __name__ == "__main__":
    main()
