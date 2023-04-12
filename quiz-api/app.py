from flask import Flask

#Permettre à votre application front-end d’effectuer des requêtes HTTP AJAX de type “cross-origin”
from flask_cors import CORS

app = Flask(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

if __name__ == "__main__":
    app.run()