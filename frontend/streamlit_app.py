import streamlit as st
import requests

API_Base = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="EngBrain",
    layout="wide"
)

st.title("EngBrain")
st.write("AI engineering memory and runbook generator for codebases.")

st.header("1. Ingest Repository")

repo_path = st.text_input(
    "Local Repo path",
    value=r"C:\Users\gusai\OneDrive\Desktop\MVP"
)

if st.button("Ingest Repo"):
    try:
        reponse = requests.post(
            f"{API_Base}/repos/ingest",
            json = {"repo_path":repo_path}
        )
        if reponse.status_code == 200:
            st.success("Repo Successfully Ingested")
            st.json(reponse.json())
        else:
            st.error("Error in Ingesting")
            st.text(reponse.text)
    except Exception as e:
        st.error(f"could not connect to backend: {e}")
    