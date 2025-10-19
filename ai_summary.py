from openai import OpenAI
import streamlit as st

# This file has the functions to connect with the openAI api in a safe manner.
# If the api cannot be accessed, the code will not completely break.


# ----- Establish AI Client ----- #

# The API client is returned. This function is not inherently safe, as it could return an error.
# Due to this, the function below wraps it in a try block.
@st.cache_resource
def get_openai_client():
    api_key = st.secrets["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


# ----- Get AI Reponses ----- #

# There are precautions in place to prevent lookups with broken / incorrect api keys and out of range years
def ai_descriptions(prompt, year):
    if year != 'career': # must be valid year
        if int(year) >= 2025:
            return "Cannot generate player info:  GPT-4.1-mini is only trained on data up until the end of the 2024 season."
    
    try:
        client = get_openai_client()
    except:
        return "Could not generate player description. OpenAI API key was not provided correctly!"
    
    try:
        response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )
        return response.output[0].content[0].text
    except:
        return "Player description could not be generated with OpenAI API. Please check that API key has been entered correctly!"


