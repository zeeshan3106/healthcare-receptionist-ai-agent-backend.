import streamlit as st
import requests 
import json

st.title("MTHC AI Receptionist")
input = st.text_input("Enter the query")
API = "http://127.0.0.1:8000/Agent"
if st.button("Submit"):
    res = requests.post(API, input)
    final = res.json()
    st.write(final['res'])
    

    
