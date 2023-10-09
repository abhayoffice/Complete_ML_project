import os
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self, config):
        self.data_transformation_config = config
        
    def get_data_transformer_object(self):
        try:
            num_pipeline = Pipeline(
                steps=[
                    ("Invoice Amount", SimpleImputer(strategy="median")),
                ]
            )

            preprocessor = ColumnTransformer([
                ("num_pipeline", num_pipeline, ['Invoice Amount'])
            ])
            return preprocessor

        except Exception as e:
            raise CustomException(e)

    def initiate_data_transformation(self, train_data, test_data):
        try:
            train_df = pd.read_csv(train_data)
            test_df = pd.read_csv(test_data)

            logging.info("Read train and test data completed")

            preprocessor = self.get_data_transformer_object()

            input_feature_train_arr = preprocessor.fit_transform(train_df[['Invoice Amount']])
            input_feature_test_arr = preprocessor.transform(test_df[['Invoice Amount']])

            train_df_transformed = pd.DataFrame(input_feature_train_arr, columns=['Invoice Amount'])
            test_df_transformed = pd.DataFrame(input_feature_test_arr, columns=['Invoice Amount'])

            train_df_transformed['Invoice Date'] = train_df['Invoice Date']
            test_df_transformed['Invoice Date'] = test_df['Invoice Date']

            train_df_transformed['Invoice Date'] = pd.to_datetime(train_df_transformed['Invoice Date'])
            test_df_transformed['Invoice Date'] = pd.to_datetime(test_df_transformed['Invoice Date'])

            train_df_transformed.set_index('Invoice Date', inplace=True)
            test_df_transformed.set_index('Invoice Date', inplace=True)

            train_df_transformed = self.replace_zero_with_mean(train_df_transformed)
            test_df_transformed = self.replace_zero_with_mean(test_df_transformed)

            if train_df_transformed.shape[0] + test_df_transformed.shape[0] <= 36:
                self.skip_file()

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path, obj=preprocessor
            )
            return train_df_transformed, test_df_transformed

        except Exception as e:
            raise CustomException(e)

    def skip_file(self):
        print("Skip this file and use os.write() here")

    def replace_zero_with_mean(self, df):
        median_value = df[df['Invoice Amount'] != 0.0]['Invoice Amount'].mean()
        df.loc[df['Invoice Amount'] == 0.0, 'Invoice Amount'] = median_value
        return df