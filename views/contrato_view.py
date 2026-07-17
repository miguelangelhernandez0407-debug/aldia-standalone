from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                              QTableWidgetItem, QPushButton, QLineEdit,
                              QMessageBox, QHeaderView, QComboBox)
from controllers.contrato_controller import ContratoController
from controllers.usuario_controller import UsuarioController
from controllers.inmueble_controller import InmuebleController

class ContratoView(QWidget):

    def __init__(self):
        super().__init__()
        self.controller = ContratoController()
        self.usuario_controller = UsuarioController()
        self.inmueble_controller = InmuebleController()
        self.setWindowTitle("Gestión de Contratos - AlDía")
        self.setMinimumSize(1000, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Formulario fila 1
        form1 = QHBoxLayout()
        self.cmb_inmueble = QComboBox()
        self.cmb_arrendador = QComboBox()
        self.cmb_arrendatario = QComboBox()
        self.cargar_combos()

        form1.addWidget(self.cmb_inmueble)
        form1.addWidget(self.cmb_arrendador)
        form1.addWidget(self.cmb_arrendatario)

        # Formulario fila 2
        form2 = QHBoxLayout()
        self.txt_valor = QLineEdit()
        self.txt_valor.setPlaceholderText("Valor mensual")
        self.txt_dia_pago = QLineEdit()
        self.txt_dia_pago.setPlaceholderText("Día de pago (1-28)")
        self.txt_fecha_inicio = QLineEdit()
        self.txt_fecha_inicio.setPlaceholderText("Fecha inicio (YYYY-MM-DD)")
        self.txt_fecha_fin = QLineEdit()
        self.txt_fecha_fin.setPlaceholderText("Fecha fin (YYYY-MM-DD)")
        self.cmb_estado = QComboBox()
        self.cmb_estado.addItems(["ACTIVO", "TERMINADO", "SUSPENDIDO"])
        self.txt_observaciones = QLineEdit()
        self.txt_observaciones.setPlaceholderText("Observaciones")

        form2.addWidget(self.txt_valor)
        form2.addWidget(self.txt_dia_pago)
        form2.addWidget(self.txt_fecha_inicio)
        form2.addWidget(self.txt_fecha_fin)
        form2.addWidget(self.cmb_estado)
        form2.addWidget(self.txt_observaciones)

        # Botones
        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_limpiar = QPushButton("Limpiar")

        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_actualizar.clicked.connect(self.actualizar)
        self.btn_eliminar.clicked.connect(self.eliminar)
        self.btn_limpiar.clicked.connect(self.limpiar)

        btn_layout.addWidget(self.btn_guardar)
        btn_layout.addWidget(self.btn_actualizar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addWidget(self.btn_limpiar)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels(["ID", "Inmueble", "Arrendador", "Arrendatario", "Valor", "Día Pago", "Estado"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.clicked.connect(self.seleccionar_fila)

        layout.addLayout(form1)
        layout.addLayout(form2)
        layout.addLayout(btn_layout)
        layout.addWidget(self.tabla)
        self.setLayout(layout)
        self.cargar_datos()

    def cargar_combos(self):
        usuarios = self.usuario_controller.obtener_usuarios()
        inmuebles = self.inmueble_controller.obtener_inmuebles()

        self.cmb_inmueble.clear()
        for inm in inmuebles:
            self.cmb_inmueble.addItem(f"{inm['direccion']} - {inm['ciudad']}", inm['id'])

        self.cmb_arrendador.clear()
        self.cmb_arrendatario.clear()
        for u in usuarios:
            self.cmb_arrendador.addItem(f"{u['nombre']} {u['apellido']}", u['id'])
            self.cmb_arrendatario.addItem(f"{u['nombre']} {u['apellido']}", u['id'])

    def cargar_datos(self):
        contratos = self.controller.obtener_contratos()
        self.tabla.setRowCount(len(contratos))
        for i, c in enumerate(contratos):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(c["id"])))
            self.tabla.setItem(i, 1, QTableWidgetItem(f"{c['direccion']} - {c['ciudad']}"))
            self.tabla.setItem(i, 2, QTableWidgetItem(f"{c['nombre_arrendador']} {c['apellido_arrendador']}"))
            self.tabla.setItem(i, 3, QTableWidgetItem(f"{c['nombre_arrendatario']} {c['apellido_arrendatario']}"))
            self.tabla.setItem(i, 4, QTableWidgetItem(str(c["valor_mensual"])))
            self.tabla.setItem(i, 5, QTableWidgetItem(str(c["dia_pago"])))
            self.tabla.setItem(i, 6, QTableWidgetItem(c["estado"]))

    def seleccionar_fila(self):
        fila = self.tabla.currentRow()
        self.id_seleccionado = self.tabla.item(fila, 0).text()
        self.txt_valor.setText(self.tabla.item(fila, 4).text())
        self.txt_dia_pago.setText(self.tabla.item(fila, 5).text())

    def guardar(self):
        ok, msg = self.controller.agregar_contrato(
            self.cmb_inmueble.currentData(),
            self.cmb_arrendador.currentData(),
            self.cmb_arrendatario.currentData(),
            self.txt_valor.text(),
            self.txt_dia_pago.text(),
            self.txt_fecha_inicio.text(),
            self.txt_fecha_fin.text() or None,
            self.cmb_estado.currentText(),
            self.txt_observaciones.text()
        )
        QMessageBox.information(self, "AlDía", msg)
        if ok:
            self.cargar_datos()
            self.limpiar()

    def actualizar(self):
        if not hasattr(self, "id_seleccionado"):
            QMessageBox.warning(self, "AlDía", "Selecciona un contrato de la tabla")
            return
        ok, msg = self.controller.actualizar_contrato(
            self.id_seleccionado,
            self.txt_valor.text(),
            self.txt_dia_pago.text(),
            self.txt_fecha_fin.text() or None,
            self.cmb_estado.currentText(),
            self.txt_observaciones.text()
        )
        QMessageBox.information(self, "AlDía", msg)
        if ok:
            self.cargar_datos()
            self.limpiar()

    def eliminar(self):
        if not hasattr(self, "id_seleccionado"):
            QMessageBox.warning(self, "AlDía", "Selecciona un contrato de la tabla")
            return
        confirmar = QMessageBox.question(self, "AlDía", "¿Estás seguro de eliminar este contrato?")
        if confirmar == QMessageBox.StandardButton.Yes:
            ok, msg = self.controller.eliminar_contrato(self.id_seleccionado)
            QMessageBox.information(self, "AlDía", msg)
            if ok:
                self.cargar_datos()
                self.limpiar()

    def limpiar(self):
        self.txt_valor.clear()
        self.txt_dia_pago.clear()
        self.txt_fecha_inicio.clear()
        self.txt_fecha_fin.clear()
        self.txt_observaciones.clear()
        if hasattr(self, "id_seleccionado"):
            del self.id_seleccionado