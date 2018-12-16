from application import db
from application.models import Base
from sqlalchemy.sql import text
from flask_login import current_user


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

    # Kolme suosituinta salia
    @staticmethod
    def top():
        stmt = text("SELECT Gym.name, COUNT(Account.name) FROM Gym, Gym_User, Account "
                    "WHERE Account.id = Gym_User.account_id "
                    "AND Gym_User.gym_id=Gym.id "
                    "GROUP BY Gym.name "
                    "ORDER BY COUNT(Account.name) DESC LIMIT 3")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"name": row[0], "count": row[1]})

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
