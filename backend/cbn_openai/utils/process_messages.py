from cbn_openai.utils.count_tokens import delete_previous_messages
from cbn_openai.vector_store import get_context
from config import PROMPT


def process_messages(user_input, messages):
    """Return valid list of messages"""
    
    for message in messages:
        if "timestamp" in message:
            del message["timestamp"] # delete timestamp key from messages

    messages.insert(0, {"role": "system", "content": PROMPT}) # insert system message
    augmented_query = get_context(user_input) # get relevant contexts
    messages.append({"role": "user", "content": augmented_query})
    conversation = delete_previous_messages(messages) # delete messages from memory to avoid model's token limit

    return conversation