from database.connection import obtener_conexion

class InmuebleModel:

    def obtener_todos(self):
        conexion = obtener_conexion()
        inmuebles = []
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT i.id, i.direccion, i.ciudad, i.tipo, i.activo,
                       u.nombre, u.apellido
                FROM inmueble i
                JOIN usuario u ON i.propietario_id = u.id
            """)
            inmuebles = cursor.fetchall()
            cursor.close()
            conexion.close()
        return inmuebles

    def insertar(self, direccion, ciudad, departamento, tipo, descripcion, propietario_id):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            sql = """INSERT INTO inmueble (direccion, ciudad, departamento, tipo, descripcion, propietario_id)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (direccion, ciudad, departamento, tipo, descripcion, propietario_id))
            conexion.commit()
            cursor.close()
            conexion.close()

    def actualizar(self, id, direccion, ciudad, tipo, descripcion):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            sql = "UPDATE inmueble SET direccion=%s, ciudad=%s, tipo=%s, descripcion=%s WHERE id=%s"
            cursor.execute(sql, (direccion, ciudad, tipo, descripcion, id))
            conexion.commit()
            cursor.close()
            conexion.close()

    def eliminar(self, id):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM inmueble WHERE id=%s", (id,))
            conexion.commit()
            cursor.close()
            conexion.close()