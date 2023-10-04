import requests
import json

api_url = [
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=0",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=1",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=2",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=3",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=4",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=5",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=6",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=7",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=8",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=9",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=10",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=11",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=12",
    "https://appscdn.superbook.cbn.com/api/bible/app_qanda.json/?lang=en&f=all&id=13",
] 
qa = []
file_path = "backend/data/qa.json"

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





