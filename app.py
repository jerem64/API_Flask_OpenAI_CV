# app.py
import secrets
from flask import Flask, session, request, make_response
from flask_cors import CORS
from config import Config
from conversational_agent import create_conversational_agent
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError

# Create the Flask application
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

#Enable Cross-Origin Resource Sharing (CORS) for the app
CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGIN}})

# Create an instance of the agent
agent = create_conversational_agent()

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
    try:
        result = agent.invoke({"input":query})
    except Exception as generic_error:
        result = f"Generic error: {generic_error}"
    
    # Prepare and return the JSON response
    response = make_response({'output': result})
    response.headers.add('Access-Control-Allow-Origin', Config.CORS_ORIGIN)
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

# Define a route for handling GET requests to '/get_auth_uri'
@app.route('/get_auth_uri', methods=['GET', 'OPTIONS'])
def get_auth_uri():
    # Handle preflight OPTIONS request for CORS
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', Config.CORS_ORIGIN)
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response    
    
    try:
        redirect_uri = 'http://localhost:4200/redirect-handler' if Flask(__name__).debug else 'https://jeremy.chassin.dev/redirect-handler'
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/calendar'], redirect_uri=redirect_uri)


        authorization_url, state = flow.authorization_url(prompt='consent')
    
    except Exception as e:
        result = str(e)
    
    # Prepare and return the JSON response
    response = make_response({'authorization_url': authorization_url, "state":state})
    response.headers.add('Access-Control-Allow-Origin', Config.CORS_ORIGIN)
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

# Define a route for handling POST requests to '/create_credentials'
@app.route('/create_credentials', methods=['POST', 'OPTIONS'])
def create_credentials():
    # Handle preflight OPTIONS request for CORS
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', Config.CORS_ORIGIN)
        response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    try:
        # Extract JSON data from the request
        data = request.get_json()
        authorizationCode = data['authorizationCode']
        state = data['state']
    
        redirect_uri = 'http://localhost:4200/redirect-handler' if app.debug else 'https://jeremy.chassin.dev/redirect-handler'
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/calendar'], redirect_uri=redirect_uri)
        
        flow.fetch_token(code=authorizationCode)

        credentials = flow.credentials
        
        with open('credentials.json', 'w') as f:
            f.write(credentials.to_json())
    
        result = "Credentials created successfully"
    except Exception as e:
        result = str(e)
    
    # Prepare and return the JSON response
    response = make_response({'output': result})
    response.headers.add('Access-Control-Allow-Origin', Config.CORS_ORIGIN)
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response




if __name__ == '__main__':
    app.run()