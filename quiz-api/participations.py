import sqlite3, json, sys

class Participation:
    def __init__(self,id,name,score):
        self.id = id
        self.name = name
        self.score = score

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'score': self.score
        }
        
        
def participation_add(name, score):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO participations (name, score) VALUES (?, ?)", (name, score))
    connection.commit()
    connection.close()
    return score


def participation_remove_all():
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM participations")
    connection.commit()
    connection.close()
    return 200


def get_position_score(playerName, score):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    
    # Récupérer la position de la participation demandée
    cursor.execute("SELECT * FROM participations WHERE name=? AND score=? LIMIT 1", (playerName, score))
    requested_participation = cursor.fetchone()
    
    # Récupérer la participation précédente
    cursor.execute("SELECT * FROM participations WHERE score < ? ORDER BY score DESC LIMIT 1", (score,))
    previous_participation = cursor.fetchone()
    
    # Récupérer la participation suivante
    cursor.execute("SELECT * FROM participations WHERE score > ? ORDER BY score ASC LIMIT 1", (score,))
    next_participation = cursor.fetchone()
    
    connection.commit()
    connection.close()
    
    return requested_participation, previous_participation, next_participation