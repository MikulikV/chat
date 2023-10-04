import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]
dataset = "backend/cbn_openai/finetuning/test_dataset.jsonl"

response = openai.File.create(
  file=open(dataset, "rb"),
  purpose="fine-tune"
)
file_id = response["id"]

print(f"File uploaded successfully with ID: {file_id}")