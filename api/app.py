from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import sys
import pandas as pd
from src.exception import CustomException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: str
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

@app.post('/predict')
def predict(customer: CustomerData):
    try:
        # loading the preprocessors
        with open('artifacts/preprocessor.pkl', 'rb') as f:
            preprocessor = pickle.load(f)

        # loading the model
        with open('artifacts/models/model.pkl', 'rb') as f:
            model = pickle.load(f)

        customer_dict = customer.dict()
        customer_dict['SeniorCitizen'] = 1 if customer_dict['SeniorCitizen'].lower() == 'yes' else 0

        df = pd.DataFrame([customer_dict])
        processed_df = preprocessor.transform(df)
        prediction = model.predict(processed_df)[0]
        probability = model.predict_proba(processed_df)[0][1]

        return {
            'prediction': int(prediction),
            'probability': float(probability)
        }

    except Exception as e:
        raise CustomException(e, sys)