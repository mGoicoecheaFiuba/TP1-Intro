from flask import Flask 
from models import db, Pelicula, Plataforma, Opinion

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://marianogico:mingo21@localhost:5432/movies_web_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


@app.route('/')
def hello_world():
    return 'Hello world!'

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("Base de datos creada y tablas inicia lizadas")
    app.run(host='0.0.0.0', debug=True, port=port)