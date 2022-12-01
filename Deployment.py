from flask import Flask,render_template,request,redirect
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
import numpy as np

app=Flask(__name__)
cors=CORS(app)
model=pickle.load(open('RegressionModel.pkl','rb'))
cars=pd.read_csv('carsEDA.csv')

@app.route('/',methods=['GET','POST'])
def index():
    companies=sorted(cars['Company'].unique())
    car_models=sorted(cars['Name'].unique())
    transmission=cars['Transmission'].unique()
    year=sorted(cars['Year'].unique(),reverse=True)
    fuel_type=cars['Fuel_Type'].unique()
    city = sorted(cars['City'].unique())

    companies.insert(0,'Select Company')
    return render_template('index.html',companies=companies, car_models=car_models, transmission=transmission, years=year,fuel_types=fuel_type, city=city)


@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():

    company=request.form.get('company')
    car_model=request.form.get('car_models')
    transmission = request.form.get('transmission')
    year=request.form.get('year')
    fuel_type=request.form.get('fuel_type')
    driven=request.form.get('kilo_driven')
    city = request.form.get('city')

    prediction=model.predict(pd.DataFrame(columns=['Name', 'Company', 'Transmission', 'Year', 'KM_Driven', 'Fuel_Type', 'City'],
                              data=np.array([car_model,company,transmission,year,driven,fuel_type,city]).reshape(1, 7)))
    print(prediction)

    return str(np.round(prediction[0],2))



if __name__=='__main__':
    app.run()