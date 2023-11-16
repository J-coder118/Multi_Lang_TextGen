import openai
import os
from pythonsupabase import create_client
from textwrap import dedent
from transformers import GPT3Tokenizer

supabase_url = "https://your-project.supabase.co"
supabase_key = "your-service-role-key"
openai_key = "your-openai-api-key"

client = create_client(supabase_url, supabase_key)

query = "your query here"
input = query.replace('\n', ' ')

configuration = openai.Configuration()
configuration.api_key = ""
openai.api_key = configuration.api_key

embedding_response = openai.Embedding.create(
    model='text-embedding-ada-002',
    input=input
)
embedding = embedding_response['data'][0]['embedding']

documents = client.rpc('match_documents', {
    'query_embedding': embedding,
    'match_threshold': 0.78,
    'match_count': 10
})['data']

tokenizer = GPT3Tokenizer.from_pretrained('gpt4')
token_count = 0
context_text = ''

for document in documents:
    content = document['content']
    encoded = tokenizer.encode(content)
    token_count += len(encoded)
    if token_count > 1500:
        break
    context_text += f"{content.strip()}\n---\n"

prompt = dedent(f"""
    You are a very enthusiastic Supabase representative who loves
    to help people! Given the following sections from the Supabase
    documentation, answer the question using only that information,
    outputted in markdown format. If you are unsure and the answer
    is not explicitly written in the documentation, say
    "Sorry, I don't know how to help with that."

    Context sections:
    {context_text}

    Question: """
    {query}
    """

    Answer as markdown (including related code snippets if available):
""")

completion_response = openai.Completion.create(
    model='text-davinci-003',
    prompt=prompt,
    max_tokens=512,
    temperature=0
)

id = completion_response['id']
text = completion_response['choices'][0]['text']

client.table('my_table').insert({'id': id, 'text': text})
