from dotenv import load_dotenv
import os
import openai
import json
import requests

# OPENAI_API_KEY
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_codes = {0: "Clear sky", 1: "Mainly clear, partly cloudy, and overcast", 2: "Mainly clear, partly cloudy, and overcast", 3: "Mainly clear, partly cloudy, and overcast", 45: "Fog and depositing rime fog", 48: "Fog and depositing rime fog", 51: "Drizzle: Light, moderate, and dense intensity", 53: "Drizzle: Light, moderate, and dense intensity", 55: "Drizzle: Light, moderate, and dense intensity", 56: "Freezing Drizzle: Light and dense intensity", 57: "Freezing Drizzle: Light and dense intensity", 61: "Rain: Slight, moderate and heavy intensity", 63: "Rain: Slight, moderate and heavy intensity", 65: "Rain: Slight, moderate and heavy intensity", 66: "Freezing Rain: Light and heavy intensity", 67: "Freezing Rain: Light and heavy intensity", 71: "Snow fall: Slight, moderate, and heavy intensity", 73: "Snow fall: Slight, moderate, and heavy intensity", 75: "Snow fall: Slight, moderate, and heavy intensity", 77: "Snow grains", 80: "Rain showers: Slight, moderate, and violent", 81: "Rain showers: Slight, moderate, and violent", 82: "Rain showers: Slight, moderate, and violent", 85: "Snow showers slight and heavy", 86: "Snow showers slight and heavy",	95: "Thunderstorm: Slight or moderate", 96: "Thunderstorm with slight and heavy hail", 99: "Thunderstorm with slight and heavy hail"}
    city, *state = location.split(', ')
    unit = "fahrenheit" if unit == None else unit
    url_location = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json"
    results = requests.get(url_location)
    locations = results.json()["results"]
    latitude = locations[0]["latitude"]
    longitude = locations[0]["longitude"]
    for loc in locations:
        if state:
            if loc["admin1"] == state[0] or loc["country"] == state[0]:
                latitude = loc["latitude"]
                longitude = loc["longitude"]

    url_weather = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&current_weather=true&temperature_unit={unit}&windspeed_unit=mph&precipitation_unit=inch"
    response = requests.get(url_weather)
    data = response.json()
    current_weather = data["current_weather"]
    weather_info = {
        "location": location,
        "temperature": current_weather["temperature"],
        "unit": unit,
        "forecast": weather_codes[current_weather["weathercode"]],
    }
    return json.dumps(weather_info)


functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, California",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }
]


def call_function(content, function_name, function_args, messages):
    available_functions = {
        "get_current_weather": get_current_weather,
    }  # only one function in this example, but you can have multiple
    # function_name = response_message["function_call"]["name"]
    function_to_call = available_functions[function_name]
    function_args = json.loads(function_args)
    function_response = function_to_call(**function_args)
    # Step 4: send the info on the function call and function response to GPT
    messages.append({ "role": "assistant", "content": content, "function_call": {"name": function_name, "arguments": f"{function_args}"} })  # extend conversation with assistant's reply
    messages.append({ "role": "function", "name": function_name, "content": function_response })  # extend conversation with function response
    second_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )  # get a new response from GPT where it can see the function response
    # response_message = second_response["choices"][0]["message"]
    try:
        for chunk in second_response:
            content = chunk["choices"][0]["delta"]
            text = content.get("content", "")
            yield(text)
    except Exception as e:
        print('Error:', e)
        return 503


def run_conversation():
    messages=[{"role": "user", "content": "What's the weather like in Virginia Beach?"}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto",
        stream=True
    )
    # response_message = response["choices"][0]["message"]
    # print(response)
    # for chunk in response:
    #     print(chunk)

    try:
        function_name = ""
        function_args = ""
        for chunk in response:
            content = chunk["choices"][0]["delta"]
            current_answer = content.get("content", "")
            if content.get("function_call"):
                function_name += content["function_call"].get("name", "")
                function_args += content["function_call"].get("arguments", "")
            else:
                print(current_answer)
        current_answer = call_function(current_answer, function_name, function_args, messages)
    except Exception as e:
        print('Error:', e)
        return 503


# print(run_conversation())