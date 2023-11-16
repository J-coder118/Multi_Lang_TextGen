from langchain.vectorstores.supabase import SupabaseVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from supabase import create_client, Client
import os
import re
import streamlit as st

import csv
import os
from supabase.client import Client, create_client
import openai
import httpx
import requests
import ssl
import time

from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
openai_key = os.getenv("OPENAI_API_KEY")


# Create a Supabase client with the configured session
supabase = Client(supabase_url, supabase_key)

openai.api_key = openai_key  # os.environ["SECRET_KEY"]




with open("ui/styles.md", "r") as styles_file:
    styles_content = styles_file.read()


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

with open("total_data.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    i = 0
    for row in reader:
        try:
            title = row[0].replace("\n", " ")
            description = row[1]
            categories = row[2].replace("\n", " ")
            tags = row[3].replace("\n", " ")
            i = 1 + i
            print("raw data", i)
            retries = 0
            embedding_value = None
            max_retries = 100
            delay_seconds = 30
            while retries < max_retries and embedding_value is None:
                try:
                    response = openai.Embedding.create(
                        model="text-embedding-ada-002", input=description
                    )
                    data = response["data"]
                    embedding_value = [embedding for embedding in data]
                except Exception as e:
                    print(f"Error occurred: {e}")
                    retries += 1
                    if retries < max_retries:
                        print(f"Retrying in {delay_seconds} seconds...")
                        time.sleep(delay_seconds)
                    else:
                        print("Maximum number of retries reached.")
            if embedding_value is not None:
                value = {
                    "title": title,
                    "tag": tags,
                    "categories": categories,
                    "description": description,
                    "embedding": embedding_value[0]["embedding"],
                }

                result = supabase.table("documents").insert(value).execute()
        except ssl.SSLError as err:
            print("error", err)
        # print("results--->", result)

        # client.table('documents').insert({'title': title, 'description': description, 'categories': categories, 'tag': tags, 'embedding': embedding_desc})
