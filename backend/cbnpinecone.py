import openai
import pinecone
import os
from dotenv import load_dotenv 

load_dotenv()
openai.api_key= os.getenv("OPENAI_API_KEY")
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), 
    environment=os.getenv("PINECONE_ENV"), 
)
embed_model = "text-embedding-ada-002"
index_name = "cbn-demo"
user_input = "Who is Gizmo?"

# get relevant contexts
embedding = openai.Embedding.create(
    input=[user_input],
    engine=embed_model
)
index = pinecone.Index(index_name)
embedded_question = embedding['data'][0]['embedding']
retrieved_data = index.query(vector=embedded_question, top_k=4, include_metadata=True)
contexts = [item['metadata']['text'] for item in retrieved_data['matches']]
augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n" + user_input