import extraction
import pandas as pd
import numpy as np

def clean_price(price: str) -> float:
    """
        Cleans and converts the price field from a string to a float.

        :param price: string
        :return: Numeric price as float
    """
    if pd.isna(price):
        return np.nan  # Handle missing values

    try:
        price = price.replace("₹", "").replace(",", "").strip()
        return float(price)
    except (ValueError, TypeError):
        return np.nan


def clean_km(kilometer: str) -> float:
    """
        Cleans and converts the kilometer driven field from a string to a float.
        Problem: what if null?

        :param kilometer: string
        :return: Numeric kilometers as float
    """
    if pd.isna(kilometer):
        return np.nan  # Handle missing values

    try:
        kilometer = kilometer.replace("km", "").replace(",", "").strip()
        return float(kilometer)
    except (ValueError, TypeError):
        return np.nan


def calculate_price_per_km(price: float, kilometer: float) -> float:
    """
        Calculates price per kilometer driven.

        :param price: float
        :param kilometer: float
        :return: Numeric price_per_km as float
    """
    if pd.isna(price) or pd.isna(kilometer):
        return np.nan

    try:
        price_per_km = price / kilometer
        return float(price_per_km)
    except (ValueError, TypeError, ZeroDivisionError):
        return np.nan

def create_brand_model_column(df: pd.DataFrame) -> pd.DataFrame:
    """
        Combines brand and model columns into a single column.

        :param df:
        :return df:
    """
    #cleaning model column
    try:
        df["model"] = df["model"].str.strip() # Remove extra spaces
        df["model"] = df["model"].str.replace( " ", "-")  # replace blank spaces within          data = np.char.replace(data, ",", ".")  # Replace commas with dots
        df["model"] = df["model"].str.lower() #convert to lowercase
    except ValueError as e:
        return e
    df["Brand_Model"] = df["Brand"] +" "+ df["model"]
    return df

def calculate_relative_price(df: pd.DataFrame) -> pd.DataFrame:
    """
        Calculate the price per kilometer relative to the brand_model average price per kilometer.

        :param df:
        :return df: df with added column PricePerKM_mean and RelativePrice
    """

    try:
        # Calculate the mean PricePerKm for each Brand_Model
        # Group df by "Brand_Model" and calculate average "PricePerKm" for each group.
        # assign result to new column "PricePerKM_mean"
        df.loc[:, "PricePerKM_mean"] = df.groupby("Brand_Model")["PricePerKm"].transform("mean")

        # Calculate the relative price by dividing each car's "PricePerKm" by "PricePerKM_mean"(of Brand_Model).
        # RelativePrice == 1 means the car is priced at the average.
        # RelativePrice > 1 indicates the car is more expensive than average.
        # RelativePrice < 1 indicates the car is cheaper than average.
        df.loc[:, "RelativePrice"] = df["PricePerKm"] / df["PricePerKM_mean"]

        return df

    except KeyError as e:
        print(f"KeyError: {e}")
        return e
    except ZeroDivisionError as e:
        print("Error: Division by zero encountered in relative price calculation.")
        return e

def find_best_deals(df, n=10):
    """
        Finds the top n deals based on the RelativePrice

        :param df (pandas.DataFrame): DataFrame containing the car data.
            top_n (int): Number of top deals to return.

        :return df: df containing the top n deals.
    """
    try:
        df = df.sort_values(by="RelativePrice")
        return df.head(n)
    except KeyError as e:
        return e



def main():
    file_path = "../../resources/UsedCarDataset.csv"
    data = extraction.extract_data(file_path)

    # Clean specific columns
    data["AskPrice"] = list(map(clean_price, data["AskPrice"])) #.apply anstatt map?
    data["kmDriven"] = list(map(clean_km, data["kmDriven"]))
    data["PricePerKm"] = list(map(calculate_price_per_km, data["AskPrice"], data["kmDriven"]))
    data["Year"] = list(map(int, data["Year"]))  # Ensure Year is integer

    #print(data["PricePerKm"].head())

    #print(data["model"].value_counts())

    print(create_brand_model_column(data))

    #print(data["Brand_Model"].value_counts())

    data = calculate_relative_price(data)
    print(isinstance(data, pd.DataFrame))

    data = find_best_deals(data, 10)

    # Example: Perform simple analyses
    #print(f"Minimum price: {min(data['AskPrice'])}")
    #print(f"Maximum price: {max(data['AskPrice'])}")
    #print(f"Average kilometers driven: {sum(data['kmDriven']) / len(data['kmDriven']):.2f}")


if __name__ == "__main__":
    main()
