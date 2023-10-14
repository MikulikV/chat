import openai
import pinecone
import sys
sys.path.append("backend/")
from config import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_ENV, EMBED_MODEL, INDEX_NAME


openai.api_key= OPENAI_API_KEY
pinecone.init(
    api_key=PINECONE_API_KEY, 
    environment=PINECONE_ENV, 
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
    contexts = [item['metadata']['text'] for item in retrieved_data['matches'] if item['score'] > 0.8] # get contexts with similarity score > 0.8
    augmented_query = "\n\n----\n\n".join(contexts)+"\n\n-----\n\n" + user_input

    return augmented_query