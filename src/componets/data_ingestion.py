import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.componets.data_transformation import DataTransformation,DataTransformationConfig
from src.componets.model_trainer import ModelTrainer,ModelTrainerConfig
@dataclass
class DataIngestionConfig:
    train_data_path=os.path.join('artifacts','train.csv')
    test_data_path=os.path.join('artifacts','test.csv')
    raw_data_path=os.path.join('artifacts','data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
        #self.logger=logging.get_logger()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv('notebook/data/stud.csv')
            logging.info('Exported or Read the dataset as dataframe')
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info("Train test split initiated")
            train_teset,test_test=train_test_split(df,test_size=0.2,random_state=42)
            train_teset.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_test.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info("Ingestion of the data is  completed")
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
            



if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)
    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))