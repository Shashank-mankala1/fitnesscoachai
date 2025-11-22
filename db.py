from astrapy import DataAPIClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

ENDPOINT = os.getenv("ASTRA_DB_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")


@st.cache_resource
def get_db_client():
    client = DataAPIClient(TOKEN)
    db=client.get_database_by_api_endpoint(ENDPOINT)
    return db


db_client = get_db_client()
profiles_collection = ["fitness_coach_ai", "notes"]

for collection in profiles_collection:
    try:
        db_client.get_collection(collection)
    except Exception:
        pass

personal_profiles_collection = db_client.get_collection("fitness_coach_ai")
notes_collection = db_client.get_collection("notes")
