# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27561f2b6176a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test3.db'

db = SQLAlchemy(app)
