# ml_flask_aws
This project consists of Machine learning algorithm implemented in scikit learn to predict the winning probability of congressional elections.

The dataset is obtained from fivethirtyeight (https://github.com/fivethirtyeight/data/tree/master/house-forecast-2018)

## Tech stack 
Python Scikit learn ---> model implemetaion
Flask ---> server side RESTful engine
Docker 
AWS lambda for deployment

Check readme.ipynb jupyter notebook for data exploration process.

## Project Structure
  
      .
    ├── ...
    ├── app                     
    │   ├── app.py        #flask restful implementation
    │   ├── data.py       #logic for ml algorithm
    │   ├── readme.ipynb  #data exploration process
    │   ├── data          #data files
    │   
    └── README.md
    │   
    └── docker.yml
  
