from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# tabla intermedia entre peliculas y plataformas
peliculas_plataformas = db.Table('peliculas_plataformas',
    db.Column('pelicula_id', db.Integer, db.ForeignKey('peliculas.id'), primary_key=True),
    db.Column('plataforma_id', db.Integer, db.ForeignKey('plataformas.id'), primary_key=True)
)

class Pelicula(db.Model):
    __tablename__ = 'peliculas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    sinopsis = db.Column(db.String(255), nullable=False)
    estreno = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(255), nullable=False)
    genero = db.Column(db.String(255), nullable=False)
    # relacion con plataformas
    plataformas = db.relationship('Plataforma', secondary=peliculas_plataformas, backref=db.backref('peliculas', lazy='dynamic'))
    imagen = db.Column(db.String(255))

class Plataforma(db.Model):
    __tablename__ = 'plataformas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    imagen = db.Column(db.String(255))

class Opinion(db.Model):
    __tablename__ = 'opiniones'
    id = db.Column(db.Integer, primary_key=True)
    pelicula_id = db.Column(db.Integer, db.ForeignKey('peliculas.id'))
    valoracion = db.Column(db.Integer)
    comentario = db.Column(db.String(255), nullable=False)
