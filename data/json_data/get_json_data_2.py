import requests
import json

# api_url = "https://appscdn.superbook.cbn.com/api/bible/app_games.json/?lang=en&f=trivia&id=0&sort=null&r=100000"
api_url = "https://appscdn.superbook.cbn.com/api/bible/app_profiles.json/?lang=en&f=all&id=0&sort=null&r=100000"
qa = []
# file_path = "backend/data/json_data/games.json"
file_path = "backend/data/json_data/profiles.json"

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    # qa.extend([{"question": item["question"], "correct answer": item["correct_ans"], "answer_1": item["answer_1"], "answer_2": item["answer_2"], "answer_3": item["answer_3"], "answer_4": item["answer_4"]} for item in data["response"] if isinstance(item, dict)])
    qa.extend([{"profile_name": item["name"], "profile_description": item["body"], "profile_bible_infoscan": item["profile_bible_infoscan"], "profile_life_lessons": item["profile_life_lessons"], "profile_key_scripture": item["profile_key_scripture"]} for item in data["response"] if isinstance(item, dict)])
else:
    print("Error")

unique_qa = []
for obj in qa:
    if obj not in unique_qa:
        unique_qa.append(obj)


with open(file_path, "w") as json_file:
    json.dump(unique_qa, json_file)





