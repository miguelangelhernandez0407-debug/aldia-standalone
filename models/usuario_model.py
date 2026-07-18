import hashlib
from database.connection import obtener_conexion

class UsuarioModel:

    def obtener_todos(self):
        conexion = obtener_conexion()
        usuarios = []
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, apellido, correo, telefono, activo FROM usuario")
            usuarios = cursor.fetchall()
            cursor.close()
            conexion.close()
        return usuarios

    def insertar(self, nombre, apellido, nombre_usuario, correo, contrasena, num_documento, telefono):
        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """INSERT INTO usuario (nombre, apellido, nombre_usuario, correo, contrasena, num_documento, telefono)
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (nombre, apellido, nombre_usuario, correo, contrasena_hash, num_documento, telefono))
                conexion.commit()
            finally:
                cursor.close()
                conexion.close()

    def actualizar(self, id, nombre, apellido, correo, telefono):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "UPDATE usuario SET nombre=%s, apellido=%s, correo=%s, telefono=%s WHERE id=%s"
                cursor.execute(sql, (nombre, apellido, correo, telefono, id))
                conexion.commit()
            finally:
                cursor.close()
                conexion.close()

    def eliminar(self, id):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM usuario WHERE id=%s", (id,))
                conexion.commit()
            finally:
                cursor.close()
                conexion.close()