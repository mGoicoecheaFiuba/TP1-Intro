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

# Ruta para obtener todas las peliculas o filtradas por el buscador
@app.route('/peliculas', methods=['GET'])
def mostar_peliculas():
    try:
        #Setea el valor del input de busqueda, si no hay es = None
        buscar = request.args.get('buscar', None)

        if buscar:
            peliculas = Pelicula.query.filter(or_(Pelicula.titulo.ilike(f'%{buscar}%')))
            #or_ permite aplicar condiciones de filtro, ilike realiza la busqueda(insensible a may y min)
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
            'plataformas': [plataforma.nombre for plataforma in peli.plataformas] #se usa la tabla relacional
        } for peli in peliculas]

        return jsonify(respuesta)
    except Exception as error:
        print("Error", error)
        return jsonify({"mensaje": "error interno del servidor"}), 500  

# Ruta para obtener una pelicula por id
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


# Ruta para obtener la info de las plataformas
@app.route('/plataformas', methods=['GET'])
def obtener_plataformas():
    try:
        plataformas = Plataforma.query.all()
        respuesta = [{
            'id': plataforma.id,
            'nombre': plataforma.nombre,
            'imagen': plataforma.imagen
        } for plataforma in plataformas]
        return jsonify(respuesta)
    except Exception as error:
        print("Error: ", error)
        return jsonify({"mensaje": "error interno del servidor"}), 500


# Ruta para obtener la info de las pelis filtradas por plataformas
@app.route("/plataformas/<int:id_plataforma>/peliculas", methods=["GET"])
def peliculas_por_plataforma(id_plataforma):
    try:
        plataforma = Plataforma.query.get(id_plataforma)

        if not plataforma:
            return jsonify({'mensaje': 'Plataforma no encontrada'}), 404

        peliculas = plataforma.peliculas.all()
        respuesta = [{
            'id': pelicula.id,
            'titulo': pelicula.titulo,
            'sinopsis': pelicula.sinopsis,
            'estreno': pelicula.estreno,
            'director': pelicula.director,
            'genero': pelicula.genero,
            'imagen': pelicula.imagen
        } for pelicula in peliculas]

        return jsonify(respuesta)

    except Exception as error:
        print("Error: ", error)
        return jsonify({"mensaje": "error interno del servidor"}), 500


# Ruta para agregar una opinion
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
       #los siguientes renglones solucionan los problemas de CORS
       respuesta = make_response(jsonify({'mensaje': 'Reseña creada exitosamente'}))
       respuesta.headers['Access-Control-Allow-Origin'] = '*'  # Permite solicitudes de cualquier origen 

       return respuesta
   except Exception as error:
       print("Error: ", error)
       return jsonify({"mensaje": "error interno del servidor"}), 500


# Ruta para obtener todas las opiniones
@app.route('/opiniones', methods=['GET'])
def mostrar_opiniones():
  try:
      opiniones = Opinion.query.all()
      peliculas = Pelicula.query.all()
      respuesta = [{
          'id': opinion.id,
          'titulo_pelicula': Pelicula.query.filter_by(id=opinion.pelicula_id).first().titulo, #esto es un JOIN de tabla opinion y tabla pelicula
          'pelicula_id': opinion.pelicula_id,
          'valoracion': opinion.valoracion,
          'comentario': opinion.comentario
      } for opinion in opiniones]

      return jsonify(respuesta)
  except Exception as error:
      print("Error: ", error)
      return jsonify({"mensaje": "error interno del servidor"}), 500




# Ruta para eliminar una opinion
@app.route('/opiniones/<id_opinion>', methods=['DELETE'])
def eliminar_opinion(id_opinion):
   try:
       opinion = Opinion.query.get(id_opinion)
       if not opinion:
           return jsonify({'mensaje': 'Opinion no encontrada'}), 404
       db.session.delete(opinion)
       db.session.commit()
       return jsonify({'mensaje': 'Opinion eliminada exitosamente'})
   except Exception as error:
       print("Error: ", error)
       return jsonify({"mensaje": "error interno del servidor"}), 500


# Ruta para editar una opinion
@app.route('/opinion/<id_opinion>', methods=['PUT'])
def editar_opinion(id_opinion):
   datos = request.json
   opinion = Opinion.query.get(id_opinion)

    # Cambia los valores del elemento opinion
   setattr(opinion, 'pelicula_id', datos['pelicula_id'])
   setattr(opinion, 'valoracion', datos['valoracion'])
   setattr(opinion, 'comentario',datos['comentario'])

   db.session.add(opinion)
   db.session.commit()
   respuesta = make_response(jsonify({'mensaje': 'Reseña creada exitosamente'}))
   respuesta.headers['Access-Control-Allow-Origin'] = '*'

   return jsonify({'mensaje': 'Opinion actualizada exitosamente'})



# Ruta para obtener una opinion
@app.route('/opiniones/<id_opinion>', methods=['GET'])
def mostar_opinion(id_opinion):
   try:
       opinion = Opinion.query.get(id_opinion)
       pelicula = Pelicula.query.get(opinion.pelicula_id)
       if not opinion:
           return jsonify({'mensaje': 'Opinion no encontrada'}), 404
       return jsonify({
           'id': opinion.id,
           'titulo':Pelicula.query.filter_by(id=opinion.pelicula_id).first().titulo, #otro JOIN
           'valoracion': opinion.valoracion,
           'comentario': opinion.comentario,
           'imagen': pelicula.imagen
       })
   except Exception as error:
       print("Error: ", error)
       return jsonify({"mensaje": "error interno del servidor"}), 500




if __name__ == '__main__':
   with app.app_context():
       db.create_all()
       print("Base de datos creada y tablas inicializadas")
   app.run(host='0.0.0.0', debug=True, port=port)


