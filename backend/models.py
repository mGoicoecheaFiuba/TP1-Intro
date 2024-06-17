from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

class pelicula(db.Model):
    __tablename__= 'peliculas'
    id= db.Column(db.Integer, primary_key=True)
    titulo= db.Column(db.String(255), nullable= False)
    sinopsis= db.Column(db.String(255), nullable= False)
    estreno= db.Column(db.String(255), nullable=False)
    director= db.Column(db.String(255), nulable=False)
    genero= db.Column(db.String(255), nulable=False)
    plataforma_id= db.Column(db.Integer, db.ForeignKey)
    imagen= db.Column(db.String(255))

class plataforma(db.Model):
    __tablename__= 'plataformas'
    id= db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(255), nullable= False)
    imagen= db.Column(db.String(255))

class opinion(db.Model):
    __tablename__= 'opiniones'
    id= db.Column(db.Integer, primary_key=True)
    pelicula_id= db.Column(db.Integer, db.ForeignKey)
    valoracion= db.Column(db.Integer)
    comentario= db.Column(db.String(255), nullable= False)