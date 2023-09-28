from flask import Flask, request, Response, stream_with_context, jsonify
from flask_cors import CORS, cross_origin
from openai.error import RateLimitError
from cbn_langchain.qa import create_chain
from cbn_openai.vector_store import get_context
from cbn_openai.utils.count_tokens import delete_previous_messages
from cbn_openai.completion import generate
from config import PROMPT


app = Flask(__name__)
# handle cors
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()  # CORS
def index():
    return "Hello world"


@app.route('/api/chat', methods=['GET', 'POST'])
@cross_origin()  # CORS
def chat():
    if request.method == 'POST':
        user_input = request.json.get('user_input')
        conversation = request.json.get('conversation')
        
        # Delete timestamp key from messages
        for message in conversation:
            if "timestamp" in message:
                del message["timestamp"]

        # Insert system message
        conversation.insert(0, {"role": "system", "content": PROMPT})
        # Get relevant contexts
        augmented_query = get_context(user_input)
        conversation.append({"role": "user", "content": augmented_query})
        # Delete messages from memory to avoid model's token limit
        conversation = delete_previous_messages(conversation)

        try:
            response = stream_with_context(generate(conversation))
        except RateLimitError:
            response = "The server is experiencing a high volume of requests. Please try again later."
        
        return Response(response)
    

@app.route('/api/langchain', methods=['GET', 'POST'])
@cross_origin()  # CORS
def langchain():
    if request.method == 'POST':
        user_input = request.json.get('user_input')
        chain = create_chain()
        response = chain({"question": user_input})

        return jsonify(response['answer'])
        

if __name__ == '__main__':
    app.run(port=8080, debug=True)