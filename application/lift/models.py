from application import db
from application.models import Lift
from sqlalchemy.sql import text
from flask_login import current_user


class Bench(Lift):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, weight, date, public):
        self.weight = weight
        self.date = date
        self.public = public

    @staticmethod
    def find_lifts():
        stmt = text("SELECT Bench.weight, Bench.date, Bench.public, Bench.id FROM Bench"
                    " WHERE Bench.account_id = :id"
                    " ORDER BY Bench.weight DESC").params(id=current_user.id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            if row[2]:
                response.append({"weight": row[0], "date": row[1], "public": "Yes", "id": row[3]})
            else:
                response.append({"weight": row[0], "date": row[1], "public": "No", "id": row[3]})

        return response


class Squat(Lift):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, weight, date, public):
        self.weight = weight
        self.date = date
        self.public = public

    @staticmethod
    def find_lifts():
        stmt = text("SELECT Squat.weight, Squat.date, Squat.public, Squat.id FROM Squat"
                    " WHERE Squat.account_id = :id"
                    " ORDER BY Squat.weight DESC").params(id=current_user.id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            if row[2]:
                response.append({"weight": row[0], "date": row[1], "public": "Yes", "id": row[3]})
            else:
                response.append({"weight": row[0], "date": row[1], "public": "No", "id": row[3]})

        return response


class Dead(Lift):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, weight, date, public):
        self.weight = weight
        self.date = date
        self.public = public

    @staticmethod
    def find_lifts():
        stmt = text("SELECT Dead.weight, Dead.date, Dead.public, Dead.id FROM Dead"
                    " WHERE Dead.account_id = :id"
                    " ORDER BY Dead.weight DESC").params(id=current_user.id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            if row[2]:
                response.append({"weight": row[0], "date": row[1], "public": "Yes", "id": row[3]})
            else:
                response.append({"weight": row[0], "date": row[1], "public": "No", "id": row[3]})

        return response
