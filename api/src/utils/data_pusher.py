import pandas as pd
from src.configurations.mongodb_connection import MongoDBConnection

def upload_to_mongodb() -> None:

    """
    This function is a helper function which is used to push the csv data to the remote MongoDB Atlas
    """

    mongodb = MongoDBConnection()

    df = pd.read_csv('C:/Users/ansar/Desktop/Workspace/Personal/MLOPs/Customer Churn Prediction/api/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    data = df.to_dict('records')
    collection = mongodb.database['churn-prediction']
    collection.insert_many(data)
    print('Data Stored in MongoDB.')