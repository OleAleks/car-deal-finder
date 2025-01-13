import pandas as pd

def extract_data(file_path: str) -> pd.DataFrame:
    """
        Reads the CSV file and extracts the raw data into a DataFrame.

        :param file_path: Path to the Used Cars CSV file
        :return: Pandas DataFrame containing raw data
    """
    try:
        # Load the CSV file into a DataFrame
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error reading the file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error


def main() -> None:
    file_path = "../../resources/UsedCarDataset.csv"
    raw_data = extract_data(file_path)

    # Example: Print first 5 rows of raw data
    print("Extracted Data (first 5 rows):")
    print(raw_data.head())

    # Example: Display column names
    print("\nColumns in the dataset:")
    print(raw_data.columns)


if __name__ == "__main__":
    main()
