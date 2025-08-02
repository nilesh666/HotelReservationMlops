import os 
import pandas as pd
import sys
import yaml
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Yaml File does not exist")
        
        with open(file_path, "r") as f:
            config = yaml.safe_load(f)
            logger.info("Successfully read the yaml file")
            return config

    
    except Exception as e:
        logger.error("Error occured in reading yaml file")
        raise CustomException("Error in reading yaml", e)
    
def load_data(path):
    try:
        logger.info("Loading the data")
        return pd.read_csv(path)
    
    except Exception as e:
        logger.error("Error occured in reading yaml file")
        raise CustomException("Error in reading yaml", e)
