import streamlit as st
import requests 
import json

st.title("MTHC AI Receptionist")

query = st.text_input("Enter your query")
API = "http://127.0.0.1:8000/Agent"

if st.button("Submit") and query:
    def generate():
        with requests.post(
            API,
            json=query,
            stream=True,
            timeout=120
        ) as res:
            res.raise_for_status()

            for chunk in res.iter_content(
                chunk_size=None,
                decode_unicode=True
            ):
                if chunk:
                    yield chunk.decode("utf-8") if isinstance(chunk, bytes) else chunk

    st.write_stream(generate())

    
