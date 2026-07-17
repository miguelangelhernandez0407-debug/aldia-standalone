from database.connection import obtener_conexion

class ContratoModel:

    def obtener_todos(self):
        conexion = obtener_conexion()
        contratos = []
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.id, c.valor_mensual, c.dia_pago, c.fecha_inicio, c.fecha_fin, c.estado,
                       i.direccion, i.ciudad,
                       u1.nombre AS nombre_arrendador, u1.apellido AS apellido_arrendador,
                       u2.nombre AS nombre_arrendatario, u2.apellido AS apellido_arrendatario
                FROM contrato c
                JOIN inmueble i ON c.inmueble_id = i.id
                JOIN usuario u1 ON c.arrendador_id = u1.id
                JOIN usuario u2 ON c.arrendatario_id = u2.id
            """)
            contratos = cursor.fetchall()
            cursor.close()
            conexion.close()
        return contratos

    def insertar(self, inmueble_id, arrendador_id, arrendatario_id, valor_mensual, dia_pago, fecha_inicio, fecha_fin, estado, observaciones):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            sql = """INSERT INTO contrato (inmueble_id, arrendador_id, arrendatario_id, valor_mensual, dia_pago, fecha_inicio, fecha_fin, estado, observaciones)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (inmueble_id, arrendador_id, arrendatario_id, valor_mensual, dia_pago, fecha_inicio, fecha_fin, estado, observaciones))
            conexion.commit()
            cursor.close()
            conexion.close()

    def actualizar(self, id, valor_mensual, dia_pago, fecha_fin, estado, observaciones):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            sql = "UPDATE contrato SET valor_mensual=%s, dia_pago=%s, fecha_fin=%s, estado=%s, observaciones=%s WHERE id=%s"
            cursor.execute(sql, (valor_mensual, dia_pago, fecha_fin, estado, observaciones, id))
            conexion.commit()
            cursor.close()
            conexion.close()

    def eliminar(self, id):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM contrato WHERE id=%s", (id,))
            conexion.commit()
            cursor.close()
            conexion.close()