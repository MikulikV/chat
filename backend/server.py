from flask import Flask, request, Response, stream_with_context, json
from flask_cors import CORS
import requests
import sseclient
import os
# from openai.error import RateLimitError

from dotenv import load_dotenv 

# OPENAI_API_KEY
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# to deploy in Azure
# OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)

# handle cors
CORS(app)


@app.route('/')
def index():
    return "Hello world"


@app.route('/api/prompt', methods=['GET', 'POST'])
def prompt():
    if request.method == 'POST':
        prompt = request.json['prompt']
    
        # try:
        def generate():
            url = 'https://api.openai.com/v1/chat/completions'
            headers = {
                'content-type': 'application/json; charset=utf-8',
                'Authorization': f"Bearer {OPENAI_API_KEY}"            
            }

            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system', 'content': 'You are an AI assistant that answers questions about anything.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0, 
                'max_tokens': 1000,
                'stream': True,            
            }

            response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
            client = sseclient.SSEClient(response)
            for event in client.events():
                if event.data != '[DONE]':
                    try:
                        text = json.loads(event.data)['choices'][0]['delta']['content']
                        yield(text)
                    except:
                        yield('')

        return Response(stream_with_context(generate()))
        # except error:
        #     return Response("The server is experiencing a high volume of requests. Please try again later.")


if __name__ == '__main__':
    app.run(port=8080, debug=True)