from application import db
from application.models import Lift, Base
from sqlalchemy.sql import text
from flask_login import current_user
import os
from operator import itemgetter


class Bench(Lift):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, weight, date, public):
        self.weight = weight
        self.date = date
        self.public = public

    # Käyttäjäkohtaiset penkkitulokset tulostettavassa muodossa.
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

    # Paras julkinen penkki tulos per käyttäjä.
    @staticmethod
    def find_best():

        if os.environ.get("HEROKU"):
            stmt = text("SELECT DISTINCT ON (Account.username) Bench.weight, Bench.date, Account.username"
                        " FROM Bench, Account WHERE Bench.weight = ( SELECT MAX(Bench.weight)"
                        " FROM Bench WHERE Bench.public = '1' AND Bench.account_id = Account.id )")
        else:
            stmt = text("SELECT MAX(Bench.weight), Bench.date, Account.username FROM Bench, Account"
                        " WHERE Account.id = Bench.account_id"
                        " AND Bench.public = '1'"
                        " GROUP BY ( Account.username )"
                        " ORDER BY ( Bench.weight ) DESC LIMIT 30")

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"weight": row[0], "date": row[1], "name": row[2]})

        if os.environ.get("HEROKU"):
            response = sorted(response, key=itemgetter("weight"), reverse=True)

        return response


class Squat(Lift):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, weight, date, public):
        self.weight = weight
        self.date = date
        self.public = public

    # Käyttäjäkohtaiset kyykkytulokset tulostettavassa muodossa.
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


    # Paras julkinen kyykky tulos per käyttäjä
    @staticmethod
    def find_best():
        if os.environ.get("HEROKU"):
            stmt = text("SELECT DISTINCT ON (Account.username) Squat.weight, Squat.date, Account.username"
                        " FROM Squat, Account WHERE Squat.weight = ( SELECT MAX(Squat.weight) FROM Squat"
                        " WHERE Squat.public = '1' AND Squat.account_id = Account.id )")
        else:
            stmt = text("SELECT MAX(Squat.weight), Squat.date, Account.username FROM Squat, Account"
                        " WHERE Account.id = Squat.account_id"
                        " AND Squat.public = '1'"
                        " GROUP BY ( Account.username )"
                        " ORDER BY ( Squat.weight ) DESC LIMIT 30")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"weight": row[0], "date": row[1], "name": row[2]})
        if os.environ.get("HEROKU"):
            response = sorted(response, key=itemgetter("weight"), reverse=True)

        return response


class Dead(Lift):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, weight, date, public):
        self.weight = weight
        self.date = date
        self.public = public

    # Käyttäjäkohtaiset penkkitulokset tulostettavassa muodossa.
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

    # Paras julkinen maastaveto tulos per käyttäjä
    @staticmethod
    def find_best():
        if os.environ.get("HEROKU"):
            stmt = text("SELECT DISTINCT ON (Account.username) Dead.weight, Dead.date, Account.username"
                        " FROM Dead, Account WHERE Dead.weight = ( SELECT MAX(Dead.weight) FROM Dead"
                        " WHERE Dead.public = '1' AND Dead.account_id = Account.id )")
        else:
            stmt = text("SELECT MAX(Dead.weight), Dead.date, Account.username FROM Dead, Account"
                        " WHERE Account.id = Dead.account_id"
                        " AND Dead.public = '1'"
                        " GROUP BY ( Account.username )"
                        " ORDER BY ( Dead.weight ) DESC LIMIT 30")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"weight": row[0], "date": row[1], "name": row[2]})
        if os.environ.get("HEROKU"):
            response = sorted(response, key=itemgetter("weight"), reverse=True)

        return response
