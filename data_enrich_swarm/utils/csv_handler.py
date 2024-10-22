# csv_handler.py

import pandas as pd
import logging


def read_csv(file_path):
    """
    Reads a CSV file into a pandas DataFrame, using 'Company Name' as the index column.

    Args:
        file_path (str): The path to the CSV file to be read.

    Returns:
        pd.DataFrame: DataFrame containing the CSV data.

    Raises:
        FileNotFoundError: If the file does not exist at the specified path.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error in the file.
        ValueError: For any other errors encountered during reading.
    """
    try:
        # Attempt to read the CSV file with 'Company Name' as the index column
        return pd.read_csv(file_path, index_col="Company Name")
    except FileNotFoundError:
        # Log and raise an error if the file is not found
        logging.error(f"The file at {file_path} was not found.")
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        # Log and raise an error if the file is empty
        logging.error(f"The file at {file_path} is empty.")
        raise pd.errors.EmptyDataError(f"The file at {file_path} is empty.")
    except pd.errors.ParserError:
        # Log and raise an error if there is a parsing issue
        logging.error(f"There was a parsing error in the file at {file_path}.")
        raise pd.errors.ParserError(
            f"There was a parsing error in the file at {file_path}."
        )
    except ValueError as e:
        # Log and raise any other value errors encountered
        logging.error(f"Error reading CSV file at {file_path}: {e}")
        raise ValueError(f"Error reading CSV file at {file_path}: {e}")


def write_csv(data, file_path):
    """
    Writes a pandas DataFrame to a CSV file.

    Args:
        data (pd.DataFrame): The DataFrame to be written to a CSV file.
        file_path (str): The path where the CSV file will be saved.

    Raises:
        FileNotFoundError: If the directory for the file path does not exist.
        PermissionError: If there is a permission issue when writing the file.
        ValueError: For any other errors encountered during writing.
    """
    try:
        # Attempt to write the DataFrame to a CSV file
        data.to_csv(file_path)
    except FileNotFoundError:
        # Log and raise an error if the directory does not exist
        logging.error(f"The directory for the file path {file_path} does not exist.")
        raise FileNotFoundError(
            f"The directory for the file path {file_path} does not exist."
        )
    except PermissionError:
        # Log and raise an error if there is a permission issue
        logging.error(f"Permission denied when writing to {file_path}.")
        raise PermissionError(f"Permission denied when writing to {file_path}.")
    except ValueError as e:
        # Log and raise any other value errors encountered
        logging.error(f"Error writing CSV file at {file_path}: {e}")
        raise ValueError(f"Error writing CSV file at {file_path}: {e}")
