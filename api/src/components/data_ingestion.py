import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException
from src.configurations.mongodb_connection import MongoDBConnection

@dataclass
class DataIngestionConfig:
    """
    This is a special class which is used for the paths of datasets.
    """
    raw_data_path: str = os.path.join('artifacts', 'raw', 'raw.csv')
    train_data_path: str = os.path.join('artifacts', 'raw', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'raw', 'test.csv')

class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig()

    def load_data(self) -> pd.DataFrame:
        """
        This function fetches the dataset from MongoDB Atlas and converts it into a pandas dataframe.
        """
        try:
            logging.info('Data Ingestion Started.')
            # Fetching the dataset
            mongodb = MongoDBConnection()
            collection = mongodb.database['churn-prediction']
            data = list(collection.find({}))

            # converting the dataset into a pandas DataFrame
            df = pd.DataFrame(data)

            # dropping the unnecessary _id column from MongoDB
            df.drop('_id', inplace=True, axis=1)
            logging.info('Dataset Fetched from MongoDB Successfully.')
            
            return df
        except Exception as e:
            raise CustomException(e, sys)

    def save_data(self) -> None:
        """
        This function splits the dataset into training and testing sets, and then saves the datasets into the artifacts/raw folder. 
        """
        try:
            df = self.load_data()

            # create the artifacts/raw directory
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            # saving the raw dataset
            logging.info('Saving the raw dataset.')
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # splitting the dataset into training and testing sets
            train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

            # saving the training and testing datasets
            logging.info('Saving the training dataset.')
            train_df.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            logging.info('Saving the testing dataset.')
            test_df.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info('Data Ingestion Completed.')

        except Exception as e:
            raise CustomException(e, sys)

    def initialise(self) -> None:
            """
            This function will run the entire data ingestion script.
            """
            self.save_data()

if __name__ == '__main__':
    data_ingestor = DataIngestion()
    data_ingestor.initialise()