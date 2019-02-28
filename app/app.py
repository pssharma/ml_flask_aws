from flask import Flask, request
from flask_restful import Api, Resource
import json,subprocess,logging
import pandas as pd
app = Flask(__name__)
api = Api(app)

logging.basicConfig(filename='app.log', format="%(asctime)s:%(filename)s:%(message)s")

class Predict(Resource):
    def post(self):
        postedData = request.get_json()
        logging.debug("postedData "+postedData)
        postJson = {
            "state": postedData["state"],
            "party" : postedData["party"],
            "district" : postedData["district"],
            "voteshare" : postedData["voteshare"],
            "state_district": postedData["state"]+"_"+str(postedData["district"])

        }
        
        
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
    app.run(host='0.0.0.0')    
