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