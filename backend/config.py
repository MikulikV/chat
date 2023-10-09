FILE_ID = "file-4hafORH93ozbNsNQ3g7Oij80" # "file-mAVL3cm6yd7WxKdjEBj3EIN4"
JOB_ID = "ftjob-57vRbAAS3Px9MkwQnFDrVyW3" # "ftjob-b4GLjz3o8H9Cr1qT0qwFT7Xw"
FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0613:cbn:cbn-model:85ijLWnF"
MODEL = "gpt-3.5-turbo"
EMBED_MODEL = "text-embedding-ada-002"
TOKEN_LIMIT = 4000
TEMPERATURE = 0
MAX_RESPONSE_TOKENS = 500
INDEX_NAME = "cbn-demo"
SEARCH_ENGINE = "cbn-dot-com"
PROMPT = f"""You are a helpful assistant, your name is CBN Assistant. You are a Christian and your task is to help people to be better."""
# Answer the following questions as best you can. You have access to the following tools:
# ```
# get_current_weather,
# get_real_time_information
# ```

# Use the following format of your chain of thoughts:

# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of tools above
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question

# Begin!

# Question:
# Helpful Answer:"""