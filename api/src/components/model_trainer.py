import pandas as pd
import os
import sys
import pickle
from dataclasses import dataclass

import mlflow
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE

from src.logger import logging
from src.exception import CustomException

@dataclass
class ModelTrainerConfig:
    """
    This is a special class which is used for the path of model.
    """
    trained_model_path: str = os.path.join('artifacts', 'models', 'model.pkl')

class ModelTrainer:
    def __init__(self) -> None:
        self.model_trainer_config = ModelTrainerConfig()

    def load_data(self) -> pd.DataFrame:
        """
        This function loads the processed training dataset.
        """
        try:
            logging.info('Loading the training datasets.')
            train_processed = pd.read_csv('artifacts/processed/train.csv')
            logging.info('Training dataset loaded successsfully.')

            return train_processed
        except Exception as e:
            raise CustomException(e, sys)
        
    def train_model(self) -> LogisticRegression:
        """
        This function train and returns a Logistic Regression model.
        """
        try:

            params = {
                        'solver': 'sag', 
                        'C': 0.30488401774858853, 
                        'max_iter': 1311, 
                        'tol': 0.07272504817997558, 
                        'class_weight': None, 
                        'fit_intercept': True, 
                        'intercept_scaling': 0.2339737361256624
                    }

            logging.info('Model training started.')
            train_processed = self.load_data()
            X_train = train_processed.drop('Churn', axis=1)
            y_train = train_processed['Churn']

            mlflow.set_experiment('Customer Churn Prediction')

            with mlflow.start_run():
                
                model = LogisticRegression(**params, random_state=42)
                model.fit(X_train, y_train)

                mlflow.log_params(params)
                mlflow.sklearn.log_model(model, 'model')

                logging.info('Model trained successfully.')

            return model
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def save_model(self) -> None:
        """
        This function saves the trained model.
        """
        try:
            model = self.train_model()
            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_path), exist_ok=True)

            logging.info('Saving the trained model.')
            with open(self.model_trainer_config.trained_model_path, 'wb') as f:
                pickle.dump(model, f)

            logging.info('Model saved successfully.')

        except Exception as e:
            raise CustomException(e, sys)
        
    def initialise(self):
        """
            This function will run the entire model trainer script.
        """
        self.save_model()

if __name__ == '__main__':
    model_trainer = ModelTrainer()
    model_trainer.initialise()