from app.compare import match_entry
from app.util import folder


def run_match_option(script_dir_path):
    # Choose folder with cif files
    cif_dir_path = folder.choose_dir(script_dir_path)
    match_entry.get_new_excel_with_matching_entries(
        cif_dir_path, script_dir_path
    )
