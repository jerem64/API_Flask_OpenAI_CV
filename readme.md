
# Pense bête - Pour commencer une API Streamlit
1. Créer un nouvel environnement virtuel
```bash
python3 -m venv env
```
2. On l'active
```bash
source venv/bin/activate
```
3. On installe streamlit
```bash
pip install flask
```
4. On définit le fichier python a utiliseer par Flask
```bash
export FLASK_APP=main.py
```
5. On démarre l'app
```bash
flask run
```
6. On déploie avec
```bash
gcloud run deploy
```
## Attention
Ne pas pousser sur github la clé OpenAI_key.json, le projet etant public sur github.
Ajouter la clé au fichier .gitignore génère une erreur car au déploiement ce fichier est ignoré...
Note pour moi même, corriges ça, on devrait pouvoir pousser sur git et deployer des choses différentes