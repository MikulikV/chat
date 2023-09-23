from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores.chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationTokenBufferMemory
import os
from dotenv import load_dotenv 

# OPENAI_API_KEY
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define vector store
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vector_store = Chroma(
    collection_name="Database",
    embedding_function=embeddings,
    persist_directory="backend/cbnlangchain/docs/chroma",
)

# Define prompts
q_prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""
Given the following conversation (delimited by <hs></hs>) and a follow up question, rephrase the follow up question to be a standalone question.
------
<hs>
{chat_history}
</hs>
------
Follow Up Question: {question}
Standalone question:
"""
)
prompt = PromptTemplate(
    input_variables=["chat_history", "context", "question"],
    template="""
% INSTRUCTIONS
- You are personal assistant named CBN Assistant who is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics.
- You are able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. 
- Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
- Always think step by step. If you don't know the answer to a question, please don't share false information.
- Answer like a Christian Broadcasting Network employee.
- Answer in the language of the question.

% YOUR TASKS
1. Answer the question at the end as helpfully as possible. You can use the following context (delimited by <ctx></ctx>) and the chat history (delimited by <hs></hs>).
If the question is "What is your question?", ask for more details.
------
<ctx>
{context}
</ctx>
------
<hs>
{chat_history}
</hs>
------
Question: {question}
Answer:

2. a) If necessary you can provide a link after answer the question related to the Bible, Jesus or CBN to learn more. For example, if the question about faith provide: https://www2.cbn.com/search/faith?search=faith.
b) If the conversation is about certain episode of the SuperBook, for example, episode "ROAR!", you can provide: https://us-en.superbook.cbn.com/gizmonote/g107 or https://us-en.superbook.cbn.com". 
""",
)

# Define memory
memory = ConversationTokenBufferMemory( 
    llm=OpenAI(),
    memory_key="chat_history", 
    input_key='question', 
    output_key='answer', 
    return_messages=True,
    max_token_limit=1500
)


# Define chain
def create_chain():    
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0), 
        chain_type="stuff", 
        retriever=vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4}), 
        condense_question_prompt=q_prompt,
        combine_docs_chain_kwargs={"prompt": prompt}, 
        memory=memory,
        get_chat_history=lambda h:h,
        return_source_documents=True,
        return_generated_question=True,
    )
    return chain

# chain = create_chain()

# while True:
#     print()
#     question = input("Question: ")

#     if question == "stop":
#         break

#     # Generate answer
#     response = chain({"question": question})
#     print()
#     print(f"Answer: {response['answer']}")