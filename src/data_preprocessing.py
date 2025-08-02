import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self, df):
        try:
            logger.info("Started data preprocessing")

            df.drop(columns = ['Unnamed: 0','Booking_ID'] , axis = 1, inplace=True)
            logger.info("Dropped booking_id and unamed: 0 columns")
            
            df.drop_duplicates(inplace=True)
            logger.info("Removed duplicates")

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            lb = LabelEncoder()
            mappings={}
            for i in cat_cols:
                df[i] = lb.fit_transform(df[i])
                mappings[i] = {label: code for label,code in zip(lb.classes_, lb.transform(lb.classes_))}
            logger.info("Applied label encoding")
            logger.info("Label mappings are: ")
            for col, maps in mappings.items():
                logger.info(f"{col} : {maps}")

            skewness_thresh = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x:x.skew())
            for col in skewness[skewness>skewness_thresh].index:
                df[col] = np.log1p(df[col])
            logger.info("Removed potential skewness from the data")

            return df

        except Exception as e:
            logger.error("Error preprocessing the data")
            raise CustomException("Error preprocessing the data", e)
    
    def balance_data(self, df):
        try:
            x = df.drop(columns=['booking_status'], axis=1)
            y = df['booking_status']

            smote = SMOTE(random_state=42)
            x_res, y_res = smote.fit_resample(x, y)
            balanced_df = pd.DataFrame(x_res, columns=x.columns)
            balanced_df['booking_status'] = y_res

            logger.info("Data balanced successfully")

            return balanced_df

        except CustomException as e:
            logger.error("Error in balancing the data")
            raise CustomException("Error in balancing the data", e)
    
    def select_features(self, df):
        try:
            model = RandomForestClassifier(random_state=42)
            x = df.drop(columns = ['booking_status'], axis=1)
            y = df['booking_status']
            model.fit(x,y)
            logger.info("Feature selection model fitted")
            feature_importance = model.feature_importances_
            feature_df = pd.DataFrame({
                                        "Features": x.columns,
                                        "Importance": feature_importance
                                    })
            logger.info("Created important featured dataframe")
            top_features = feature_df.sort_values(by="Importance", ascending=False)

            num_features_to_select = self.config["data_processing"]["no_of_features"]
            top_10_features = top_features["Features"].head(num_features_to_select).values
            top_10_df = df[top_10_features.tolist()+["booking_status"]]

            logger.info("Completed feature selection successfully")
            logger.info(f"Top 10 features are: {top_10_features}")

            return top_10_df
        
        except Exception as e:
            logger.error("Error in selecting features from the data")
            raise CustomException("Error in selecting features form the data", e)
    
    def save_data(self, df, path):
        try:
            df.to_csv(path, index=False)
            logger.info(f"Successfully saved the processed data to {path}")

        except Exception as e:
            logger.error("Error saving the data")
            raise CustomException("Error saving the data", e)
    
    def process(self):
        try:
            logger.info("Loading the data to preprocess")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df,PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed successfully")

        except Exception as e:
            logger.error("Error in processing the data")
            raise CustomException("Error in processing the data", e)
        
if __name__=="__main__":
    p = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    p.process()





