# HOW TO MAKE IT WORK
1. Create a new virtual environment
```bash
python3 -m venv env
```
2. Activate the virtual environment
```bash
source env/bin/activate
```
3. Install required packages
```bash
pip install -r requirements.txt
```
4. Define the Python file to be used by Flask
```bash
export FLASK_APP=app.py
```
5. Start the app
```bash
flask run --debug
```
6. Deploy with
```bash
gcloud run deploy
```
## WARNING
Do not push the key API_Keys.json on GitHug as it is public, if done OpenAI will detect it and mark the key as leaked.
Adding the key to the .gitignore file generate an error because when deploying the file is ignored...