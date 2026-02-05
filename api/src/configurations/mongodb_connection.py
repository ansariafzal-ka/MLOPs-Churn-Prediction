import sys
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from src.exception import CustomException
from src.logger import logging

class MongoDBConnection:
    """
    This class will connect to the remote Mongodb Atlas where the data is stored.
    """
    client = None
    def __init__(self) -> None:
        try:
            load_dotenv()
            if MongoDBConnection.client is None:
                self.initialise_mongodb()
        except Exception as e:
            raise CustomException(e, sys)

    def initialise_mongodb(self) -> None:
        try:
            MONGODB_URI = os.getenv('MONGODB_URI')
            MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
            MongoDBConnection.client = MongoClient(MONGODB_URI)
            self.database = MongoDBConnection.client[MONGODB_DATABASE]
            logging.info('Connected to Mongodb.')
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == '__main__':
    connection = MongoDBConnection()