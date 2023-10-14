from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
import sys
sys.path.append("backend/")
from config import PINECONE_API_KEY, PINECONE_ENV, EMBED_MODEL, INDEX_NAME
from utils.load_data import load_data


if __name__ == "__main__":
    # load OPENAI_API_KEY
    chunks = []
    source_dir = ["backend/data/cbn_knowledge_base/brands/"]
    for sd in source_dir:
        chunks.extend(load_data(sd))

    # embed text and store embeddings
    embedding = OpenAIEmbeddings(model=EMBED_MODEL)

    # initialize pinecone
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV, 
    )

    # First, check if our index already exists. If it doesn't, we create it
    if INDEX_NAME not in pinecone.list_indexes():
        # create a new index
        pinecone.create_index(
            name=INDEX_NAME,
            metric='cosine',
            dimension=1536,  
        )
        # load chunks into vector store
        vector_store = Pinecone.from_documents(
            documents=chunks,
            embedding=embedding,
            index_name=INDEX_NAME,
        )
    else:
        index = pinecone.Index(INDEX_NAME)
        vectorstore = Pinecone(
            index, embedding, "text"
        )
        # add new documents into vector store
        vectorstore.add_documents(chunks)


    


