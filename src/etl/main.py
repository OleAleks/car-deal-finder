import yaml
import extraction
import transformation
from load import DatabaseLoader

def main():
    config_file = '../../utils/config/db_config.yaml'

    with open(config_file) as file:
        config = yaml.safe_load(file)

    database_path = config['database']['paths']['database']

    #Extract data
    raw_data = extraction.extract_data(config['database']['paths']['raw_data'])
    #print(raw_data.columns)

    #Transform data
    transformed_data = transformation.transform_data(raw_data)
    #save data to csv for loading
    transformed_data.to_csv(config['database']['paths']['transformed_csv']
                            , index=False)

    #Load data into database
    #config_file = "../../utils/config/db_config.yaml"
    with DatabaseLoader(config_file) as db_loader:
        db_loader.load_transformed_data(transformed_data)

if __name__ == "__main__":
    main()