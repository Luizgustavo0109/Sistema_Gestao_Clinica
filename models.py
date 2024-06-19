from flask_sqlalchemy import SQLAlchemy
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    sexo = db.Column(db.String(10))
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    data_hora = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    paciente = db.relationship('Paciente', backref=db.backref('consultas', lazy=True))
