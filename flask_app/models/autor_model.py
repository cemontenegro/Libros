from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import libro_model

class Autor:
	def __init__(self,data):
		self.id = data['id']
		self.nombre= data['nombre']
		self.favorite_books = []
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']
		self.favorito_libros = []

	#METODO PARA CREAR
	@classmethod
	def save(cls,data):
		consulta = "Insert INTO autores (nombre,created_at,updated_at) VALUES(%(nombre)s,NOW(),NOW());"
		return connectToMySQL('esquema_libros').query_db(consulta,data)

	#METODO DE LECTURA
	@classmethod
	def get_all(cls):
		consulta = "SELECT * FROM autores;"
		autores_from_db = connectToMySQL('esquema_libros').query_db(consulta)
		autores = []
		for b in autores_from_db:
			autores.append(cls(b))
		return autores

	@classmethod
	def get_one(cls, id):
		consulta = "SELECT * FROM autores WHERE id = %(id)s;"
		data = connectToMySQL('esquema_libros').query_db(consulta, {"id": id})
		return cls(data[0])

#NUEVO

	@classmethod
	def unfavorited_autores(cls,data):
		query = "SELECT * FROM autores WHERE autores.id NOT IN ( SELECT autor_id FROM favoritos WHERE libro_id = %(id)s );"
		autores = []
		results = connectToMySQL('esquema_libros').query_db(query,data)
		for row in results:
			autores.append(cls(row))
		return autores

	@classmethod
	def add_favorito(cls,data):
		query = "INSERT INTO favoritos (autor_id,libro_id) VALUES (%(autor_id)s,%(libro_id)s);"
		return connectToMySQL('esquema_libros').query_db(query,data);


	@classmethod
	def get_by_id(cls,data):
		query = "SELECT * FROM autores LEFT JOIN favoritos ON autores.id = favoritos.autor_id LEFT JOIN libros ON libros.id = favoritos.libro_id WHERE autores.id = %(id)s;"
		results = connectToMySQL('esquema_libros').query_db(query,data)

		# Creates instance of author object from row one
		autor = cls(results[0])
		# append all book objects to the instances favorites list.
		for row in results:
			# if there are no favorites
			if row['libros.id'] == None:
				break
			# common column names come back with specific tables attached
			data = {
				"id": row['libros.id'],
				"titulo": row['titulo'],
				"num_paginas": row['num_paginas'],
				"created_at": row['libros.created_at'],
				"updated_at": row['libros.updated_at']
			}
			autor.favorito_libros.append(libro_model.Libro(data))
		return autor
