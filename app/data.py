import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import argparse,json,sys,logging
import tensorflow as tf
import ast

import os

logging.basicConfig(filename='app.log', format="%(asctime)s:%(filename)s:%(message)s")
FLAGS = None
MAIN_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(MAIN_PATH, "data")
retJson = {}
cat_attributes = ["party","state_district","state"]
class MultiColumnLabelEncoder:
    def __init__(self,columns = None):
        self.columns = columns

    def fit(self,X,y=None):
        return self  

    def transform(self,X):
        output = X.copy()
        for col in self.columns:
            output[col] = LabelEncoder().fit_transform(output[col].astype(str))
        return output
    
    def fit_transform(self, X,y=None):
        return self.fit(X,y).transform(X)


def loading_data(data_path=DATA_PATH):
    file_path = os.path.join(data_path,"house_district_forecast.csv")
    df = pd.read_csv(file_path)
    return df


# creating a test set with 20% of data 
def split_traintest(data):
    return train_test_split(data, test_size = 0.2, random_state=42)

# while taking a test set we must make sure it is "stratified sampling" by creating a category of voteshare
def stratified_split(data):
    data["state_district"] = data["state"].map(str)+"_"+data["district"].map(str)
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.33,random_state=42)
    #data["voteshare_cat"] = np.ceil(data["voteshare"].astype(float)/10)
    for train_index, test_index in split.split(data,data["party"].astype(str)):
        strat_train_set = data.loc[train_index]
        strat_test_set = data.loc[test_index]
    #for set in (strat_train_set,strat_test_set):
        #set.drop(["voteshare_cat"], axis=1, inplace=True)    
    return strat_train_set, strat_test_set    




def get_labels_predictors(train_data):
    predictors = train_data.drop(["win_probability","forecastdate","special","candidate","incumbent","model","p10_voteshare","p90_voteshare"],axis=1)
    labels = train_data["win_probability"].copy()
    return MultiColumnLabelEncoder(cat_attributes).fit_transform(predictors),labels
           

def fit_model(predictors_prepared,labels):
    rfRegg = RandomForestRegressor()
    rfRegg.fit(predictors_prepared,labels)
    predictions = rfRegg.predict(predictors_prepared)
    rfRegMse = mean_squared_error(labels,predictions)
    rfRegRmse = np.sqrt(rfRegMse)
    logging.debug("rmse "+str(rfRegRmse))
    return rfRegg

def main(_):
    train_set,test_set = stratified_split(loading_data())
    predictors,labels =get_labels_predictors(train_set)
    f_model = fit_model(predictors,labels)
    json_string = FLAGS.predict_params
    logging.debug(json_string)
    #we get the json string and convert it into pandas data frame
    df_predict = pd.DataFrame(json.loads(json_string),index=[0])
    df_prepared = MultiColumnLabelEncoder(cat_attributes).fit_transform(df_predict)
    df_predict = f_model.predict(df_prepared)
    retJson["win_prob"] = df_predict[0]
    logging.debug(str(retJson["win_prob"]))
    #write this json onto a text file
    with open("text.txt","w") as f:
        json.dump(retJson, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--predict_params',
        type=str,
        default='',
        help="""
        Path to predict the winning probability percentage depending
        on state, district, votershare and party 
        """
    ) 
    FLAGS, unparsed = parser.parse_known_args()
tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)    




    







