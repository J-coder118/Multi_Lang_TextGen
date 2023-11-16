import csv
import os
from supabase.client import Client, create_client
import openai
import httpx
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
openai_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_key 

function_name = "match_documents"

supabase = Client(supabase_url, supabase_key)


st.title("chat")
st.caption("Please ask what you want.")

question = st.text_input("Question")

if st.button("Get Answer"):
    response = openai.Embedding.create(model="text-embedding-ada-002", input=question)
    data = response["data"]

    embedding_query = [embedding for embedding in data]

    print("LOADING...")

    print("sfddsfds")
    similarity_threshold = 0.79
    match_count = 10
    model_engine = "gpt-4"
    payload = {
        "query_embedding": embedding_query[0]["embedding"],
        "match_count": match_count,
        "match_threshold": 0.8,
    }

    response = supabase.rpc(function_name, payload).execute()

    data = response.data
    response_data_0 = data[0]["description"]
    response_data_1 = data[1]["description"]
    response_data_2 = data[2]["description"]
    response_data_3 = data[3]["description"]
    response_data_4 = data[4]["description"]
    response_data_5 = data[5]["description"]
    response_data_6 = data[6]["description"]
    response_data_7 = data[7]["description"]
    response_data_8 = data[8]["description"]
    response_data_9 = data[9]["description"]

    prompt = [
        {
            "role": "system",
            "content": "You are an AI assistant that provides helpful answers.",
        },
        {
            "role": "user",
            "content": f"""
        Just rewrite this content in Russian
        {response_data_0+
         response_data_1+
         response_data_2+
         response_data_3+
         response_data_4+
         response_data_5+
         response_data_6+
         response_data_7+
         response_data_8+
         response_data_9
         }
        """,
        },
    ]

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.8,
    )

    ai_response = response.choices[0].message["content"]

    st.write("AI Answer:", ai_response)

    if isinstance(response_data_0, list) and len(response_data_0) > 0:
        first_result = response_data_0[0]
        description = first_result.get("description")
        if description:
            print(description)
        else:
            print("Description not found in the response.")
    else:
        print("No response data or empty response.")
