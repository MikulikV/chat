from flask import Flask, request, Response, stream_with_context, json, jsonify
from flask_cors import CORS, cross_origin
import requests
import sseclient
import os
import tiktoken
import openai
from openai.error import RateLimitError
from cbnlangchain.qa import create_chain
from cbnpinecone import get_context
from dotenv import load_dotenv 

load_dotenv()

# const
openai.api_key = os.environ["OPENAI_API_KEY"]
max_response_tokens = 500
token_limit= 4000
prompt = "You are a helpful assistant, your name is CBN Assistant. You are a Christian and your task is to help people to be better."

app = Flask(__name__)
# handle cors
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()  # CORS
def index():
    return "Hello world"


# Function to count tokens
def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


@app.route('/api/chat', methods=['GET', 'POST'])
@cross_origin()  # CORS
def chat():
    if request.method == 'POST':
        user_input = request.json.get('user_input')
        conversation = request.json.get('conversation')
        
        # Delete timestamp key from messages
        for obj in conversation:
            if "timestamp" in obj:
                del obj["timestamp"]

        conversation.append({"role": "user", "content": user_input})

        # Delete messages from memory to avoid model's token limit
        num_tokens = num_tokens_from_messages(conversation)
        while (num_tokens+max_response_tokens >= token_limit):
            del conversation[1] 
            num_tokens = num_tokens_from_messages(conversation)

        try:
            def generate():
                url = 'https://api.openai.com/v1/chat/completions'
                headers = {
                    'content-type': 'application/json; charset=utf-8',
                    'Authorization': f"Bearer {openai.api_key}"            
                }

                data = {
                    'model': 'gpt-3.5-turbo',
                    'messages': [{"role": "system", "content": prompt}, *conversation],
                    'temperature': 0, 
                    'max_tokens': max_response_tokens,
                    'stream': True,            
                }

                completion = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
                client = sseclient.SSEClient(completion)
                for event in client.events():
                    if event.data != '[DONE]':
                        try:
                            text = json.loads(event.data)['choices'][0]['delta']['content']
                            yield(text)
                        except:
                            yield('')

            response = stream_with_context(generate())
        except RateLimitError:
            response = "The server is experiencing a high volume of requests. Please try again later."
        
        return Response(response)
    

@app.route('/api/retrieval', methods=['GET', 'POST'])
@cross_origin()  # CORS
def retrieval():
    if request.method == 'POST':
        user_input = request.json.get('user_input')
        conversation = request.json.get('conversation')
        
        # Delete timestamp key from messages
        for obj in conversation:
            if "timestamp" in obj:
                del obj["timestamp"]
        
        # get relevant contexts
        augmented_query = get_context(user_input)
        conversation.append({"role": "user", "content": augmented_query})

        # Delete messages from memory to avoid model's token limit
        num_tokens = num_tokens_from_messages(conversation)
        while (num_tokens+max_response_tokens >= token_limit):
            del conversation[1] 
            num_tokens = num_tokens_from_messages(conversation)

        try:
            def generate():
                url = 'https://api.openai.com/v1/chat/completions'
                headers = {
                    'content-type': 'application/json; charset=utf-8',
                    'Authorization': f"Bearer {openai.api_key}"            
                }

                data = {
                    'model': 'gpt-3.5-turbo',
                    'messages': [{"role": "system", "content": prompt}, *conversation],
                    'temperature': 0, 
                    'max_tokens': max_response_tokens,
                    'stream': True,            
                }

                completion = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
                client = sseclient.SSEClient(completion)
                for event in client.events():
                    if event.data != '[DONE]':
                        try:
                            text = json.loads(event.data)['choices'][0]['delta']['content']
                            yield(text)
                        except:
                            yield('')

            response = stream_with_context(generate())
        except RateLimitError:
            response = "The server is experiencing a high volume of requests. Please try again later."
        
        return Response(response)
    

@app.route('/api/langchain', methods=['GET', 'POST'])
@cross_origin()  # CORS
def langchain():
    if request.method == 'POST':
        user_input = request.json.get('user_input')
        chain = create_chain()
        response = chain({"question": user_input})

        return jsonify(response['answer'])
        
        

if __name__ == '__main__':
    app.run(port=8080, debug=True)