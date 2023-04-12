from flask import Flask

#Permettre à votre application front-end d’effectuer des requêtes HTTP AJAX de type “cross-origin”
from flask_cors import CORS

app = Flask(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/') ## La route
def hello_world(): ## Son nom
	x = 'world'
	return f"Hello, {x}" # Son retour


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200


if __name__ == "__main__":
    app.run() # DOIT TOUJOURS ETRE A LA FIN
    