from flask import Flask, jsonify, request, Response, make_response
from models import db, Pelicula, Plataforma, Opinion, peliculas_plataformas
from flask_cors import CORS, cross_origin
from sqlalchemy import or_

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://marianogoico:mingo21@localhost:5432/movies_web_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/peliculas', methods=['GET'])
def mostar_peliculas():
    try:
        buscar = request.args.get('buscar', None)

        if buscar:
            peliculas = Pelicula.query.filter(or_(Pelicula.titulo.ilike(f'%{buscar}%')))
        else:
            peliculas = Pelicula.query.all()

        respuesta = [{
            'id': peli.id,
            'titulo': peli.titulo,
            'sinopsis': peli.sinopsis,
            'estreno': peli.estreno,
            'director': peli.director,
            'genero': peli.genero,
            'imagen': peli.imagen,
            'plataformas': [plataforma.nombre for plataforma in peli.plataformas]
        } for peli in peliculas]

        return jsonify(respuesta)
    except Exception as error:
        print("Error", error)
        return jsonify({"mensaje": "error interno del servidor"}), 500  


@app.route('/peliculas/<id_pelicula>', methods=['GET'])
def mostrar_pelicula(id_pelicula):
    try:
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
    except Exception as error:
        print("Error: ", error)
        return jsonify({"mensaje": "error interno del servidor"}), 500 


@app.route('/plataformas', methods=['GET'])
def obtener_plataformas():
    try:
        plataformas = Plataforma.query.all()
        respuesta = [{
            'id': plataforma.id,
            'nombre': plataforma.nombre
        } for plataforma in plataformas]
        return jsonify(respuesta)
    except Exception as error:
        print("Error: ", error)
        return jsonify({"mensaje": "error interno del servidor"}), 500

@app.route("/plataformas/<int:id_plataforma>/peliculas", methods=["GET"])
def peliculas_por_plataforma(id_plataforma):
    try:
        plataforma = Plataforma.query.get(id_plataforma)

        if not plataforma:
            return jsonify({'mensaje': 'Plataforma no encontrada'}), 404

        peliculas = plataforma.peliculas.all()
        respuesta = [{
            'id': peli.id,
            'titulo': peli.titulo,
            'sinopsis': peli.sinopsis,
            'estreno': peli.estreno,
            'director': peli.director,
            'genero': peli.genero,
            'imagen': peli.imagen
        } for peli in peliculas]

        return jsonify(respuesta)

    except Exception as error:
        print("Error: ", error)
        return jsonify({"mensaje": "error interno del servidor"}), 500


@app.route('/opinion', methods=['POST'])
def hacer_reseña():
    try:
        datos = request.json
        nueva_reseña = Opinion(
            pelicula_id=datos['pelicula_id'],
            valoracion=datos['valoracion'],
            comentario=datos['comentario']
        )
        db.session.add(nueva_reseña)
        db.session.commit()
        respuesta = make_response(jsonify({'mensaje': 'Reseña creada exitosamente'}))
        respuesta.headers['Access-Control-Allow-Origin'] = '*'  # Permite solicitudes de cualquier origen
        return respuesta
    except Exception as error:
        print("Error: ", error)
        return jsonify({"mensaje": "error interno del servidor"}), 500


@app.route('/opiniones', methods=['GET'])
def mostrar_opiniones():
    try:
        opiniones = Opinion.query.all()
        respuesta = [{
            'id': opinion.id,
            'pelicula_id': opinion.pelicula_id,
            'valoracion': opinion.valoracion,
            'comentario': opinion.comentario
        } for opinion in opiniones]

        return jsonify(respuesta)
    except Exception as error:
        print("Error: ", error)
        return jsonify({"mensaje": "error interno del servidor"}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Base de datos creada y tablas inicializadas")
    app.run(host='0.0.0.0', debug=True, port=port)
