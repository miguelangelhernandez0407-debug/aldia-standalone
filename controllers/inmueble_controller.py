from models.inmueble_model import InmuebleModel

class InmuebleController:

    def __init__(self):
        self.model = InmuebleModel()

    def obtener_inmuebles(self):
        return self.model.obtener_todos()

    def agregar_inmueble(self, direccion, ciudad, departamento, tipo, descripcion, propietario_id):
        if not direccion or not ciudad:
            return False, "Dirección y ciudad son obligatorios"
        try:
            self.model.insertar(direccion, ciudad, departamento, tipo, descripcion, propietario_id)
            return True, "Inmueble registrado correctamente"
        except Exception as e:
            return False, f"Error al registrar: {e}"

    def actualizar_inmueble(self, id, direccion, ciudad, tipo, descripcion):
        if not direccion or not ciudad:
            return False, "Dirección y ciudad son obligatorios"
        try:
            self.model.actualizar(id, direccion, ciudad, tipo, descripcion)
            return True, "Inmueble actualizado correctamente"
        except Exception as e:
            return False, f"Error al actualizar: {e}"

    def eliminar_inmueble(self, id):
        try:
            self.model.eliminar(id)
            return True, "Inmueble eliminado correctamente"
        except Exception as e:
            return False, f"Error al eliminar: {e}"