from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from config.paths_config import *
from utils.common_functions import read_yaml

if __name__=="__main__":

    d = DataIngestion(read_yaml(CONFIG_PATH))
    d.run()

    p = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    p.process()

    m = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    m.run()