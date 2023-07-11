import sys
import numpy as np
from dataclasses import dataclass
import pandas as pd
from sklearn.compose import ColumnTransformer  #it is use to create pipline
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import  save_object 
import os

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join ("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config= DataTransformationConfig()
    
    def get_data_transformation_object(self):
        try:
            numerical_column = ["reading_score","writing_score"]
            categorical_column = ["gender","race_ethnicity",
                                  "parental_level_of_education",
                                  "lunch","test_preparation_course"]
            
            num_pipeline= Pipeline(
              
                steps=
                [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())

                ]
            )

            cat_pipeline = Pipeline(
                steps= [
                    ("imputer", SimpleImputer(strategy = "most_frequent")),
                    ("one_hot_encode", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Categorical columns : {categorical_column}")
            logging.info(f"Numerical columns are : {numerical_column}")

            preprocessor =  ColumnTransformer(
                [
                    ("num_pipeline_agg", num_pipeline, numerical_column),
                    ("cat_pipeline_agg", cat_pipeline, categorical_column)
                ]
            )

            logging.info("Logging Initiated")
            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            logging.info("Train and test data has been read")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = "math_score"

            input_feature_train_df=train_data.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_data[target_column_name]

            input_feature_test_df=test_data.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_data[target_column_name]
            
            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            preprocessing_train_data = preprocessing_obj.fit_transform(input_feature_train_df)
            preprocessing_test_data = preprocessing_obj.transform(input_feature_test_df)

            #concatinating preprocessed array allong with target varibale as an array using np.c_

            train_arr = np.c_[
                preprocessing_train_data, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                preprocessing_test_data, np.array(target_feature_test_df)
                ]

            logging.info(f"Saved preprocessing object.")


            save_object (
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )


        except Exception as e:
            raise CustomException(e, sys)

            



