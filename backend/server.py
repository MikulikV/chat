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


max_response_tokens = 500
token_limit= 4000

# def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
#     encoding = tiktoken.encoding_for_model(model)
#     num_tokens = 0
#     for message in messages:
#         num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
#         for key, value in message.items():
#             num_tokens += len(encoding.encode(value))
#             if key == "name":  # if there's a name, the role is omitted
#                 num_tokens += -1  # role is always required and always 1 token
#     num_tokens += 2  # every reply is primed with <im_start>assistant
#     return num_tokens


@app.route('/api/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.json.get('user_input')
        conversation = request.json.get('conversation', [{"role": "system", "content": "You are a helpful assistant."}])
        
        conversation.append({"role": "user", "content": user_input})

        # num_tokens = num_tokens_from_messages(conversation)
        # while (num_tokens+max_response_tokens >= token_limit):
        #     del conversation[1] 
        #     num_tokens = num_tokens_from_messages(conversation)

        # try:
        def generate():
            url = 'https://api.openai.com/v1/chat/completions'
            headers = {
                'content-type': 'application/json; charset=utf-8',
                'Authorization': f"Bearer {OPENAI_API_KEY}"            
            }

            data = {
                'model': 'gpt-3.5-turbo',
                'messages': conversation,
                'temperature': 0, 
                'max_tokens': token_limit,
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
        
        # conversation.append({"role": "assistant", "content": stream_with_context(generate())})

        # return Response(conversation)
        return Response(stream_with_context(generate()))
        # except RateLimitError:
        #     return Response("The server is experiencing a high volume of requests. Please try again later.")


if __name__ == '__main__':
    app.run(port=8080, debug=True)