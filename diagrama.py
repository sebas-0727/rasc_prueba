from flask import Blueprint, jsonify, render_template
import pymysql

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'io0727.mysql.pythonanywhere-services.com',
    'user': 'io0727',
    'password': '^@k4,FB7RQ2?G_z',
    'database': 'io0727$default',
    'port': 3306
}

# Crear el blueprint
diagrama_blueprint = Blueprint('diagrama', __name__)

# Función para conectar a la base de datos
def conectar():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        db=DB_CONFIG['database'],  # Cambié 'db' a 'database' para coincidir con la configuración
        port=DB_CONFIG.get('port', 3306)
    )

# Función para obtener los datos de conteo desde la base de datos
def datos_conteo():
    conn = None
    try:
        conn = conectar()
        cur = conn.cursor()
        consulta = """
        SELECT zona, COUNT(*) AS conteo
        FROM reporte
        GROUP BY zona
        """
        cur.execute(consulta)
        datos = cur.fetchall()
        return [list(row) for row in datos]  # Convertir tuplas a listas
    finally:
        if conn:
            conn.close()

# Ruta para mostrar la página del diagrama
@diagrama_blueprint.route("/diagrama")
def inicio():
    return render_template('diagrama.html')

# Ruta para obtener los datos en formato JSON
@diagrama_blueprint.route('/datos')
def datos_json():
    datos = datos_conteo()
    return jsonify(datos)
