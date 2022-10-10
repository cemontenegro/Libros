from flask import render_template,redirect,request,session,flash
from flask_app.models.autor_model import Autor
from flask_app.models.libro_model import Libro

from flask_app import app

@app.route('/libros', methods=["GET"])
def formulario_libro():
	return render_template("libros.html", todos_autores=Autor.get_all(), todos_libros=Libro.get_all())

@app.route('/crearlibro', methods=["POST"])
def crearlibro():
	data = {
		"titulo": request.form["titulo"],
		"num_paginas" : request.form["num_paginas"],
	}
	libro_id = Libro.save(data)
	return redirect('/libros')

@app.route('/libro/<int:id>')
def show_libro(id):
	data = {
		"id":id
	}
	return render_template('vista_libro.html',libro=Libro.get_by_id(data),unfavorited_autores=Autor.unfavorited_autores(data))

@app.route('/join/autor',methods=['POST'])
def join_autor():
	data = {
		'autor_id': request.form['autor_id'],
		'libro_id': request.form['libro_id']
	}
	Autor.add_favorito(data)
	return redirect(f"/libro/{request.form['libro_id']}")