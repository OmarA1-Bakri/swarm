# csv_handler.py

# csv_handler.py

import pandas as pd
import logging


def read_csv(file_path):
    try:
        return pd.read_csv(file_path, index_col="Company Name")
    except FileNotFoundError:
        logging.error(f"The file at {file_path} was not found.")
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        logging.error(f"The file at {file_path} is empty.")
        raise pd.errors.EmptyDataError(f"The file at {file_path} is empty.")
    except pd.errors.ParserError:
        logging.error(f"There was a parsing error in the file at {file_path}.")
        raise pd.errors.ParserError(
            f"There was a parsing error in the file at {file_path}."
        )
    except ValueError as e:
        logging.error(f"Error reading CSV file at {file_path}: {e}")
        raise ValueError(f"Error reading CSV file at {file_path}: {e}")


def write_csv(data, file_path):
    try:
        data.to_csv(file_path)
    except FileNotFoundError:
        logging.error(f"The directory for the file path {file_path} does not exist.")
        raise FileNotFoundError(
            f"The directory for the file path {file_path} does not exist."
        )
    except PermissionError:
        logging.error(f"Permission denied when writing to {file_path}.")
        raise PermissionError(f"Permission denied when writing to {file_path}.")
    except ValueError as e:
        logging.error(f"Error writing CSV file at {file_path}: {e}")
        raise ValueError(f"Error writing CSV file at {file_path}: {e}")
