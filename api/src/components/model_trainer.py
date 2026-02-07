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

    def load_data(self, train_processed_path) -> pd.DataFrame:
        """
        This function loads the processed training dataset.
        """
        try:
            logging.info('Loading the training datasets.')
            train_processed_df = pd.read_csv(train_processed_path)
            logging.info('Training dataset loaded successsfully.')

            return train_processed_df
        except Exception as e:
            raise CustomException(e, sys)
        
    def train_model(self, params, train_processed_df) -> LogisticRegression:
        """
        This function train and returns a Logistic Regression model.
        """
        try:

            logging.info('Model training started.')
            X_train = train_processed_df.drop('Churn', axis=1)
            y_train = train_processed_df['Churn']

            smote = SMOTE(random_state=42)
            X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
            print(f'Shape: ({X_train_resampled.shape}), ({y_train_resampled.shape})')

            mlflow.set_experiment('Churn Prediction')

            with mlflow.start_run(run_name='model_training'):
                
                model = LogisticRegression(**params, random_state=42)
                model.fit(X_train_resampled, y_train_resampled)

                mlflow.log_params(params)
                mlflow.sklearn.log_model(model, name='model')

                logging.info('Model trained successfully.')

            return model
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def save_model(self, model) -> None:
        """
        This function saves the trained model.
        """
        try:
            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_path), exist_ok=True)

            logging.info('Saving the trained model.')
            with open(self.model_trainer_config.trained_model_path, 'wb') as f:
                pickle.dump(model, f)

            logging.info('Model saved successfully.')

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == '__main__':

    train_processed_path = 'artifacts/processed/train.csv'

    params = {
                'solver': 'sag', 
                'C': 0.30488401774858853, 
                'max_iter': 1311, 
                'tol': 0.07272504817997558, 
                'class_weight': None, 
                'fit_intercept': True, 
                'intercept_scaling': 0.2339737361256624
            }

    model_trainer = ModelTrainer()
    train_processed_df = model_trainer.load_data(train_processed_path)
    model = model_trainer.train_model(params, train_processed_df)
    model_trainer.save_model(model)