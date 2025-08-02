import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
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
            logger.inof("Removed duplicates")

        except Exception as e:
            logger.error("Error preprocessing the data")
            raise CustomException("Error preprocessing the data", e)
