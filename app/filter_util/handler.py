import os

import click

# Save files that have errors and save the dataframe
# These are usually files that are valid


def handle_errors(errors_df, chosen_file, Output_folder):
    """Handle errors found in the DataFrame."""
    if not errors_df.empty:
        click.secho("Errors found:", fg="red")
        click.echo(errors_df)
        base_name = os.path.splitext(os.path.basename(chosen_file))[0]
        error_filename = f"{base_name}_errors.xlsx"
        error_file_path = os.path.join(Output_folder, error_filename)
        errors_df.to_excel(error_file_path, index=False)
        click.secho(f"Errors saved to: {error_file_path}", fg="cyan")
    else:
        click.secho("No errors found in the DataFrame.", fg="green")
