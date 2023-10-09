import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]
file_id = "file-mAVL3cm6yd7WxKdjEBj3EIN4"
model_name = "gpt-3.5-turbo"

response = openai.FineTuningJob.create(
    training_file=file_id,
    model=model_name,
    suffix="SB-with-10-laws",
)
job_id = response["id"]

print(f"Status: {response['status']}")
print(f"Fine-tuning job created successfully with Job ID: {job_id}")

response = openai.FineTuningJob.retrieve(job_id)
fine_tuned_model_id = response["fine_tuned_model"]
print(f"Fine-tuned model ID: {fine_tuned_model_id}")
