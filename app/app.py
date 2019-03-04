from flask import Flask, request
from logging.handlers import RotatingFileHandler
from flask_restful import Api, Resource
import json,subprocess,logging,traceback
import pandas as pd


app = Flask(__name__)
api = Api(app)

#logging.basicConfig(filename='app.log', format="%(asctime)s:%(filename)s:%(message)s")
STATES_LIST = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI',
       'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI',
       'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV',
       'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
       'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

PARTY_LIST = ['R', 'D', 'LIB', 'G', 'I', 'GRE', 'NPA', 'IND',
       'US Taxpayers', 'Working Class', 'Legal Marijuana Now',
       'Independence Party', 'REF', 'CON', 'Reform Party', 'WOF', 'IPO',
       'L', 'AME', 'DPD', 'Mountain', "Women's Equality Party"]

class Predict(Resource):
    def post(self):
        postedData = request.get_json()
        retJson = {}
        postJson = {}

        logger.debug(postedData)
        
        if all (k in postedData for k in ('state','party','district','voteshare')):
            state = postedData["state"]
            party = postedData["party"]
            district = postedData["district"]
            voteshare = postedData["voteshare"]
            if state not in STATES_LIST:
                retJson["message"] = "Syntax of state is Wrong or No Data for this state now."
                return retJson
            elif party not in PARTY_LIST:
                retJson["message"] = "Choose from party list in the documentation."
                return retJson
            elif int(voteshare) < 0 or int(voteshare) > 100:
                retJson["message"] = "Voteshare is the percentage value. So it should stay between 0 to 100."
                return retJson
            elif int(district) > 32:
                retJson["message"] = "Check your district"
                return retJson
            else:
                postJson = {
                "state": state,
                "party" : party,
                "district" : district,
                "voteshare" : voteshare,
                "state_district": state+"_"+str(district)}

        else:
            retJson["message"] = "All 4 of the attributes 'state', 'party', 'district', 'voteshare' has to be populated"
        
        
        
        stringPosted = json.dumps(postJson)
    
        proc = subprocess.Popen(['python', 'data.py', '--predict_params='+stringPosted])
        proc.communicate()[0]
        proc.wait()
        retJson = {}
        with open("text.txt") as g:
            retJson = json.load(g)
        
        return retJson





api.add_resource(Predict,'/predict')


if __name__ == "__main__":
    handler = RotatingFileHandler('app.log', maxBytes = 10000 , backupCount=3)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    app.run(host='0.0.0.0',debug=True)
        
