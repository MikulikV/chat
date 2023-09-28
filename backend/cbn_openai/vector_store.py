import openai
import pinecone
import os
from dotenv import load_dotenv
from config import EMBED_MODEL, INDEX_NAME

load_dotenv()
openai.api_key= os.environ["OPENAI_API_KEY"]
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"], 
    environment=os.environ["PINECONE_ENV"], 
)


def get_context(user_input):
    """Get relevant contexts"""
    embedding = openai.Embedding.create(
        input=[user_input],
        engine=EMBED_MODEL
    )
    index = pinecone.Index(INDEX_NAME)
    embedded_question = embedding['data'][0]['embedding']
    retrieved_data = index.query(vector=embedded_question, top_k=4, include_metadata=True)
    contexts = [item['metadata']['text'] for item in retrieved_data['matches']]
    augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n" + user_input

    return augmented_query