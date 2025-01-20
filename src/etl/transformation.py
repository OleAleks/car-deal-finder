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


def update_car_age(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the age of the car based on the current year.

    :param df: DataFrame containing the car data.
    :return df: DataFrame with added 'CarAge' column.
    """
    current_year = pd.Timestamp.now().year
    df["Age"] = current_year - df["Year"]
    return df

def categorize_price(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize cars into price categories.

    :param df: DataFrame containing the car data.
    :return df: DataFrame with added 'PriceCategory' column.
    """
    bins = [0, 500000, 1000000, 1500000, np.inf]
    labels = ['Budget', 'Mid-range', 'Luxury']
    df['PriceCategory'] = pd.cut(df['AskPrice'], bins=bins, labels=labels, right=False)
    return df


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
        if kilometer > 0:
            price_per_km = price / kilometer
            return float(price_per_km)
        else:
            price_per_km = -1
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
        # Exclude rows with PricePerKm == -1 from the calculation
        valid_rows = df["PricePerKm"] != -1

        # Calculate the mean PricePerKm for each Brand_Model
        # Group df by "Brand_Model" and calculate average "PricePerKm" for each group.
        # assign result to new column "PricePerKM_mean"
        df.loc[valid_rows, "PricePerKM_mean"] = df.groupby("Brand_Model")["PricePerKm"].transform("mean")

        # Calculate the relative price by dividing each car's "PricePerKm" by "PricePerKM_mean"(of Brand_Model).
        # RelativePrice == 1 means the car is priced at the average.
        # RelativePrice > 1 indicates the car is more expensive than average.
        # RelativePrice < 1 indicates the car is cheaper than average.
        df.loc[valid_rows, "RelativePrice"] = df["PricePerKm"] / df["PricePerKM_mean"]

        # Assign -1 to RelativePrice for invalid rows with PricePerKm == -1
        df.loc[~valid_rows, "RelativePrice"] = -1

        return df

    except KeyError as e:
        print(f"KeyError: {e}")
        return e
    except ZeroDivisionError as e:
        print("Error: Division by zero encountered in relative price calculation.")
        return e


def filter_data(df: pd.DataFrame, brand: str = None, model: str = None, year_range: tuple = None,
                age_range: tuple = None, km_driven_range: tuple = None, transmission: str = None,
                owner: str = None, fuel_type: str = None, ask_price_range: tuple = None,
                relative_price_range: tuple = None, car_age_range: tuple = None) -> pd.DataFrame:
    """
    Filter the DataFrame based on user input for multiple attributes.

    :param df: DataFrame containing the car data.
    :param brand: Specific brand to filter by.
    :param model: Specific model to filter by.
    :param year_range: Tuple containing min and max year.
    :param age_range: Tuple containing min and max age.
    :param km_driven_range: Tuple containing min and max kilometers driven.
    :param transmission: Specific transmission type to filter by.
    :param owner: Specific owner type to filter by.
    :param fuel_type: Specific fuel type to filter by.
    :param ask_price_range: Tuple containing min and max asking price.
    :param relative_price_range: Tuple containing min and max relative price.
    :param car_age_range: Tuple containing min and max car age.
    :return: Filtered DataFrame.
    """
    # Filter by brand
    if brand:
        df = df[df['Brand'] == brand]

    # Filter by model
    if model:
        df = df[df['model'] == model]

    # Filter by year range
    if year_range:
        df = df[df['Year'].between(year_range[0], year_range[1])]

    # Filter by age range
    if age_range:
        df = df[df['Age'].between(age_range[0], age_range[1])]

    # Filter by kilometers driven range
    if km_driven_range:
        df = df[df['kmDriven'].between(km_driven_range[0], km_driven_range[1])]

    # Filter by transmission
    if transmission:
        df = df[df['Transmission'] == transmission]

    # Filter by owner
    if owner:
        df = df[df['Owner'] == owner]

    # Filter by fuel type
    if fuel_type:
        df = df[df['FuelType'] == fuel_type]

    # Filter by asking price range
    if ask_price_range:
        df = df[df['AskPrice'].between(ask_price_range[0], ask_price_range[1])]

    # Filter by relative price range
    if relative_price_range:
        df = df[df['RelativePrice'].between(relative_price_range[0], relative_price_range[1])]

    # Filter by car age range
    if car_age_range:
        df = df[df['CarAge'].between(car_age_range[0], car_age_range[1])]

    return df

def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    # Exclude rows with NULL in kmDriven
    data = data[data['kmDriven'].notna()].copy()

    data["AskPrice"] = list(map(clean_price, data["AskPrice"]))
    data["kmDriven"] = list(map(clean_km, data["kmDriven"]))
    data["PricePerKm"] = list(map(calculate_price_per_km, data["AskPrice"], data["kmDriven"]))
    data["Year"] = data["Year"].astype(int)

    data = update_car_age(data)
    data = create_brand_model_column(data)
    data = calculate_relative_price(data)

    return data
