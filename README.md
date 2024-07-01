# TP1-Intro
Repositorio para el trabajo practico 1 de la materia Introduccion al desarrollo de software
El trabajo fue el desarrollo en grupo de una página web, la idea principal es mostrar en qué plataformas está disponible una pelicula. 
Como complemento, en ella se tiene la posbilidad de agregar una reseña que consta de una puntuación (la máxima es de 5 estrellas) y un comentario de una pelicula ya vista.

------------Pasos para correr la pagina------------

instalación de requerimentos:
-pip install virtualenv

correr la pagina:
-sudo sytemctl start postgresql
*cargar la base de datos*
modificar  linea 11 del archivo app.py e intercambiar los campos  USUARIO, CONTRASEÑABD Y NOMBREBD: app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://USUARIO:CONTRASEÑABD@localhost:5432/NOMBREBD' por tu nombre de usuario postgresql, contraseña, y nombre de la base de datos respectivamente.

-cd /~/TP1-Intro
-virtualenv venv
-source venv/bin/activate
-pip install Flask
-pip install flask-cors
-pip install Flask-SQLAlchemy
-pip install psycopg2
-cd backend
-python3 app.py

--en otra terminal--

-cd /~/TP1-Intro/frontend
-python3 -m http.server

