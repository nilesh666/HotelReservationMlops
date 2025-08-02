import os 
import pandas as pd
from sklearn.model_selection import train_test_split
from google.cloud import storage
from src.custom_exception import CustomException
from src.logger import get_logger
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Data ingestion started with {self.bucket_name} bucket and the bucket file is {self.bucket_file_name}")

    def download_csv_from_gcp(self):  
        try:       

            client = storage.Client()
            print(f"Client:{type(client)}")
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)
            print(f"bucket variable : {type(bucket)}")
            print(f"blob variable: {type(blob)}")

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"CSV successfully downloaded to {RAW_FILE_PATH}")
            
        except Exception as e:
            logger.error("Error downloading csv")
            raise CustomException("Error downlaoding csv from gcp", e)
        
    def split_data(self):
        try:
            logger.info("Spllting the data started")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size=1-self.config["train_ratio"], random_state = 42)
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            logger.info("Split completed and saved the train, test successfully")

        except Exception as e:
            logger.error("Error splitting the data")
            raise CustomException("Error splitting the data", e)
        
    def run(self):
        try:
            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Completed data ingestion successfully")

        except CustomException as ce:
            logger.error(f"Error in running data ingestion {str(ce)}")
        

# if __name__=="__main__":
#     d = DataIngestion(read_yaml(CONFIG_PATH))
#     d.run()