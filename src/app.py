from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
api = Api(app)


class RawFeats:
    def __init__(self, feats):
        self.feats = feats

    def fit(self, X, y=None):
        pass


    def transform(self, X, y=None):
        return X[self.feats]

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

filename = 'finalized_model.sav'
model = pickle.load(open(filename, 'rb'))

class Scoring(Resource):
    def post(self):
        json_data = request.get_json()
        df = pd.DataFrame(json_data.values(), index=json_data.keys()).transpose()
        df['Not_Graduate'] = np.where(df['Education'] == 'Graduate', 0, 1)
        df['SelfEmployed'] = np.where(df['Self_Employed'] == 'Yes', 1, 0)
        df['Is_Married'] = np.where(df['Married'] == 'Yes', 1, 0)
        df['Urban'] = np.where(df['Property_Area'] == 'Urban', 1, 0)
        df['Semiurban'] = np.where(df['Property_Area'] == 'Semiurban', 1, 0)
        df.loc[(df.Dependents == '3+'),'Dependents'] = 4
        df['LogLoanAmount'] = np.log(df['LoanAmount'].astype(float))
        df['TotalIncome'] = (df['ApplicantIncome'] + df['CoapplicantIncome']).astype(float)
        df['LogTotalIncome'] = np.log(df['TotalIncome'])
        # df.drop(columns=['TotalIncome', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_ID', 'Gender', 'Self_Employed', 'Education', 'Married', 'Property_Area'], inplace=True)
        res = model.predict_proba(df)
        return res.tolist()

api.add_resource(Scoring, '/scoring')
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)