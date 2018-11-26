from application import db
from application.models import Lift


class Bench(Lift):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, weight, date):
        self.weight = weight
        self.date = date


class Squat(Lift):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, weight, date):
        self.weight = weight
        self.date = date


class Dead(Lift):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, weight, date):
        self.weight = weight
        self.date = date
