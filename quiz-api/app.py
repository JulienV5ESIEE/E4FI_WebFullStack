from flask import Flask, jsonify, request
import hashlib, json, os, sys, jwt, sqlite3
import datetime
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from jwt_utils import secret, decode_token, build_token, JwtError
from questions import Question, add_question, remove_question, remove_all_questions, get_question_by_id, get_question_by_position, update_question, get_all_questions
from participations import participation_add, participation_remove_all, get_position_score
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Setup the Flask-JWT-Extended extension
# CE MDP DOIT ETRE LE MEME QUE DANS JWT_UTILS.PY !!!
app.config["JWT_SECRET_KEY"] = "notresupermotdepasse2023ESIEE"
app.config["JWT_HEADER_TYPE"] = "Bearer"
jwt = JWTManager(app)


@app.route('/rebuild-db', methods=['POST'])
def rebuild_db():
    try:
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS possible_answers')
        cursor.execute('DROP TABLE IF EXISTS questions')
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions 
                        (id INTEGER PRIMARY KEY,
                        text TEXT NOT NULL,
                        title TEXT NOT NULL,
                        image TEXT NOT NULL,
                        position INTEGER NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS possible_answers 
                        (id INTEGER PRIMARY KEY,
                        text TEXT NOT NULL,
                        isCorrect INTEGER NOT NULL,
                        question_id INTEGER NOT NULL,
                        FOREIGN KEY (question_id) REFERENCES questions (id))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS participations (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        score INTEGER NOT NULL);''')
        connection.commit()
        connection.close()
        return "Ok", 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/quiz-info', methods=['GET'])
def quiz_info():
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM questions")
    row_count = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM participations ORDER BY score DESC")
    participations = cursor.fetchall()
    if participations is None:
        participations = []
    scores = []
    for p in participations:
        scores.append({'playerName': p[1], 'score': p[2]})
    quiz_data = {
        'scores': scores,
        'size': row_count,
    }
    return jsonify(quiz_data)



################################################ QUESTIONS ################################################

# ADD QUESTION
@app.route('/questions', methods=['POST'])
@jwt_required(optional=True)
def add_questions():
    current_user = get_jwt_identity()
    if current_user:
        question_data = request.get_json()
        print(question_data, file=sys.stdout)
        try:
            question = Question(None, question_data['text'], question_data['title'],
                                question_data['image'], question_data['position'], question_data['possibleAnswers'])
            question_id = add_question(question.to_dict())
            return {"id": question_id}, 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify(logged_in_as=current_user), 401


# GET QUESTION BY ID
@app.route('/questions/<question_id>', methods=['GET'])
def get_questions(question_id):
    question = get_question_by_id(question_id)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404
    return jsonify(question.to_dict()), 200


# UPDATE QUESTION
@app.route('/questions/<int:question_id>', methods=['PUT'])
@jwt_required(optional=True)
def update_questions(question_id):
    current_user = get_jwt_identity()
    if current_user:
        question_data = request.get_json()
        try:
            question = Question(question_id, question_data['text'], question_data['title'],
                                question_data['image'], question_data['position'], question_data['possibleAnswers'])
            print(question.to_dict(), file=sys.stdout)
            result = update_question(question_id, question.to_dict())
            if result is None:
                return jsonify({'error': 'Question not found'}), 404
            else:
                return jsonify(question.to_dict()), 204
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify(logged_in_as=current_user), 401


# GET QUESTION BY POSITION
@app.route('/questions', methods=['GET'])
def get_questions_by_position():
    position = request.args.get('position')
    if position is None:
        return jsonify({'error': 'Missing parameter: position'}), 400
    question = get_question_by_position(position)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404
    return jsonify(question.to_dict()), 200


# REMOVE QUESTION BY ID
@app.route('/questions/<int:question_id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_question(question_id):
    current_user = get_jwt_identity()
    if current_user:
        try:
            result = remove_question(question_id)
            if result is None:
                return jsonify({'error': 'Question not found'}), 404
            else:
                return {"message": "Question deleted successfully"}, 204
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify(logged_in_as=current_user), 401
    
    
# GET ALL QUESTIONS
@app.route('/questions/get_all', methods=['GET'])
def get_questions_all():
    question = get_all_questions()
    if question is None:
        return jsonify({'error': 'Questions not found'}), 404
    return question, 200
    
    

# REMOVE ALL QUESTIONS

@app.route('/questions/all', methods=['DELETE'])
@jwt_required(optional=True)
def delete_all_questions():
    current_user = get_jwt_identity()
    if current_user:
        try:
            remove_all_questions()
            return {"message": "All questions deleted successfully"}, 204
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify(logged_in_as=current_user), 401


################################################ PARTICIPATIONS ################################################

# ADD PARTICIPATION
@app.route('/participations', methods=['POST'])
def add_participations():
    payload = request.get_json()
    questions = get_all_questions()
    # SI il n'y a pas le meme nombre de reponses et de questions
    if len(payload['answers']) != len(questions):
        return {"error":"Bad request"}, 400
    
    score = 0
    i = 0
    answers = payload['answers']
    for question in questions:
        # Vérifier si la réponse de l'utilisateur est correcte
        if question['possibleAnswers'][answers[i]-1]['isCorrect']:
            score += 1
        i += 1
    participation_add(payload['playerName'], score)
    return {"playerName": payload['playerName'], "score":score}, 200


# DELETE ALL PARTICIPATIONS
@app.route('/participations/all', methods=['DELETE'])
@jwt_required(optional=True)
def remove_all_participations():
    try:
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({'error': 'Invalid user token'}), 401
        participation_remove_all()
        return jsonify({'message': 'All participations have been deleted'}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    password = payload.get('password')
    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    if hashed_password == "d8170650479293c12e0201e5fdf45f40":  # flask2023
        token = build_token()
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid password'}), 401



if __name__ == "__main__":
    app.run(port=5000)  # DOIT TOUJOURS ETRE A LA FIN


# LANCER VENV
# source venv/Scripts/activate

# npm run dev


######################################## DOCKER ########################################
# CREER UNE IMAGE DOCKER
# docker image build -t quiz-local-api .
# docker container run -it --rm -p 5000:5000 --name quiz-local-api quiz-local-api

# SUPPRIMER D'ANCIEN CONTAINER
# docker container ls -a
# docker container rm <nom-ou-id-des-containers>

# SUPPRIMER D'ANCIENNE IMAGE
# docker image ls
# docker image rm <nom-ou-id-des-images>

# SUPPRIMER UNE IMAGE ORPHELINE
# docker image prune

######################################## GIT ########################################
# git add .
# git commit -m "API flask Hello World"
# git push
