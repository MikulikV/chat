import json
import requests
import os
from elastic_site_search import Client
from config import SEARCH_ENGINE


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
    },
    # {
    #     "name": "get_actual_information",
    #     "description": "Get actual information",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "key_query": {
    #                 "type": "string",
    #                 "description": "The key word or phrase, e.g. What is Orphan's Promise?",
    #             },
    #             "category": {
    #                 "type": "string",
    #                 "enum": ["Briefing Notes & Run Sheets", "Brands", "Programs", "Marketing Campaigns", "Product", "Prayer", "Caller Resources", "CBN PC Resources", "Digital Media"]
    #             },
    #         },
    #         "required": ["key_query"],
    #     },
    # }
]


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


def get_actual_information(key_query, category=""):
    """Get actual information"""
    print(key_query, category)
    url = "https://cbn.helpjuice.com/api/v3/search"
    headers = {
        'Authorization': os.environ["HELPJUICE_API_KEY"]           
    }
    categories = {
        "Briefing Notes & Run Sheets": 290795, 
        "Brands": 116262, 
        "Programs": 163994,
        "Marketing Campaigns": 146855,
        "Product": 146856,
        "Prayer": 116257,
        "Caller Resources": 116263, 
        "CBN PC Resources": 211074,
        "Digital Media": 282186
    }
    filters = {
        "query": key_query,
        "category_id": categories[category] if category else "" 
    }
    response = requests.get(url, headers=headers, params=filters)
    # search_api_key = os.environ["SEARCH_API_KEY"]
    # client = Client(api_key=search_api_key)
    # response = client.search(SEARCH_ENGINE, key_query, {"filters": {"entity-node": {"s_type": ["news", "article"]}}})
    # print(key_query)
    # print(response)
    # info = [(" ").join(page["m_rendered_item"]) for page in response["body"]["records"]["entity-node"][:1]] # get information from first 3 pages
    results = response.json()["searches"][:3]
    info = [{"answer": result["long_answer_sample"], "url": result["url"]} for result in results]
    cbn_info = {}
    if len(info) > 0:
        for i in range(0, len(info)):
            cbn_info[f"source_{i + 1}"] = info[i]
            
    return json.dumps(cbn_info)