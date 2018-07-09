# models.py

from app import db


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(2))
    name = db.Column(db.String(50))


class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    customer = db.Column(db.Boolean())
    engineering = db.Column(db.Boolean())
    extra = db.Column(db.String(400))
