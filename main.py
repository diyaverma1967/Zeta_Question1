from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

model = joblib.load("dispute_model.pkl")

app = FastAPI(title="Dispute Risk API", version="1.0")
class DisputeInput(BaseModel):
    transaction_amount: float
    customer_age: int
    customer_tenure: int
    account_type: str
    dispute_reason: str
    channel: str
    customer_flagged: int
    previous_disputes: int
    dispute_time: str

def assign_priority(input_data, risk_prediction):
    if risk_prediction == 1:
        return "High", "Investigate"
    elif input_data.customer_flagged == 1 or input_data.previous_disputes > 2:
        return "Medium", "Manual Review"
    else:
        return "Low", "Auto-resolve"

@app.get("/")
def root():
    return {"message": "Dispute Risk Classification API is running."}

@app.post("/predict/")
def predict_risk(dispute: DisputeInput):
    try:
        input_df = {
            "transaction_amount": [dispute.transaction_amount],
            "customer_age": [dispute.customer_age],
            "customer_tenure": [dispute.customer_tenure],
            "account_type": [dispute.account_type],
            "dispute_reason": [dispute.dispute_reason],
            "channel": [dispute.channel],
            "customer_flagged": [dispute.customer_flagged],
            "previous_disputes": [dispute.previous_disputes],
            "dispute_time": [dispute.dispute_time],
        }

        prediction = model.predict(pd.DataFrame(input_df))[0]
        priority, recommendation = assign_priority(dispute, prediction)

        return {
            "risk": "High" if prediction == 1 else "Low",
            "priority": priority,
            "recommended_action": recommendation,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

