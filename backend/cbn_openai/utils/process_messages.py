from config import PROMPT


def process_messages(messages):
    """Return valid list of messages"""
    
    for message in messages:
        if "timestamp" in message:
            del message["timestamp"] # delete timestamp key from messages

    messages.insert(0, {"role": "system", "content": PROMPT}) # insert system message

    return messages