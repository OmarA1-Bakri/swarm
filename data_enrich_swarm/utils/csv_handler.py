# csv_handler.py

import pandas as pd


def read_csv(file_path):
    """
    Reads a CSV file into a pandas DataFrame, using 'Company Name' as the index column.

    Args:
        file_path (str): The path to the CSV file to be read.

    Returns:
        DataFrame: A pandas DataFrame containing the data from the CSV file.

    Raises:
        FileNotFoundError: If the file at the specified path does not exist.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If there is a parsing error in the CSV file.
        ValueError: If 'Company Name' is not a column in the CSV file.
    """
    try:
        return pd.read_csv(file_path, index_col="Company Name")
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"The file at {file_path} is empty.")
    except pd.errors.ParserError:
        raise pd.errors.ParserError(
            f"There was a parsing error in the file at {file_path}."
        )
    except ValueError as e:
        raise ValueError(f"Error reading CSV file at {file_path}: {e}")


def write_csv(data, file_path):
    """
    Writes a pandas DataFrame to a CSV file.

    Args:
        data (DataFrame): The pandas DataFrame to be written to a CSV file.
        file_path (str): The path where the CSV file will be saved.

    Raises:
        FileNotFoundError: If the directory for the file path does not exist.
        PermissionError: If there is a permission error when writing the file.
        ValueError: If the data provided is not a valid DataFrame.
    """
    try:
        data.to_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"The directory for the file path {file_path} does not exist."
        )
    except PermissionError:
        raise PermissionError(f"Permission denied when writing to {file_path}.")
    except ValueError as e:
        raise ValueError(f"Error writing CSV file at {file_path}: {e}")
