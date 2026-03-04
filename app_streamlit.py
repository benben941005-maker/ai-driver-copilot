
import streamlit as st
import pandas as pd
from api import load_deliveries, coordinator

st.set_page_config(layout="wide")
st.title("AI Senior Driver Copilot")

df=load_deliveries()

delivery=st.selectbox("Select delivery",df["delivery_id"])
row=df[df["delivery_id"]==delivery].iloc[0].to_dict()

question=st.text_input("Ask AI (or simulate voice)","How should I arrange parcels?")

if st.button("Ask Copilot"):
    result=coordinator(question,row,df)
    st.subheader("Parcel Advice")
    st.write(result["parcel"])
    st.subheader("Route Suggestion")
    st.write(result["route"])
    st.subheader("Failure Risk")
    st.write(round(result["risk"]*100,1),"%")
