# AlDía — Sistema de Gestión de Pagos de Arriendo

Aplicación de escritorio (PyQt6) para la gestión de usuarios, inmuebles y contratos de arriendo, con persistencia en MySQL.

## Requisitos previos
- Python 3.11+
- MySQL 8+
- Librería mysql-connector-python

## Instalación
```bash
git clone https://github.com/miguelangelhernandez0407-debug/aldia-standalone.git
cd aldia-standalone
pip install mysql-connector-python PyQt6
```

## Configuración de base de datos
Crear la base `aldia_db` en MySQL local y ajustar credenciales en `database/connection.py` si es necesario.

## Ejecución
```bash
python main.py
```

## Módulos
- **Usuarios**: gestión CRUD de usuarios del sistema.
- **Inmuebles**: gestión CRUD de propiedades en arriendo.
- **Contratos**: vincula usuarios e inmuebles con condiciones de arriendo.

## Estructura de ramas
- `main`: versión estable
- `develop`: integración de módulos
- `feature/*`: desarrollo por módulo