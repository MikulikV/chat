from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import BSHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.clean_data import clean_text
from utils.tokenizer import tiktoken_len

# define text_splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", "(?<=\.)", "(?<=\!)", "(?<=\?)", "(?<=\,)", " ", ""],
    length_function=tiktoken_len, 
    add_start_index=True,
)

def load_data(source_dir):
    loader = DirectoryLoader(source_dir, glob="**/*.html", loader_cls=BSHTMLLoader, show_progress=True)
    documents = loader.load()
    # clean and split loaded files
    docs = clean_text(documents)
    # split documents by chunks
    chunks = text_splitter.split_documents(docs)
    result_chunks = [doc for doc in chunks if tiktoken_len(doc.page_content) >= 100] # chunks more than chunk_overlap

    return result_chunks


    