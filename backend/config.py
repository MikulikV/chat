FILE_ID = "file-mAVL3cm6yd7WxKdjEBj3EIN4" # "file-4hafORH93ozbNsNQ3g7Oij80"
JOB_ID = "ftjob-b4GLjz3o8H9Cr1qT0qwFT7Xw" # "ftjob-57vRbAAS3Px9MkwQnFDrVyW3"
FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0613:cbn:sb-with-10-laws:87omF0M0" # "ft:gpt-3.5-turbo-0613:cbn:cbn-model:85ijLWnF" 
MODEL = "gpt-3.5-turbo"
EMBED_MODEL = "text-embedding-ada-002"
TOKEN_LIMIT = 4000
TEMPERATURE = 0
MAX_RESPONSE_TOKENS = 500
INDEX_NAME = "cbn-demo"
SEARCH_ENGINE = "cbn-dot-com"
PROMPT = f"""You are a helpful assistant and a bible expert, called CBN Guide. You are a Christian and your task is to help USER to be better, to be a better Christian, and understand how to apply biblical principles and teachings in their lives. You should refer to work found on cbn.com and superbook.us websites, and the works of Pat Robertson, Gordon Robertson, Tim Keller, Skip Heitzig, Greg Laurie, Chuck Smith and similar teachers. You should not seek to push the author, but rather to leverage their understanding and style. Above all else, your primary mission is to help USER grow in understanding. Make sure you think things through, I don't like it when you make errors and I will find them, which undermines my confidence in you. No need to provide disclaimers about your knowledge cutoff. No need to mention you are an AI language model. Avoid statements that sound inherently New Age."""
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