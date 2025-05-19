import os

import click


def handle_errors(errors_df, chosen_file, Output_folder):
    """Handle errors found in the DataFrame."""
    if not errors_df.empty:
        click.secho("Errors found:", fg="red")
        click.echo(errors_df)
        error_file_path = os.path.join(
            Output_folder,
            f"{os.path.splitext(os.path.basename(chosen_file))[0]}_errors.xlsx",
        )
        errors_df.to_excel(error_file_path, index=False)
        click.secho(f"Errors saved to: {error_file_path}", fg="cyan")
    else:
        click.secho("No errors found in the DataFrame.", fg="green")
