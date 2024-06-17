from flask import Flask, jsonify, request
from models import db, Pelicula, Plataforma, Opinion

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://marianogoico:mingo21@localhost:5432/movies_web_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#ruta para agregar una plataforma
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

#ruta para agregar una película
@app.route('/agregar_pelicula', methods=['POST'])
def agregar_pelicula():
    titulo = request.json.get('titulo')
    sinopsis = request.json.get('sinopsis')
    estreno = request.json.get('estreno')
    director = request.json.get('director')
    genero = request.json.get('genero')
    plataforma_id = request.json.get('plataforma_id')
    imagen = request.json.get('imagen')

    if not (titulo and sinopsis and estreno and director and genero and plataforma_id):
        return jsonify({'mensaje': 'Todos los campos son requeridos'}), 400

    pelicula = Pelicula(
        titulo=titulo,
        sinopsis=sinopsis,
        estreno=estreno,
        director=director,
        genero=genero,
        plataforma_id=plataforma_id,
        imagen=imagen
    )

    db.session.add(pelicula)
    db.session.commit()

    return jsonify({'mensaje': 'Película agregada correctamente'}), 201

# ruta de prueba
@app.route('/')
def hello_world():
    return 'Hello world!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Base de datos creada y tablas inicializadas")
    app.run(host='0.0.0.0', debug=True, port=port)