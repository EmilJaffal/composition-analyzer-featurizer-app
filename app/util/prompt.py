import textwrap
import click
from bobleesj.utils.sources.oliynyk import Property


def choose_sort_method():
    click.echo("\nWelcome to the chemical formula sorting tool!")
    click.echo("This tool allows you to sort chemical formulas from an Excel file.")

    sorting_methods = [
        "Custom label - Reorder by the pre-configured label for each element.",
        "Stoichiometry - Reorder by the ratio of each element in the formula.",
        "Property - Reorder by elemental chemical property value.",
        "Parse formulas into elements and indices without sorting.",
    ]

    click.echo("\nSorting methods available:")
    for index, method in enumerate(sorting_methods, start=1):
        click.echo(f"  {index}. {method}")

    sort_method = click.prompt(
        "Choose one of the sorting methods above by entering the corresponding number",
        type=int,
    )
    return sort_method


def print_match_option():
    introductory_paragraph = textwrap.dedent(
        """\
        ===
        You will be required to provide an Excel file that contains CIF IDs.

        Upon completion, two outputs will be generated:
        1. Filtered Excel file with rows matching CIF content in the folder
        2. Filered .cif folder with rows matching
        3. CSV on unavailable CIF content that are not found in the sheet

        Let's get started!
        ===
        """
    )

    print(introductory_paragraph)
