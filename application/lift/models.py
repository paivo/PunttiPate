from application import db
from application.models import Lift, Base
from sqlalchemy.sql import text
from flask_login import current_user
import os
from operator import itemgetter


class Gym(Base):
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    # Tietokannasta tietty sali id nimen perusteella.
    @staticmethod
    def find_one(name):
        stmt = text("SELECT Gym.id FROM Gym "
                    "WHERE Gym.name = :name ").params(name=name)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append(row[0])

        return response

    # Kaikki salit. Id ja salin nimi.
    @staticmethod
    def find_all():
        stmt = text("SELECT Gym.id, Gym.name FROM Gym "
                    "ORDER BY Gym.name")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id": row[0], "name": row[1]})

        return response

    # Kaikki salien nimet.
    @staticmethod
    def find_all_names():
        stmt = text("SELECT Gym.name FROM Gym "
                    "ORDER BY Gym.name")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append(row[0])

        return response

    # Käyttäjä kohtaiset salit. Id ja salin nimi.
    @staticmethod
    def find_gyms():
        stmt = text("SELECT Gym.id, Gym.name FROM Gym, Gym_User, Account "
                    "WHERE Account.id = :id "
                    "AND Account.id = Gym_User.account_id "
                    "AND Gym_User.gym_id = Gym.id "
                    "ORDER BY Gym.name").params(id=current_user.id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id": row[0], "name": row[1]})

        return response

    # Käyttäjä kohtaiset salit. Id, salin nimi ja milloin yhdistetty käyttäjään.
    @staticmethod
    def find_gyms_joined():
        stmt = text("SELECT Gym.id, Gym.name, Gym_User.date_created FROM Gym, Gym_User, Account "
                    "WHERE Account.id = :id "
                    "AND Account.id = Gym_User.account_id "
                    "AND Gym_User.gym_id = Gym.id "
                    "ORDER BY Gym_User.date_created DESC").params(id=current_user.id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id": row[0], "name": row[1], "date_created": row[2]})

        return response


class GymUser(Base):
    gym_id = db.Column(db.Integer, db.ForeignKey('gym.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, gym_id, account_id):
        self.gym_id = gym_id
        self.account_id = account_id

    # Kaikki yhdistetyt gym ja user id:t
    @staticmethod
    def find_all():
        stmt = text("SELECT Gym_User.gym_id, Gym_User.account_id FROM Gym_User")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"gym_id": row[0], "account_id": row[1]})

        return response

    # Poistetaan tietty yhteys käyttäjän ja gymin välillä.
    @staticmethod
    def delete(gym_id):
        stmt = text("DELETE FROM Gym_User WHERE gym_id = :gym_id AND account_id = :id"
                    ).params(gym_id=gym_id, id=current_user.id)
        db.engine.execute(stmt)


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
