from flask import json
import openai
import requests
import sseclient
import os
from dotenv import load_dotenv
from config import FINE_TUNED_MODEL, TEMPERATURE, MAX_RESPONSE_TOKENS
from cbn_openai.tools import functions, get_current_weather, get_real_time_information

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
available_functions = {
    "get_current_weather": get_current_weather,
    "get_real_time_information": get_real_time_information,
}


def generate(conversation):
    """Create completion and generate answer"""
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'Authorization': f"Bearer {openai.api_key}"            
    }
    data = {
        'model': FINE_TUNED_MODEL,
        'messages': conversation,
        'temperature': TEMPERATURE, 
        'functions': functions,
        'function_call': "auto",
        'max_tokens': MAX_RESPONSE_TOKENS,
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
                        
    # Check if GPT wanted to call a function
    if flag:
        # Call the function
        function_to_call = available_functions[function_name]
        function_args = json.loads(function_args)
        function_response = function_to_call(**function_args)
        print(function_response)
        # Send the info on the function call and function response to GPT
        conversation.append({ "role": "assistant", "content": f"{content}", "function_call": {"name": function_name, "arguments": f"{function_args}"} })  # extend conversation with assistant's reply
        conversation.append({ "role": "function", "name": function_name, "content": function_response })  # extend conversation with function response
        yield from generate(conversation) # generate second response
    

        