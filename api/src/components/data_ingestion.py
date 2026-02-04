import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifacts', 'raw', 'raw.csv')
    train_data_path: str = os.path.join('artifacts', 'raw', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'raw', 'test.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def load_data(self) -> pd.DataFrame:
        try:
            logging.info('Data Ingestion Started.')
            # loading the dataset
            df = pd.read_csv('C:/Users/ansar/Desktop/Workspace/Personal/MLOPs/Customer Churn Prediction/api/customer_churn_data.csv')
            logging.info('Dataset Loaded Successfully.')
            return df
        except Exception as e:
            raise CustomException(e, sys)

    def save_data(self):
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

    def initialise(self):
            # This function will run the entire data ingestion script.
            self.save_data()