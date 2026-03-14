from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

class PredictRequest(BaseModel):
    crop: str
    location: str

class PredictResponse(BaseModel):
    probability: float
    risk: str
    action: str
    ipm_stage: str
    cost: int
    moa: str
    reason: str

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):

    # TEMP MOCK (we will replace with real model after)
    prob = round(random.uniform(0.1, 0.9), 2)

    if prob < 0.3:
        risk = "LOW"
        action = "No intervention required"
        ipm_stage = "Preventive"
        cost = 0
        moa = "-"
        reason = "Low pest pressure"
    elif prob < 0.6:
        risk = "MEDIUM"
        action = "Neem-based biopesticide + traps"
        ipm_stage = "Biological control"
        cost = 300
        moa = "3A"
        reason = "Moderate pest presence"
    else:
        risk = "HIGH"
        action = "Selective chemical insecticide"
        ipm_stage = "Chemical control"
        cost = 800
        moa = "4A"
        reason = "Economic threshold crossed"

    return {
        "probability": prob,
        "risk": risk,
        "action": action,
        "ipm_stage": ipm_stage,
        "cost": cost,
        "moa": moa,
        "reason": reason
    }
