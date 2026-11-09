"""Keep writable user data outside the replaceable portable application files."""
import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent


def workbook_path(default_directory: Path = APP_DIR) -> Path:
    directory = os.environ.get('ENERGY_REPORT_DATA_DIR')
    if directory:
        return Path(directory).expanduser().resolve() / 'DataMaster.xlsx'

    app_directory = Path(default_directory)
    data_directories = [app_directory / 'data']
    if app_directory.name.casefold() == 'app':
        data_directories.append(app_directory.parent / 'data')
    for data_directory in data_directories:
        workbook = data_directory / 'DataMaster.xlsx'
        if workbook.is_file():
            return workbook
    return app_directory / 'DataMaster.xlsx'


def report_output_directory(default_directory: Path = APP_DIR) -> Path:
    directory = os.environ.get('ENERGY_REPORT_OUTPUT_DIR')
    return Path(directory).expanduser().resolve() if directory else Path(default_directory).resolve()
