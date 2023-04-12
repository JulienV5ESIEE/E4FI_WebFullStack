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
    
    
## LANCER VENV
# source venv/Scripts/activate


######################################## DOCKER ########################################
## CREER UNE IMAGE DOCKER 
# docker image build -t quiz-local-api .
# docker container run -it --rm -p 5000:5000 --name quiz-local-api quiz-local-api

## SUPPRIMER D'ANCIEN CONTAINER
# docker container ls -a
# docker container rm <nom-ou-id-des-containers>

## SUPPRIMER D'ANCIENNE IMAGE
# docker image ls
# docker image rm <nom-ou-id-des-images>

## SUPPRIMER UNE IMAGE ORPHELINE
# docker image prune


######################################## GIT ########################################
#
#
