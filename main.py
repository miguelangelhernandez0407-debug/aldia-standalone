import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from views.usuario_view import UsuarioView
from views.inmueble_view import InmuebleView
from views.contrato_view import ContratoView

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AlDía - Sistema de Gestión de Arriendos")
        self.setMinimumSize(1100, 700)

        tabs = QTabWidget()
        tabs.addTab(UsuarioView(), "Usuarios")
        tabs.addTab(InmuebleView(), "Inmuebles")
        tabs.addTab(ContratoView(), "Contratos")

        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())