import pandas as pd
import numpy as np

import os
import sys
import pickle
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from dataclasses import dataclass
from typing import Tuple


from src.logger import logging
from src.exception import CustomException

@dataclass
class DataProcessingConfig:
    """
    This is a special class which is used for the paths of datasets and preprocessor.
    """
    train_processed_data_path: str = os.path.join('artifacts', 'processed', 'train.csv')
    test_processed_data_path: str = os.path.join('artifacts', 'processed', 'test.csv')
    processor_data_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataProcessing:
    def __init__(self) -> None:
        self.processor_config = DataProcessingConfig()

    def load_data(self, train_path, test_path) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        This function loads the raw training and testing datasets
        """
        try:
            logging.info('Data Processing Started.')
            logging.info('Loading the raw datasets.')
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Raw datasets loaded successfully.')

            return (
                train_df,
                test_df
            )
        except Exception as e:
            raise CustomException(e, sys)
        

    def process_data(self, train_df, test_df)  -> Tuple[pd.DataFrame, pd.DataFrame, ColumnTransformer]:
        """
        This function processes the raw training and testing datasets.
        """
        try:

            logging.info('Processing the data...')
            # converting the TotalCharges feature into numeric
            train_df['TotalCharges'] = pd.to_numeric(train_df['TotalCharges'], errors='coerce')
            test_df['TotalCharges'] = pd.to_numeric(test_df['TotalCharges'], errors='coerce')

            # dropping the customerID column
            train_df.drop('customerID', axis=1, inplace=True)
            test_df.drop('customerID', axis=1, inplace=True)

            # separating numeric, categorical, target features
            log_feature = ['TotalCharges']
            numeric_features = train_df.select_dtypes(include=['int64', 'float64']).columns.difference(['SeniorCitizen', 'TotalCharges']).tolist()
            categorical_features = train_df.select_dtypes(include='object').columns.difference(['Churn']).tolist()

            # mapping the target feature Yes:1, No:0
            train_df['Churn'] = train_df['Churn'].map({'Yes': 1, 'No': 0})
            test_df['Churn'] = test_df['Churn'].map({'Yes': 1, 'No': 0})

            # replacing the No internet service and No phone service with No    
            for feature in categorical_features:
                if 'No internet service' in train_df[feature].unique():
                    train_df[feature] = train_df[feature].replace({
                        'No internet service': 'No'
                    })
                    test_df[feature] = test_df[feature].replace({
                        'No internet service': 'No'
                    })
                elif 'No phone service' in train_df[feature].unique():
                    train_df[feature] = train_df[feature].replace({
                        'No phone service': 'No'
                    })
                    test_df[feature] = test_df[feature].replace({
                        'No phone service': 'No'
                    })

            # skewed transformation pipeline
            log_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='constant', fill_value=0.0)),
                ('log_transform', FunctionTransformer(np.log1p, feature_names_out='one-to-one')),
                ('scaler', StandardScaler())
            ])

            # numeric transformation pipeline
            numeric_pipeline = Pipeline([
                ('scaler', StandardScaler())
            ])

            # categorical transformation pipeline
            categorical_pipeline = Pipeline([
                ('encoder', OneHotEncoder(handle_unknown='ignore'))
            ])

            # full pipeline
            preprocessor = ColumnTransformer([
                ('log', log_pipeline, log_feature),
                ('numeric', numeric_pipeline, numeric_features),
                ('categorical', categorical_pipeline, categorical_features)
            ])

            # separating X and y features
            X_train = train_df.drop('Churn', axis=1)
            X_test = test_df.drop('Churn', axis=1)

            y_train = train_df['Churn']
            y_test = test_df['Churn']

            # fitting the pipeline
            X_train_processed = preprocessor.fit_transform(X_train)
            X_test_processed = preprocessor.transform(X_test)

            # getting feature names
            feature_names = preprocessor.get_feature_names_out()

            # creating dataframes
            train_processed = pd.DataFrame(X_train_processed, columns=feature_names)
            test_processed = pd.DataFrame(X_test_processed, columns=feature_names)

            # adding the target feature
            train_processed['Churn'] = y_train.values
            test_processed['Churn'] = y_test.values

            logging.info('Processing Completed.')

            return (
                train_processed,
                test_processed,
                preprocessor
            )

        except Exception as e:
            raise CustomException(e, sys)

    def save_data(self, train_processed, test_processed, preprocessor) -> None:
        """
        This function saves the processed training and testing datasets, and the preprocessor object.
        """
        try:

            # create the artifacts/processed directory    
            os.makedirs(os.path.dirname(self.processor_config.train_processed_data_path), exist_ok=True)

            # saving the datasets
            train_processed.to_csv(self.processor_config.train_processed_data_path, index=False, header=True)
            test_processed.to_csv(self.processor_config.test_processed_data_path, index=False, header=True)

            # saving the preprocessor
            with open(self.processor_config.processor_data_path, 'wb') as f:
                pickle.dump(preprocessor, f)

            logging.info('Datasets and Processor saved successfully.')

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == '__main__':

    train_path = 'artifacts/raw/train.csv'
    test_path = 'artifacts/raw/test.csv'

    data_processor = DataProcessing()

    train_df, test_df = data_processor.load_data(train_path, test_path)
    train_processed, test_processed, preprocessor = data_processor.process_data(train_df, test_df)
    data_processor.save_data(train_processed, test_processed, preprocessor)