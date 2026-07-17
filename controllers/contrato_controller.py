from models.contrato_model import ContratoModel

class ContratoController:

    def __init__(self):
        self.model = ContratoModel()

    def obtener_contratos(self):
        return self.model.obtener_todos()

    def agregar_contrato(self, inmueble_id, arrendador_id, arrendatario_id, valor_mensual, dia_pago, fecha_inicio, fecha_fin, estado, observaciones):
        if not inmueble_id or not arrendador_id or not arrendatario_id or not valor_mensual:
            return False, "Inmueble, arrendador, arrendatario y valor mensual son obligatorios"
        try:
            self.model.insertar(inmueble_id, arrendador_id, arrendatario_id, valor_mensual, dia_pago, fecha_inicio, fecha_fin, estado, observaciones)
            return True, "Contrato registrado correctamente"
        except Exception as e:
            return False, f"Error al registrar: {e}"

    def actualizar_contrato(self, id, valor_mensual, dia_pago, fecha_fin, estado, observaciones):
        if not valor_mensual:
            return False, "El valor mensual es obligatorio"
        try:
            self.model.actualizar(id, valor_mensual, dia_pago, fecha_fin, estado, observaciones)
            return True, "Contrato actualizado correctamente"
        except Exception as e:
            return False, f"Error al actualizar: {e}"

    def eliminar_contrato(self, id):
        try:
            self.model.eliminar(id)
            return True, "Contrato eliminado correctamente"
        except Exception as e:
            return False, f"Error al eliminar: {e}"