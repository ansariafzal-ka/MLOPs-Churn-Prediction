import pandas as pd
import matplotlib.pyplot as plt
import sys
import pickle

import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, precision_score, f1_score, roc_curve, roc_auc_score, classification_report

from src.logger import logging
from src.exception import CustomException

class ModelEvaluation:

    def load_data(self, test_processed_path) -> pd.DataFrame:
        """
        This function loads the processed testing dataset.
        """
        try:
            test_processed_df = pd.read_csv(test_processed_path)
            return test_processed_df
        except Exception as e:
            raise CustomException(e, sys)
    
    def load_model(self, model_path) -> LogisticRegression:
        """
        This function loads the trained model.
        """
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
                return model
        except Exception as e:
            raise CustomException(e, sys)
        
    def evaluate_model(self, test_processed_df, model):
        """
        This function evaluates the trained model on the testing dataset.
        """
        try:
            logging.info('Model evaluation started.')

            X_test = test_processed_df.drop('Churn', axis=1)
            y_test = test_processed_df['Churn']

            logging.info('Making predictions on test data...')

            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:,1]

            logging.info('Calculating metrics...')
            recall = recall_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            auc_score = roc_auc_score(y_test, y_prob)
            fpr, tpr, thresholds = roc_curve(y_test, y_prob)

            fig = plt.figure(figsize=(6, 4))
            plt.plot(fpr, tpr, label=f'Logistic Regression (AUC={auc_score:.3f})')
            plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
            plt.grid(True, alpha=0.3)
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('ROC curve for Logistic Regression')
            plt.legend()

            mlflow.set_experiment('Churn Prediction')

            with mlflow.start_run(run_name='model_evaluation'):
                mlflow.log_metric('recall', recall)
                mlflow.log_metric('precision', precision)
                mlflow.log_metric('f1_score', f1)
                mlflow.log_metric('auc_score', auc_score)

                mlflow.log_figure(fig, 'roc_curve.png')
                plt.close()

            logging.info(f'Recall: {recall:.3f}, Precision: {precision:.3f}, F1 Score: {f1:.3f} AUC Score: {auc_score:.3f}')
            logging.info('Model evaluation completed.')
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == '__main__':
    test_processed_path = 'artifacts/processed/test.csv'
    model_path = 'artifacts/models/model.pkl'

    model_evaluator = ModelEvaluation()
    test_processed_df = model_evaluator.load_data(test_processed_path)
    model = model_evaluator.load_model(model_path)
    model_evaluator.evaluate_model(test_processed_df, model)