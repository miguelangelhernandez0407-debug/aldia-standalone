from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                              QTableWidgetItem, QPushButton, QLineEdit,
                              QMessageBox, QHeaderView, QComboBox)
from controllers.inmueble_controller import InmuebleController
from controllers.usuario_controller import UsuarioController

class InmuebleView(QWidget):

    def __init__(self):
        super().__init__()
        self.controller = InmuebleController()
        self.usuario_controller = UsuarioController()
        self.setWindowTitle("Gestión de Inmuebles - AlDía")
        self.setMinimumSize(900, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Formulario
        form_layout = QHBoxLayout()

        self.txt_direccion = QLineEdit()
        self.txt_direccion.setPlaceholderText("Dirección")
        self.txt_ciudad = QLineEdit()
        self.txt_ciudad.setPlaceholderText("Ciudad")
        self.txt_departamento = QLineEdit()
        self.txt_departamento.setPlaceholderText("Departamento")
        self.txt_descripcion = QLineEdit()
        self.txt_descripcion.setPlaceholderText("Descripción")

        self.cmb_tipo = QComboBox()
        self.cmb_tipo.addItems(["APARTAMENTO", "CASA", "HABITACION", "LOCAL", "OTRO"])

        self.cmb_propietario = QComboBox()
        self.cargar_propietarios()

        form_layout.addWidget(self.txt_direccion)
        form_layout.addWidget(self.txt_ciudad)
        form_layout.addWidget(self.txt_departamento)
        form_layout.addWidget(self.cmb_tipo)
        form_layout.addWidget(self.txt_descripcion)
        form_layout.addWidget(self.cmb_propietario)

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
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Dirección", "Ciudad", "Tipo", "Propietario", "Activo"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.clicked.connect(self.seleccionar_fila)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.tabla)
        self.setLayout(layout)
        self.cargar_datos()

    def cargar_propietarios(self):
        self.propietarios = self.usuario_controller.obtener_usuarios()
        self.cmb_propietario.clear()
        for p in self.propietarios:
            self.cmb_propietario.addItem(f"{p['nombre']} {p['apellido']}", p['id'])

    def cargar_datos(self):
        inmuebles = self.controller.obtener_inmuebles()
        self.tabla.setRowCount(len(inmuebles))
        for i, inm in enumerate(inmuebles):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(inm["id"])))
            self.tabla.setItem(i, 1, QTableWidgetItem(inm["direccion"]))
            self.tabla.setItem(i, 2, QTableWidgetItem(inm["ciudad"]))
            self.tabla.setItem(i, 3, QTableWidgetItem(inm["tipo"]))
            self.tabla.setItem(i, 4, QTableWidgetItem(f"{inm['nombre']} {inm['apellido']}"))
            self.tabla.setItem(i, 5, QTableWidgetItem("Sí" if inm["activo"] else "No"))

    def seleccionar_fila(self):
        fila = self.tabla.currentRow()
        self.id_seleccionado = self.tabla.item(fila, 0).text()
        self.txt_direccion.setText(self.tabla.item(fila, 1).text())
        self.txt_ciudad.setText(self.tabla.item(fila, 2).text())

    def guardar(self):
        propietario_id = self.cmb_propietario.currentData()
        ok, msg = self.controller.agregar_inmueble(
            self.txt_direccion.text(), self.txt_ciudad.text(),
            self.txt_departamento.text(), self.cmb_tipo.currentText(),
            self.txt_descripcion.text(), propietario_id
        )
        QMessageBox.information(self, "AlDía", msg)
        if ok:
            self.cargar_datos()
            self.limpiar()

    def actualizar(self):
        if not hasattr(self, "id_seleccionado"):
            QMessageBox.warning(self, "AlDía", "Selecciona un inmueble de la tabla")
            return
        ok, msg = self.controller.actualizar_inmueble(
            self.id_seleccionado, self.txt_direccion.text(),
            self.txt_ciudad.text(), self.cmb_tipo.currentText(),
            self.txt_descripcion.text()
        )
        QMessageBox.information(self, "AlDía", msg)
        if ok:
            self.cargar_datos()
            self.limpiar()

    def eliminar(self):
        if not hasattr(self, "id_seleccionado"):
            QMessageBox.warning(self, "AlDía", "Selecciona un inmueble de la tabla")
            return
        confirmar = QMessageBox.question(self, "AlDía", "¿Estás seguro de eliminar este inmueble?")
        if confirmar == QMessageBox.StandardButton.Yes:
            ok, msg = self.controller.eliminar_inmueble(self.id_seleccionado)
            QMessageBox.information(self, "AlDía", msg)
            if ok:
                self.cargar_datos()
                self.limpiar()

    def limpiar(self):
        self.txt_direccion.clear()
        self.txt_ciudad.clear()
        self.txt_departamento.clear()
        self.txt_descripcion.clear()
        if hasattr(self, "id_seleccionado"):
            del self.id_seleccionado