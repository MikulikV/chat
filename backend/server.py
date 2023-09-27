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
from cbn_openai.tools import functions, get_current_weather
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
                    'functions': functions,
                    'function_call': "auto",
                    'max_tokens': max_response_tokens,
                    'stream': True,            
                }

                completion = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
                client = sseclient.SSEClient(completion)
                function_name = ""
                function_args = ""
                flag = False
                for event in client.events():
                    if event.data != '[DONE]':
                        try:
                            content = json.loads(event.data)['choices'][0]['delta']
                            text = content.get("content", "")
                            if content.get("function_call"):
                                flag = True
                                function_name += content["function_call"].get("name", "")
                                function_args += content["function_call"].get("arguments", "")
                            else:
                                yield(text)
                        except Exception as e:
                            yield('Error: ' + e)

                if flag:
                    available_functions = {
                        "get_current_weather": get_current_weather,
                    }  # only one function in this example, but you can have multiple
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(function_args)
                    function_response = function_to_call(**function_args)
                    # Step 4: send the info on the function call and function response to GPT
                    conversation.append({ "role": "assistant", "content": f"{content}", "function_call": {"name": function_name, "arguments": f"{function_args}"} })  # extend conversation with assistant's reply
                    conversation.append({ "role": "function", "name": function_name, "content": function_response })  # extend conversation with function response
                    second_response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=conversation,
                        stream=True
                    )  # get a new response from GPT where it can see the function response
                    try:
                        for chunk in second_response:
                            content = chunk["choices"][0]["delta"]
                            text = content.get("content", "")
                            yield(text)
                    except Exception as e:
                        print('Error: ', e)
                        return 503

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