# app.py
from flask import Flask, request, make_response
from flask_cors import CORS
from config import Config
from qa_chain import create_qa_chain

# Create the Flask application
app = Flask(__name__)

#Enable Cross-Origin Resource Sharing (CORS) for the app
CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGIN}})

# Create an instance of the question-answering chain
qa_chain = create_qa_chain()

# Define a route for handling POST requests to '/ask_question'
@app.route('/ask_question', methods=['POST', 'OPTIONS'])
def ask_question():
    # Handle preflight OPTIONS request for CORS
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', Config.CORS_ORIGIN)
        response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    # Extract JSON data from the request
    data = request.get_json()
    input_string = data['input']
    
    # Prepare the question by removing '*' to prevent tricks
    query = input_string

    # Get the response from the question-answering chain
    output = qa_chain({"query": query})
    
    # Prepare and return the JSON response
    response = make_response({'output': output["result"]})
    response.headers.add('Access-Control-Allow-Origin', Config.CORS_ORIGIN)
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

if __name__ == '__main__':
    app.run()