import requests
import os

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
    "query": "Orphan's Promise",
    "category_id": categories["Brands"]
}
result = requests.get(url, headers=headers, params=filters)
print(result.json())
print(result.json()["searches"][0]["long_answer_sample"])