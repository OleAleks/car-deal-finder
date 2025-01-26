import sqlite3
import yaml


class DatabaseLoader:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.connection = None
        self.cursor = None
        self.database_path = self.config["database"]["paths"]["database"]

    def __enter__(self):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()  # Create a cursor
        self.create_tables()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def load_config(self
                    , config_file
                    ):
        """Load configuration from a YAML file.

        :param config_file: Path to yaml configuration file
        """
        with open(config_file, "r") as file:
            return yaml.safe_load(file)

    def create_tables(self):

        """Create tables in the SQLite database using queries from the config."""

        table_creation_queries = [
            "create_brands_table",
            "create_models_table",
            "create_transmission_table",
            "create_owners_table",
            "create_fuel_types_table",
            "create_cars_table"
        ]
        for query_key in table_creation_queries:
            create_table_query = self.config["database"]["queries"][query_key]
            self.cursor.execute(create_table_query)
        self.connection.commit()

    def load_transformed_data(self,
                              df
                              ) -> None:

        """
            Load transformed data into normalized database
        :param df: Transformed DataFrame
        """
        # Insert unique lookup data
        lookup_insertions = [
            ("insert_brand", "brand"),
            ("insert_transmission", "transmission"),
            ("insert_owner", "owner"),
            ("insert_fuel_type", "fueltype")
        ]
        for query_key, column in lookup_insertions:
            insert_query = self.config["database"]["queries"][query_key]
            unique_values = df[column].unique()
            for value in unique_values:
                self.cursor.execute(insert_query, (value,))

        # Insert models
        insert_model_query = self.config["database"]["queries"]["insert_model"]
        unique_models = df[["brand", "model"]].drop_duplicates()
        for _, row in unique_models.iterrows():
            self.cursor.execute(insert_model_query, (row["brand"], row["model"]))

        # Insert cars
        insert_car_query = self.config["database"]["queries"]["insert_car"]
        for _, row in df.iterrows():
            try:
                self.cursor.execute(insert_car_query, (
                    row["brand"],  # brand_name for brand_id
                    row["model"],
                    row["brand"],  # brand_name again for model_id lookup
                    row["year"],
                    row["age"],
                    row["kmdriven"],
                    row["transmission"],
                    row["owner"],
                    row["fueltype"],
                    row["askprice"],
                    row["priceperkm"],
                    row["brand_model"],
                    row["priceperkm_mean"],
                    row["relativeprice"],
                    row["priceclassification"]
                ))
            except sqlite3.Error as e:
                print(f"Error inserting car: {e}")
                print(f"Problematic row: {row}")
                return e
        self.connection.commit()
        print(f"Successfully inserted {len(df)} transformed car records")
