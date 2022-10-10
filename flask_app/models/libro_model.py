from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import autor_model

class Libro:
	def __init__( self , data ):
		self.id = data['id']
		self.titulo = data['titulo']
		self.num_paginas = data['num_paginas']
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']
		self.autores_who_favorited = []

	@classmethod
	def get_all(cls):
		consulta = "SELECT * FROM libros;"
		results = connectToMySQL('esquema_libros').query_db(consulta)
		libros = []
		for libro_model in results:
			libros.append( cls(libro_model) )
		return libros

	@classmethod
	def save(cls, data ):
		query = "INSERT INTO libros ( titulo , num_paginas , created_at, updated_at) VALUES ( %(titulo)s , %(num_paginas)s , NOW() , NOW());"
		return connectToMySQL('esquema_libros').query_db( query, data )


	@classmethod
	def get_by_id(cls,data):
		query = "SELECT * FROM libros LEFT JOIN favoritos ON libros.id = favoritos.libro_id LEFT JOIN autores ON autores.id = favoritos.autor_id WHERE libros.id = %(id)s;"
		results = connectToMySQL('esquema_libros').query_db(query,data)

		libro = cls(results[0])

		for row in results:
			if row['autores.id'] == None:
				break
			data = {
				"id": row['autores.id'],
				"nombre": row['nombre'],
				"created_at": row['autores.created_at'],
				"updated_at": row['autores.updated_at']
			}
			libro.autores_who_favorited.append(autor_model.Autor(data))
		return libro

	@classmethod
	def unfavorited_libros(cls,data):
		query = "SELECT * FROM libros WHERE libros.id NOT IN ( SELECT libro_id FROM favoritos WHERE autor_id = %(id)s );"
		results = connectToMySQL('esquema_libros').query_db(query,data)
		libros = []
		for row in results:
			libros.append(cls(row))
		print(libros)
		return libros