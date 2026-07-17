from models.usuario_model import UsuarioModel

class UsuarioController:

    def __init__(self):
        self.model = UsuarioModel()

    def obtener_usuarios(self):
        return self.model.obtener_todos()

    def agregar_usuario(self, nombre, apellido, nombre_usuario, correo, contrasena, num_documento, telefono):
        if not nombre or not apellido or not correo:
            return False, "Nombre, apellido y correo son obligatorios"
        try:
            self.model.insertar(nombre, apellido, nombre_usuario, correo, contrasena, num_documento, telefono)
            return True, "Usuario registrado correctamente"
        except Exception as e:
            return False, f"Error al registrar: {e}"

    def actualizar_usuario(self, id, nombre, apellido, correo, telefono):
        if not nombre or not apellido or not correo:
            return False, "Nombre, apellido y correo son obligatorios"
        try:
            self.model.actualizar(id, nombre, apellido, correo, telefono)
            return True, "Usuario actualizado correctamente"
        except Exception as e:
            return False, f"Error al actualizar: {e}"

    def eliminar_usuario(self, id):
        try:
            self.model.eliminar(id)
            return True, "Usuario eliminado correctamente"
        except Exception as e:
            return False, f"Error al eliminar: {e}"