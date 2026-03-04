
import pandas as pd, joblib, os, numpy as np

def load_deliveries():
    return pd.read_csv("data/deliveries.csv")

def load_model():
    if os.path.exists("models/failure_model.pkl"):
        return joblib.load("models/failure_model.pkl")
    return None

def parcel_advice():
    return "Place heavier parcels at bottom, smaller on top. Leave door clearance. Take POD photo."

def route_suggestion(df):
    ids=df["delivery_id"].tolist()
    return " → ".join(ids[:5])

def failure_risk(model,row):
    if model is None: return 0.3
    X=pd.DataFrame([{
        "building_type":row["building_type"],
        "time_of_day":"afternoon",
        "parcel_count":row["parcel_count"],
        "past_fail_rate":0.2,
        "customer_note_len":len(row.get("customer_note",""))
    }])
    return float(model.predict_proba(X)[0][1])

def coordinator(question,row,df):
    model=load_model()
    return {
        "parcel":parcel_advice(),
        "route":route_suggestion(df),
        "risk":failure_risk(model,row)
    }
