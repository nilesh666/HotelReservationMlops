import os 
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import lightgbm as lgb
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path
        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f"Loading train data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading test data from {self.test_path}")
            test_df = load_data(self.test_path)

            x_train = train_df.drop(columns=['booking_status'],axis=1)
            y_train = train_df['booking_status']

            x_test = test_df.drop(columns=['booking_status'],axis=1)
            y_test = test_df['booking_status']

            logger.info("Data splitted for model training")

            return x_train, y_train, x_test, y_test

        except Exception as e:
            logger.error("Error in loading and splitting the data")
            raise CustomException("Error in loading and splitting the data", e)
    
    def train_lgbm(self, x_train, y_train):
        try:
            logger.info("Initialized model")
            model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("Hyperparameter tuning started")

            random_search = RandomizedSearchCV(
                estimator=model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params["n_iter"],
                cv = self.random_search_params["cv"],
                n_jobs=self.random_search_params["n_jobs"],
                verbose = self.random_search_params["verbose"],
                random_state=self.random_search_params["random_state"],
                scoring = self.random_search_params["scoring"]
            )

            logger.info("Training started with hyperparameter tuning")

            random_search.fit(x_train, y_train)

            logger.info("Hyperparameter tuning completed")

            best_params = random_search.best_params_
            best_model = random_search.best_estimator_

            logger.info(f"Best parameters are {best_params}")

            return best_model

        except Exception as e:
            logger.error("Error in training the model")
            raise CustomException("Error in training the model", e)
        
    def evaluate_model(self, model, x_test, y_test):
        try:
            logger.info("Evlauating the model")
            y_pred = model.predict(x_test)

            acc = accuracy_score(y_test, y_pred)
            p = precision_score(y_test, y_pred)
            r = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(f"Accuracy: {acc}")
            logger.info(f"Precision: {p}")
            logger.info(f"Recall: {r}")
            logger.info(f"F1_score: {f1}")

            return {
                "Accuracy": acc,
                "Precision": p,
                "Recall": r,
                "F1_score": f1
            }

        except Exception as e:
            logger.error("Error in evaluating the model")
            raise CustomException("Error in evaluating the model", e)
    
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            logger.info("Saving the model")

            joblib.dump(model, self.model_output_path)
            logger.info(f"Saved the model to {self.model_output_path}")

        except Exception as e:
            logger.error("Error in saving the model")
            raise CustomException("Error in saving the model", e)
        
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Stareted model training piepline")
                logger.info("Starting MLflow experimentation")

                mlflow.log_artifact(self.train_path, artifact_path = "datasets")
                mlflow.log_artifact(self.test_path, artifact_path = "datasets")

                x_train, y_train, x_test, y_test = self.load_and_split_data()
                best_model = self.train_lgbm(x_train, y_train)
                metrics = self.evaluate_model(best_model, x_test, y_test)
                self.save_model(best_model)

                mlflow.log_artifact(self.model_output_path)
                mlflow.log_params(best_model.get_params())
                mlflow.log_metrics(metrics)


                logger.info("Completed training pipeline successfully")

        except Exception as e:
            logger.error("Error in training pipeline")
            raise CustomException("Error in training pipline", e)
        
if __name__=="__main__":
    m = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    m.run()

        