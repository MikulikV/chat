from flask import Flask, request, Response, stream_with_context, jsonify
from flask_cors import CORS, cross_origin
from openai.error import RateLimitError
from cbn_langchain.qa import create_chain
from cbn_openai.utils.process_messages import process_messages
from cbn_openai.completion import generate


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
        conversation = process_messages(user_input, conversation)

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