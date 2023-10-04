import tiktoken
from config import MODEL, TOKEN_LIMIT, MAX_RESPONSE_TOKENS


def num_tokens_from_messages(messages):
    """Count tokens of the conversation"""
    encoding = tiktoken.encoding_for_model(MODEL)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += 1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant

    return num_tokens


def delete_previous_messages(conversation):
    """Delete messages from memory to avoid model's token limit"""
    num_tokens = num_tokens_from_messages(conversation)
    while (num_tokens + MAX_RESPONSE_TOKENS >= TOKEN_LIMIT):
        del conversation[1] 
        num_tokens = num_tokens_from_messages(conversation)

    return conversation

