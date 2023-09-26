from flask import Flask, request, Response, stream_with_context, json, jsonify
from flask_cors import CORS, cross_origin
import requests
import sseclient
import os
import openai
from openai.error import RateLimitError
from cbn_langchain.qa import create_chain
from cbn_openai.vector_store import get_context
from cbn_openai.utils.count_tokens import delete_previous_messages
from dotenv import load_dotenv 

load_dotenv()

# const
openai.api_key = os.environ["OPENAI_API_KEY"]
model = "gpt-3.5-turbo"
token_limit = 4000
temperature = 0
max_response_tokens = 500
prompt = "You are a helpful assistant, your name is CBN Assistant. You are a Christian and your task is to help people to be better."

app = Flask(__name__)
# handle cors
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()  # CORS
def index():
    return "Hello world"


@app.route('/api/chat', methods=['GET', 'POST'])
@cross_origin()  # CORS
def chat():
    if request.method == 'POST':
        user_input = request.json.get('user_input')
        conversation = request.json.get('conversation')
        
        # Delete timestamp key from messages
        for message in conversation:
            if "timestamp" in message:
                del message["timestamp"]

        # Get relevant contexts
        augmented_query = get_context(user_input)
        conversation.append({"role": "user", "content": augmented_query})
        # Delete messages from memory to avoid model's token limit
        conversation = delete_previous_messages(conversation)

        try:
            def generate():
                url = 'https://api.openai.com/v1/chat/completions'
                headers = {
                    'content-type': 'application/json; charset=utf-8',
                    'Authorization': f"Bearer {openai.api_key}"            
                }

                data = {
                    'model': model,
                    'messages': [{"role": "system", "content": prompt}, *conversation],
                    'temperature': temperature, 
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
        chain = create_chain(temperature)
        response = chain({"question": user_input})

        return jsonify(response['answer'])
        

if __name__ == '__main__':
    app.run(port=8080, debug=True)