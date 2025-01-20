from os import write

import extraction
import transformation
from load import DatabaseLoader

def main():
    #Extract data
    file_path = "../../resources/UsedCarDataset.csv"
    raw_data = extraction.extract_data(file_path)
    #print(raw_data.columns)

    #Transform data
    transformed_data = transformation.transform_data(raw_data)
    transformed_data.to_csv("transformed_data.csv", index=False)


    #Load data into database
    #config_file = "../../utils/config/db_config.yaml"
    #with DatabaseLoader(config_file) as db_loader:
    #    db_loader.load_data(transformed_data)

if __name__ == "__main__":
    main()