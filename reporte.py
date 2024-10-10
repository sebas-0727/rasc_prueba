import base64
import pymysql
from flask import Blueprint, jsonify, request, render_template

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'io0727.mysql.pythonanywhere-services.com',
    'user': 'io0727',
    'password': '^@k4,FB7RQ2?G_z',
    'database': 'io0727$default',
    'port': 3306
}

# Crear el blueprint para reportes
reporte_blueprint = Blueprint('reporte', __name__)

# Función para conectar a la base de datos
def conectar():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        db=DB_CONFIG['database'],  # Cambié 'db' a 'database' para coincidir con la configuración
        port=DB_CONFIG.get('port', 3306),
        cursorclass=pymysql.cursors.DictCursor
    )

# Ruta para mostrar el formulario de reporte
@reporte_blueprint.route("/reporte", methods=['GET'])
def formulario_reporte():
    return render_template("reporte.html")

# Ruta para la vista del administrador
@reporte_blueprint.route("/admin", methods=['GET'])
def admin():
    return render_template("admin.html")

# Función para obtener la imagen de una especie desde la base de datos
def get_especie_imagen(especie_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT imagen FROM reptiles WHERE numero = %s', (especie_id,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado['imagen'] if resultado else None
    except Exception as e:
        print(f"Error al obtener imagen de la especie: {e}")
        return None

# Ruta para obtener especies con imágenes
@reporte_blueprint.route("/especies", methods=['GET'])
def obtener_especies_con_imagenes():
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute('SELECT numero, nombre, imagen FROM reptiles')
        especies = cursor.fetchall()
        
        for especie in especies:
            if especie['imagen'] and isinstance(especie['imagen'], bytes):
                especie['imagen'] = base64.b64encode(especie['imagen']).decode('utf-8')
        
        cursor.close()
        conn.close()

        return jsonify(especies)
    except Exception as e:
        print(f"Error al obtener especies e imágenes: {e}")
        return jsonify({'mensaje': 'Error al obtener especies e imágenes'}), 500

# Ruta para registrar un nuevo reporte
@reporte_blueprint.route("/registrar_reporte", methods=['POST'])
def registrar_reporte():
    try:
        zona = request.form.get('zona')
        hora = request.form.get('hora')
        rep_especie_id = request.form.get('rep_especie_id')
        ataco = request.form.get('ataco')
        observaciones = request.form.get('observaciones')

        # Obtener imagen de la especie
        rep_especie_imagen = get_especie_imagen(rep_especie_id)

        imagen_url = None
        if 'imagen' in request.files and request.files['imagen'].filename != '':
            imagen_file = request.files['imagen']
            imagen_url = imagen_file.read()

        # Insertar los datos en la base de datos
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO reporte (zona, hora, especie_imagen, ataco, observaciones, imagen) VALUES (%s, %s, %s, %s, %s, %s)',
                    (zona, hora, rep_especie_imagen, ataco, observaciones, imagen_url))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'mensaje': 'Reporte agregado correctamente'})
    except Exception as ex:
        print(f"Error al agregar el reporte: {ex}")
        return jsonify({'mensaje': 'Error al agregar el reporte'}), 500

# Ruta para consultar los reportes generales
@reporte_blueprint.route("/reportes_general", methods=['GET'])
def consultar_reportes():
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT r.zona, r.hora, r.especie_imagen, r.ataco, r.imagen AS reporte_imagen, 
                rep.imagen AS especie_imagen, rep.nombre AS especie_nombre, r.observaciones
            FROM reporte r
            LEFT JOIN reptiles rep ON r.especie_imagen = rep.numero
        """)
        data = []

        for row in cur.fetchall():
            reporte_imagen_blob = row['reporte_imagen']
            especie_imagen_blob = row['especie_imagen']

            # Convertir las imágenes a base64 si existen
            reporte_imagen_base64 = base64.b64encode(reporte_imagen_blob).decode('utf-8') if reporte_imagen_blob else None
            especie_imagen_base64 = base64.b64encode(especie_imagen_blob).decode('utf-8') if especie_imagen_blob else None

            data.append({
                'zona': row['zona'],
                'hora': row['hora'],
                'especie_imagen': especie_imagen_base64,
                'ataco': row['ataco'],
                'imagen': reporte_imagen_base64,
                'observaciones': row['observaciones']
            })
        
        cur.close()
        conn.close()
        
        return jsonify({'reportes': data, 'mensaje': 'Reportes en la zona'})
    except Exception as ex:
        print(f"Error al consultar reportes: {ex}")
        return jsonify({'mensaje': 'Error al consultar reportes'}), 500

# Ruta para eliminar reportes antiguos (más de 7 días)
@reporte_blueprint.route("/limpiar_reportes_antiguos", methods=['POST'])
def limpiar_reportes_antiguos():
    try:
        conn = conectar()
        cur = conn.cursor()
        sql = "DELETE FROM reporte WHERE fecha_registro < CURDATE() - INTERVAL 7 DAY"
        cur.execute(sql)
        conn.commit()

        return jsonify({'mensaje': 'Reportes antiguos eliminados correctamente'})
    except Exception as ex:
        print(f"Error al eliminar reportes antiguos: {ex}")
        return jsonify({'mensaje': 'Error al eliminar reportes antiguos'}), 500
    finally:
        cur.close()
        conn.close()


