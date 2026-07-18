import re
from models.usuario_model import UsuarioModel

class UsuarioController:
    """Controlador que gestiona las operaciones CRUD de usuarios,
    delegando la persistencia al UsuarioModel."""

    def __init__(self):
        self.model = UsuarioModel()

    def obtener_usuarios(self):
        """Retorna la lista completa de usuarios registrados."""
        return self.model.obtener_todos()

    def agregar_usuario(self, nombre, apellido, nombre_usuario, correo, contrasena, num_documento, telefono):
        """Registra un nuevo usuario tras validar campos obligatorios
        y formato de correo. Retorna (éxito: bool, mensaje: str)."""
        if not nombre or not apellido or not correo:
            return False, "Nombre, apellido y correo son obligatorios"
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", correo):
            return False, "El formato del correo no es válido"
        try:
            self.model.insertar(nombre, apellido, nombre_usuario, correo, contrasena, num_documento, telefono)
            return True, "Usuario registrado correctamente"
        except Exception as e:
            return False, f"Error al registrar: {e}"

    def actualizar_usuario(self, id, nombre, apellido, correo, telefono):
        """Actualiza los datos de un usuario existente por su id."""
        if not nombre or not apellido or not correo:
            return False, "Nombre, apellido y correo son obligatorios"
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", correo):
            return False, "El formato del correo no es válido"
        try:
            self.model.actualizar(id, nombre, apellido, correo, telefono)
            return True, "Usuario actualizado correctamente"
        except Exception as e:
            return False, f"Error al actualizar: {e}"

    def eliminar_usuario(self, id):
        """Elimina un usuario por su id."""
        try:
            self.model.eliminar(id)
            return True, "Usuario eliminado correctamente"
        except Exception as e:
            return False, f"Error al eliminar: {e}"