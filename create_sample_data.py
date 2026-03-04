
import os
import numpy as np
import pandas as pd

np.random.seed(123)

def ensure_dirs():
    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("knowledge", exist_ok=True)

def make_deliveries(n=200):
    building_types = ["HDB","Condo","Landed","Office","Mall"]
    time_windows = ["9-12","12-3","3-6","6-9"]
    notes = [
        "Please arrange parcels nicely beside the door.",
        "Call me when you arrive.",
        "Leave at guardhouse if not home.",
        "Do not ring bell, baby sleeping.",
        "Security requires registration.",
        ""
    ]
    df = pd.DataFrame({
        "delivery_id":[f"D{100000+i}" for i in range(n)],
        "lat":1.28+np.random.normal(0,0.02,n),
        "lon":103.85+np.random.normal(0,0.03,n),
        "time_window":np.random.choice(time_windows,n),
        "parcel_count":np.random.randint(1,6,n),
        "building_type":np.random.choice(building_types,n),
        "customer_note":np.random.choice(notes,n)
    })
    return df

def make_history(n=500):
    building_types=["HDB","Condo","Landed","Office","Mall"]
    time_of_day=["morning","afternoon","evening"]
    df=pd.DataFrame({
        "building_type":np.random.choice(building_types,n),
        "time_of_day":np.random.choice(time_of_day,n),
        "parcel_count":np.random.randint(1,6,n),
        "past_fail_rate":np.random.uniform(0,0.6,n)
    })
    df["customer_note_len"]=np.random.randint(0,40,n)
    p=0.1+0.2*(df["building_type"]=="Condo")+0.3*df["past_fail_rate"]
    failure=np.random.binomial(1,p.clip(0,0.9))
    df["success"]=1-failure
    return df

def write_kb():
    docs={
"parcel_arrangement_rules.txt":"Put heavy parcels at bottom. Keep door clear. Take clear POD photo.",
"proof_of_delivery_rules.txt":"Take wide photo showing door and parcels. Ensure lighting is clear.",
"condo_access_rules.txt":"Register at guardhouse. Call customer if access denied.",
"common_fail_reasons.txt":"Recipient not home, wrong address, security restriction."
}
    for k,v in docs.items():
        with open(f"knowledge/{k}","w") as f: f.write(v)

if __name__=="__main__":
    ensure_dirs()
    make_deliveries().to_csv("data/deliveries.csv",index=False)
    make_history().to_csv("data/history.csv",index=False)
    write_kb()
    print("Sample data created")
