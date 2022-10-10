from flask import render_template,redirect,request,session,flash

from flask_app.models.autor_model import Autor
from flask_app.models.libro_model import Libro
from flask_app import app


@app.route('/')
def index():
	return redirect('/autores')

#RUTA DE LECTURA
@app.route('/autores')
def dojos():
	return render_template("autores.html", autores=Autor.get_all())

#RUTA DE CREACION
@app.route('/crearautor', methods=['POST'])
def crearautor():
	data = {
		"nombre" : request.form['a_nombre']
	}
	autor_id = Autor.save(data)
	return redirect('/autores')

@app.route('/autor/<int:id>')
def show_autor(id):
	data = {
		"id": id
	}
	return render_template('vista_autor.html',autor=Autor.get_by_id(data),unfavorited_libros=Libro.unfavorited_libros(data))

@app.route('/join/libro',methods=['POST'])
def join_libro():
	data = {
		'autor_id': request.form['autor_id'],
		'libro_id': request.form['libro_id']
	}
	Autor.add_favorito(data)
	return redirect(f"/autor/{request.form['autor_id']}")