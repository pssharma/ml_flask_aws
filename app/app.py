from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests,json,subprocess
import pandas as pd
app = Flask(__name__)
api = Api(app)


class Predict(Resource):
    def post(self):
        postedData = request.get_json()

        postJson = {
            "state": postedData["state"],
            "party" : postedData["party"],
            "district" : postedData["district"],
            "voteshare" : postedData["voteshare"],
            "state_district": postedData["state"]+"_"+str(postedData["district"])

        }
      

        stringPosted = json.dumps(jsonify(postJson))
        
        proc = subprocess.Popen('python data.py --predict_params='+stringPosted)
        proc.communicate()[0]
        proc.wait()
        with open("text.txt") as g:
            retJson = json.load(g)

        return retJson    

api.add_resource(Predict,'/predict')


if __name__ == "__main__":
    app.run(host='0.0.0.0')    
