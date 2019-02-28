
# ml_flask_aws
This project consists of Machine learning algorithm implemented in scikit learn to predict the winning probability of congressional elections.

The dataset is obtained from [fivethirtyeight](https://github.com/fivethirtyeight/data/tree/master/house-forecast-2018)

## Tech stack 
>Python Scikit learn ---> model implemetaion
>Flask ---> server side RESTful engine
>Docker 
>AWS lambda for deployment

>Check readme.ipynb jupyter notebook for data exploration process.
## Project Structure
    ├──app
    │
    │   ├── data.py       #logic for ml algorithm
    │   ├── readme.ipynb  #data exploration process
    │   ├── data          #data files
    │   ├── text.txt      #where the result is stored as json  
    │   
    ├── README.md
    │   
    └── docker.yml

## Project workflow

> A REST request to the app with parameters state, district, party and voteshare will determine the win probability of the candidate.
> for request json
```
{
"state":"AL",
"district": 2,
"party": "D",
"voteshare": 58
}
```
>response json would be
```
{
"win_probability":0.98765
}
```
> example result is stored in text.txt
>parameter lists to choose from
```
party: [D,R,LIB,IND,GRE,I,G,REF,L,CON,AME,US Taxpayers,NPA,Working Class,WOF,Independence Party,Reform Party,IPO,Mountain,DPD,Legal Marijuana Now,Women's Equality Party]
state: follow conevtion from [here](https://en.wikipedia.org/wiki/List_of_United_States_congressional_districts)
voteshare: can be any decimal between 0 to 100
```


