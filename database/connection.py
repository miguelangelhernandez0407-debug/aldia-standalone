import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            port=3306,
            database="aldia_db",
            user="root",
            password=""
        )
        return conexion
    except Error as e:
        print(f"Error de conexión: {e}")
        return None