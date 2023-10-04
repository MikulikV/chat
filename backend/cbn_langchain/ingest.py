from langchain.document_loaders import WebBaseLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
import re
import tiktoken
import os
from dotenv import load_dotenv 
from config import EMBED_MODEL, INDEX_NAME

# functions to prepare the data
def fix_newlines(text):
    return re.sub(r"(?<!\n)\n(?!\n)", " ", text)


def fix_tabs(text):
    return re.sub(r"(?<!\t)\t(?!\t)", " ", re.sub(r"\t{2,}", " \t ", text))


def remove_multiple_newlines(text):
    return re.sub(r"\n{2,}", " \n ", text)


def remove_multiple_spaces(text):
    return re.sub(r" +", " ", text)


def remove_time_codes(text):
    return re.sub(r"\d{2}:\d{2}:\d{2}", "", text)


def remove_stars_from_text(text):
    return text.replace("*", "")


def clean_text(data, cleaning_functions):
    if isinstance(data, str):
        for cleaning_function in cleaning_functions:
            data = cleaning_function(data)
        prepared_data = data
    elif isinstance(data, list):
        prepared_data = []
        for document in data:
            for cleaning_function in cleaning_functions:
                document.page_content = cleaning_function(document.page_content)
            doc = Document(
                page_content=document.page_content,
                metadata=document.metadata
            )
            prepared_data.append(doc)
    
    return prepared_data

# function to count the tokens and text splitter
tokenizer = tiktoken.get_encoding("cl100k_base")
def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", "(?<=\.)", "(?<=\!)", "(?<=\?)", "(?<=\,)", " ", ""],
    length_function=tiktoken_len, 
    add_start_index = True,
)


if __name__ == "__main__":
    # load OPENAI_API_KEY
    load_dotenv()

    cleaning_functions = [
        fix_tabs,
        remove_time_codes,
        remove_stars_from_text,
        fix_newlines,
        remove_multiple_newlines,
        remove_multiple_spaces,
    ]

    documents = []
    # load CBN Faith section and SuperBook FAQ
    web_loader = WebBaseLoader([
        "https://www2.cbn.com/lp/faith-homepage", 
        "https://www2.cbn.com/faith/devotionals",
        "https://www2.cbn.com/devotions/god-will-help-you-triumph-over-despair",
        "https://www2.cbn.com/faith/who-is-jesus",
        "https://www2.cbn.com/faith/new-christians",
        "https://www2.cbn.com/lp/faith-coming-back-your-faith",
        "https://www2.cbn.com/lp/faith-grow-deeper-your-faith",
        "https://www2.cbn.com/lp/faith-share-your-faith",
        "https://www2.cbn.com/devotions/trust-god",
        "https://www2.cbn.com/article/bible-says/bible-verses-about-prayer-praying",
        "https://www2.cbn.com/resources/ebook/perfect-timing-discover-key-answered-prayer",
        "https://www2.cbn.com/article/purpose/seven-keys-hearing-gods-voice",
        # FAQ SuperBook
        "https://cbn.com/superbook/faq-episodes.aspx", 
        "https://us-en.superbook.cbn.com/faq"
        "https://us-en.superbook.cbn.com/congratulations",
        "https://appscdn.superbook.cbn.com/api/bible/app_profiles.json/?lang=en&f=all&id=0&sort=null&r=100000&vid=13653741"
        "https://appscdn.superbook.cbn.com/api/bible/app_games.json/?lang=en&f=trivia&id=0&sort=null&r=100000&vid=13653741&result_version=2",
        "https://appscdn.superbook.cbn.com/api/bible/app_gospel/?lang=en&vid=13653741",
        "https://appscdn.superbook.cbn.com/api/bible/app_multimedia.json/?lang=en&f=all&id=0&sort=null&r=100000&vid=13653741"
    ])
    documents.extend(web_loader.load())
    # clean and split loaded files
    docs = clean_text(documents, cleaning_functions)
    chunks = text_splitter.split_documents(docs)
    result_chunks = [doc for doc in chunks if tiktoken_len(doc.page_content) >= 100] # chunks more than chunk_overlap

    # embed text and store embeddings
    embedding = OpenAIEmbeddings(model=EMBED_MODEL)

    # initialize pinecone
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"), 
        environment=os.getenv("PINECONE_ENV"), 
    )

    # First, check if our index already exists. If it doesn't, we create it
    if INDEX_NAME not in pinecone.list_indexes():
        # we create a new index
        pinecone.create_index(
        name=INDEX_NAME,
        metric='cosine',
        dimension=1536,  
    )

    vector_store = Pinecone.from_documents(
        documents=result_chunks,
        embedding=embedding,
        index_name=INDEX_NAME,
    )


