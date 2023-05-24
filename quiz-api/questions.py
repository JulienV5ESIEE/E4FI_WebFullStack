import sqlite3, json, sys

#Récupérer le token envoyé en paramètre
#request.headers.get('Authorization')

#récupèrer un l'objet json envoyé dans le body de la requète
#request.get_json()

# Cette classe correspond au modèle de données d'une question
class Question:
    def __init__(self, id, text, title, image, position, possible_answers):
        self.id = id
        self.text = text
        self.title = title
        self.image = image
        self.position = position
        self.possible_answers = possible_answers

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'title': self.title,
            'image': self.image,
            'position': self.position,
            'possibleAnswers': self.possible_answers
        }

class PossibleAnswer:
    def __init__(self, id, text, isCorrect):
        self.id = id
        self.text = text
        self.isCorrect = isCorrect

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'isCorrect': self.isCorrect
        }

# Cette fonction permet d'insérer une nouvelle question dans la base de données
def add_question(question):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    print(question, file=sys.stdout)
    
    # Vérifier si la position est déjà prise
    cursor.execute("SELECT COUNT(*) FROM questions WHERE position=?", (question['position'],))
    row = cursor.fetchone()
    count = row[0]
    
    # Si la position est déjà prise, décaler les questions suivantes
    if count > 0:
        cursor.execute("UPDATE questions SET position = position + 1 WHERE position >= ?", (question['position'],))

    # Ajouter la nouvelle question à la position demandée
    cursor.execute("INSERT INTO questions (text, title, image, position) VALUES (?, ?, ?, ?)", (
        question['text'], question['title'], question['image'], question['position']))
    question_id = cursor.lastrowid
    for answer in question['possibleAnswers']:
        cursor.execute("INSERT INTO possible_answers (text, isCorrect, question_id) VALUES (?, ?, ?)", (
            answer['text'], answer['isCorrect'], question_id))
    connection.commit()
    connection.close()
    return question_id

def remove_question(question_id):
    question = get_question_by_id(question_id)
    if question is not None:
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM possible_answers WHERE question_id=?', (question.id,))
        cursor.execute('DELETE FROM questions WHERE id=?', (question_id,))
        cursor.execute("SELECT * FROM questions WHERE position>?", (question.position,))
        allquestionstosplit = cursor.fetchall()
        print(allquestionstosplit, file=sys.stdout)
        for question in allquestionstosplit:
            cursor.execute("UPDATE questions SET position = position - 1 WHERE id=?", (question[0],))
        connection.commit()
        connection.close()
        return question_id
    else:
        return None
     
def remove_all_questions():
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM possible_answers')
    cursor.execute('DELETE FROM questions')
    connection.commit()
    connection.close()

# Cette fonction permet de récupérer une question à partir de son identifiant
def get_question_by_id(question_id):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM questions WHERE id=?', (question_id,))
    question_data = cursor.fetchone()

    if question_data is not None:
        cursor.execute('SELECT * FROM possible_answers WHERE question_id=?', (question_id,))
        possible_answers_data = cursor.fetchall()
        answers = []
        for i in possible_answers_data:
            answer = {
                'text': i[1],
                'isCorrect': bool(i[2])
            }
            answers.append(answer)
        return Question(id=question_data[0], text=question_data[1], title=question_data[2], image=question_data[3], position=question_data[4], possible_answers=answers)
    else:
        return None

# Cette fonction permet de récupérer une question à partir de sa position dans le quiz
def get_question_by_position(position):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM questions WHERE position=?', (position,))
    question_data = cursor.fetchone()

    if question_data is not None:
        cursor.execute('SELECT * FROM possible_answers WHERE question_id=?', (question_data[0],))
        possible_answers_data = cursor.fetchall()
        answers = []
        for i in possible_answers_data:
            answer = {
                'text': i[1],
                'isCorrect': bool(i[2])
            }
            answers.append(answer)
        return Question(id=question_data[0], text=question_data[1], title=question_data[2], image=question_data[3], position=question_data[4], possible_answers=answers)
    else:
        return None
     
# Cette fonction permet de mettre à jour une question à partir de son id dans le quiz
# print(question[1], file=sys.stdout)
def update_question(question_id, question_data):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM questions WHERE id=?', (question_id,))
    existing_question = cursor.fetchone()
    if existing_question is not None:
        question_position = int(existing_question[4])
        print(question_position, file=sys.stdout)
        print(question_data['position'], file=sys.stdout)
        if question_position != question_data['position']:
            cursor.execute('SELECT * FROM questions WHERE position=?', (question_data['position'],))
            firstquestion = cursor.fetchone()
            # On récupère toutes les questions
            
            if(int(question_data['position']) < int(question_position)): # Si on descends la question dans les positions
                cursor.execute('SELECT * FROM questions WHERE position>=? AND position<=?', (firstquestion[0],question_position,))
            else:
                cursor.execute('SELECT * FROM questions WHERE position>? AND position<=?', (question_position,question_data['position'],))
            all_questions = cursor.fetchall()
            for question in all_questions:
                if(int(question_data['position']) < int(question_position)): # Si on descends la question dans les positions
                    print(question[1], file=sys.stdout)
                    cursor.execute("UPDATE questions SET position = position + 1 WHERE id=?", (question[0],))
                else:
                    cursor.execute("UPDATE questions SET position = position - 1 WHERE id=?", (question[0],))
        
            # On update la question en question
            cursor.execute("UPDATE questions SET text=?, title=?, image=?, position = ? WHERE id=?", (
                question_data['text'],question_data['title'],question_data['image'],question_data['position'],question_id,))
 
        cursor.execute('DELETE FROM possible_answers WHERE question_id=?', (question_id,))
        for answer in question_data['possibleAnswers']:
            print(answer['text'], file=sys.stdout)
            print(answer['isCorrect'], file=sys.stdout)
            print(question_id, file=sys.stdout)
            cursor.execute('INSERT INTO possible_answers (text, isCorrect, question_id) VALUES (?, ?, ?)', (
                answer['text'], answer['isCorrect'], question_id))
        
        connection.commit()
        connection.close()
        return question_position
    else:
        return None
    
    
    
def get_all_questions():
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM questions ORDER BY position ASC")
        all_questions = cursor.fetchall()
        questions = []
        for question in all_questions:
            cursor.execute("SELECT * FROM possible_answers WHERE question_id=?", (question[0],))
            possible_answers = cursor.fetchall()
            possible_answers_list = []
            for answer in possible_answers:
                possible_answers_list.append({
                    'id': answer[0],
                    'text': answer[1],
                    'isCorrect': answer[2]
                })
            questions.append({
                'id': question[0],
                'text': question[1],
                'title': question[2],
                'image': question[3],
                'position': question[4],
                'possibleAnswers': possible_answers_list
            })
    except Exception as e:
        raise e
    finally:
        connection.close()
    return questions
