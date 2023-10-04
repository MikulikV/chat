import requests
import json

api_url = [
    "https://appscdn.superbook.cbn.com/api/bible/app_profiles.json/?lang=en&f=all&id=0",
    "https://appscdn.superbook.cbn.com/api/bible/app_profiles.json/?lang=en&f=all&id=0",
    "https://appscdn.superbook.cbn.com/api/bible/app_profiles.json/?lang=en&f=all&id=0",
    "https://appscdn.superbook.cbn.com/api/bible/app_profiles.json/?lang=en&f=all&id=0",
    "https://appscdn.superbook.cbn.com/api/bible/app_profiles.json/?lang=en&f=all&id=0",
    "https://appscdn.superbook.cbn.com/api/bible/app_profiles.json/?lang=en&f=all&id=0",
    "https://appscdn.superbook.cbn.com/api/bible/app_profiles.json/?lang=en&f=all&id=0",
    "https://appscdn.superbook.cbn.com/api/bible/app_profiles.json/?lang=en&f=all&id=0",
    "https://appscdn.superbook.cbn.com/api/bible/app_profiles.json/?lang=en&f=all&id=0",
] 
qa = []
file_path = "backend/data/profiles.json"

for url in api_url:
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json() 
        qa.extend([{"question": item["question"], "answer": item["answer"]} for item in data["response"] if isinstance(item, dict)])
    else:
        print("Error")

unique_qa = []
for obj in qa:
    if obj not in unique_qa:
        unique_qa.append(obj)


with open(file_path, "w") as json_file:
    json.dump(unique_qa, json_file)





