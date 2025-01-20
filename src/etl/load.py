import sqlite3
import pandas as pd
import yaml


class DatabaseLoader:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.config["database"]["name"])
        self.cursor = self.connection.cursor()  # Create a cursor
        self.create_tables()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def load_config(self, config_file):
        """Load configuration from a YAML file."""
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)

    def create_tables(self):

        """Create tables in the SQLite database using queries from the config."""
        create_cars_table = self.config["database"]["queries"]["create_cars_table"]
        create_additional_info_table = self.config["database"]["queries"]["create_additional_info_table"]

        self.cursor.execute(create_cars_table)
        self.cursor.execute(create_additional_info_table)
        self.connection.commit()

    def load_data(self, df):
        """Load data from DataFrame into the Cars table."""
        df.to_sql("Cars", self.connection, if_exists='append', index=False)

#def main():
    # Path to your config.yaml file
    #config_file = "/../utils/config/db_config.yaml"

    # Use the DatabaseLoader as a context manager
    #with DatabaseLoader(config_file) as db:
        #df =
        # Load data into the database
        # db_loader.load_data(df)
