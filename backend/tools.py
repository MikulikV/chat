from dotenv import load_dotenv
import os
import openai
import json
import requests

# OPENAI_API_KEY
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

weather_codes = {0: "Clear sky", 1: "Mainly clear, partly cloudy, and overcast", 2: "Mainly clear, partly cloudy, and overcast", 3: "Mainly clear, partly cloudy, and overcast", 45: "Fog and depositing rime fog", 48: "Fog and depositing rime fog", 51: "Drizzle: Light, moderate, and dense intensity", 53: "Drizzle: Light, moderate, and dense intensity", 55: "Drizzle: Light, moderate, and dense intensity", 56: "Freezing Drizzle: Light and dense intensity", 57: "Freezing Drizzle: Light and dense intensity", 61: "Rain: Slight, moderate and heavy intensity", 63: "Rain: Slight, moderate and heavy intensity", 65: "Rain: Slight, moderate and heavy intensity", 66: "Freezing Rain: Light and heavy intensity", 67: "Freezing Rain: Light and heavy intensity", 71: "Snow fall: Slight, moderate, and heavy intensity", 73: "Snow fall: Slight, moderate, and heavy intensity", 75: "Snow fall: Slight, moderate, and heavy intensity", 77: "Snow grains", 80: "Rain showers: Slight, moderate, and violent", 81: "Rain showers: Slight, moderate, and violent", 82: "Rain showers: Slight, moderate, and violent", 85: "Snow showers slight and heavy", 86: "Snow showers slight and heavy",	95: "Thunderstorm: Slight or moderate", 96: "Thunderstorm with slight and heavy hail", 99: "Thunderstorm with slight and heavy hail"}

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    city, *state = location.split(', ')
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

    url_weather = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch"
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

def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "What's the weather like in Virginia Beach?"}]
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
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        response_message = second_response["choices"][0]["message"]
        
    return response_message

print(run_conversation())