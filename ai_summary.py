from openai import OpenAI
import streamlit as st

# ----- Establish AI Client ----- #

# Cache allows the data to be stored, meaning the program will run faster
@st.cache_resource
def get_openai_client():
    api_key = st.secrets["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


# ----- Get AI Reponses ----- #

def ai_descriptions(prompt):
    client = get_openai_client()
    response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
    return response.output[0].content[0].text

