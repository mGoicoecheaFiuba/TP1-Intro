from flask import Flask, jsonify, request
from models import db, Pelicula, Plataforma, Opinion, peliculas_plataformas
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://joaco:joaco2005@localhost:5432/peliculas_web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/peliculas', methods=['GET'])
def mostar_peliculas():
    peliculas = Pelicula.query.all()
    respuesta = []
    try:
        for peli in peliculas:
            respuesta.append({
                'id': peli.id,
                'titulo': peli.titulo,
                'sinopsis': peli.sinopsis,
                'estreno': peli.estreno,
                'director': peli.director,
                'genero': peli.genero,
                'imagen': peli.imagen,
                'plataformas': [plataforma.nombre for plataforma in peli.plataformas]
            })
    except Exception as error:
        print("error: " + str(error))
    return jsonify(respuesta)

@app.route('/peliculas/<id_pelicula>', methods=['GET'])
def mostrar_pelicula(id_pelicula):
    pelicula = Pelicula.query.get(id_pelicula)
    if not pelicula:
        return jsonify({'mensaje': 'Pelicula no encontrada'}), 404

    return jsonify({
        'id': pelicula.id,
        'titulo': pelicula.titulo,
        'sinopsis': pelicula.sinopsis,
        'estreno': pelicula.estreno,
        'director': pelicula.director,
        'genero': pelicula.genero,
        'imagen': pelicula.imagen,
        'plataformas': [plataforma.nombre for plataforma in pelicula.plataformas]
    })


@app.route('/agregar_plataforma', methods=['POST'])
def agregar_plataforma():
    nombre = request.json.get('nombre')
    imagen = request.json.get('imagen')

    if not nombre:
        return jsonify({'mensaje': 'El nombre de la plataforma es requerido'}), 400

    plataforma = Plataforma(nombre=nombre, imagen=imagen)
    db.session.add(plataforma)
    db.session.commit()

    return jsonify({'mensaje': 'Plataforma agregada correctamente'}), 201

@app.route('/agregar_pelicula', methods=['POST'])
def agregar_pelicula():
    titulo = request.json.get('titulo')
    sinopsis = request.json.get('sinopsis')
    estreno = request.json.get('estreno')
    director = request.json.get('director')
    genero = request.json.get('genero')
    plataformas_ids = request.json.get('plataformas')  
    imagen = request.json.get('imagen')

    if not (titulo and sinopsis and estreno and director and genero and plataformas_ids):
        return jsonify({'mensaje': 'Todos los campos son requeridos'}), 400

    pelicula = Pelicula(
        titulo=titulo,
        sinopsis=sinopsis,
        estreno=estreno,
        director=director,
        genero=genero,
        imagen=imagen
    )

    for plataforma_id in plataformas_ids:
        plataforma = Plataforma.query.get(plataforma_id)
        if plataforma:
            pelicula.plataformas.append(plataforma)

    db.session.add(pelicula)
    db.session.commit()

    return jsonify({'mensaje': 'Pelicula agregada correctamente'}), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Base de datos creada y tablas inicializadas")
    app.run(host='0.0.0.0', debug=True, port=port)