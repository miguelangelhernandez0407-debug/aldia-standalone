from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                              QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                              QMessageBox, QHeaderView)
from controllers.usuario_controller import UsuarioController

class UsuarioView(QWidget):

    def __init__(self):
        super().__init__()
        self.controller = UsuarioController()
        self.setWindowTitle("Gestión de Usuarios - AlDía")
        self.setMinimumSize(800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Formulario
        form_layout = QHBoxLayout()

        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre")
        self.txt_apellido = QLineEdit()
        self.txt_apellido.setPlaceholderText("Apellido")
        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("Nombre de usuario")
        self.txt_correo = QLineEdit()
        self.txt_correo.setPlaceholderText("Correo")
        self.txt_contrasena = QLineEdit()
        self.txt_contrasena.setPlaceholderText("Contraseña")
        self.txt_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_documento = QLineEdit()
        self.txt_documento.setPlaceholderText("Num. Documento")
        self.txt_telefono = QLineEdit()
        self.txt_telefono.setPlaceholderText("Teléfono")

        form_layout.addWidget(self.txt_nombre)
        form_layout.addWidget(self.txt_apellido)
        form_layout.addWidget(self.txt_usuario)
        form_layout.addWidget(self.txt_correo)
        form_layout.addWidget(self.txt_contrasena)
        form_layout.addWidget(self.txt_documento)
        form_layout.addWidget(self.txt_telefono)

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
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Correo", "Teléfono", "Activo"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.clicked.connect(self.seleccionar_fila)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.tabla)
        self.setLayout(layout)
        self.cargar_datos()

    def cargar_datos(self):
        usuarios = self.controller.obtener_usuarios()
        self.tabla.setRowCount(len(usuarios))
        for i, u in enumerate(usuarios):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(u["id"])))
            self.tabla.setItem(i, 1, QTableWidgetItem(u["nombre"]))
            self.tabla.setItem(i, 2, QTableWidgetItem(u["apellido"]))
            self.tabla.setItem(i, 3, QTableWidgetItem(u["correo"]))
            self.tabla.setItem(i, 4, QTableWidgetItem(u["telefono"] or ""))
            self.tabla.setItem(i, 5, QTableWidgetItem("Sí" if u["activo"] else "No"))

    def seleccionar_fila(self):
        fila = self.tabla.currentRow()
        self.id_seleccionado = self.tabla.item(fila, 0).text()
        self.txt_nombre.setText(self.tabla.item(fila, 1).text())
        self.txt_apellido.setText(self.tabla.item(fila, 2).text())
        self.txt_correo.setText(self.tabla.item(fila, 3).text())
        self.txt_telefono.setText(self.tabla.item(fila, 4).text())

    def guardar(self):
        ok, msg = self.controller.agregar_usuario(
            self.txt_nombre.text(), self.txt_apellido.text(),
            self.txt_usuario.text(), self.txt_correo.text(),
            self.txt_contrasena.text(), self.txt_documento.text(),
            self.txt_telefono.text()
        )
        QMessageBox.information(self, "AlDía", msg)
        if ok:
            self.cargar_datos()
            self.limpiar()

    def actualizar(self):
        if not hasattr(self, "id_seleccionado"):
            QMessageBox.warning(self, "AlDía", "Selecciona un usuario de la tabla")
            return
        ok, msg = self.controller.actualizar_usuario(
            self.id_seleccionado, self.txt_nombre.text(),
            self.txt_apellido.text(), self.txt_correo.text(),
            self.txt_telefono.text()
        )
        QMessageBox.information(self, "AlDía", msg)
        if ok:
            self.cargar_datos()
            self.limpiar()

    def eliminar(self):
        if not hasattr(self, "id_seleccionado"):
            QMessageBox.warning(self, "AlDía", "Selecciona un usuario de la tabla")
            return
        confirmar = QMessageBox.question(self, "AlDía", "¿Estás seguro de eliminar este usuario?")
        if confirmar == QMessageBox.StandardButton.Yes:
            ok, msg = self.controller.eliminar_usuario(self.id_seleccionado)
            QMessageBox.information(self, "AlDía", msg)
            if ok:
                self.cargar_datos()
                self.limpiar()

    def limpiar(self):
        self.txt_nombre.clear()
        self.txt_apellido.clear()
        self.txt_usuario.clear()
        self.txt_correo.clear()
        self.txt_contrasena.clear()
        self.txt_documento.clear()
        self.txt_telefono.clear()
        if hasattr(self, "id_seleccionado"):
            del self.id_seleccionado