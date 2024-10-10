import threading
import time
import pymysql
from plyer import notification  # Usando plyer para notificaciones (en entornos locales)
from flask import Blueprint, jsonify

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'io0727.mysql.pythonanywhere-services.com',
    'user': 'io0727',
    'password': '^@k4,FB7RQ2?G_z',
    'database': 'io0727$default',
    'port': 3306
}

# Rutas de archivos (el sonido no se reproducirá en PythonAnywhere)
SONIDO_ALERTA = "./static/alerta/public_alerta.mp3"
ICONO_PATH = "./static/alerta/imagen_prueba.png"

# Crear el blueprint
alerta_blueprint = Blueprint('alerta', __name__)

# Variables globales para controlar el sistema de alertas
notificaciones_enviadas = set()
alerta_thread = None
is_alerting = False

# Función para obtener el último número en la base de datos
def obtener_ultimo_numero():
    with pymysql.connect(**DB_CONFIG) as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT MAX(numero) as max_numero FROM reporte")
            resultado = cursor.fetchone()
            return resultado['max_numero'] if resultado['max_numero'] is not None else 0

# Función para verificar si hay nuevos registros
def verificar_nuevos_registros(ultimo_numero_conocido):
    with pymysql.connect(**DB_CONFIG) as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM reporte WHERE numero > %s", (ultimo_numero_conocido,))
            return cursor.fetchall()

# Función para reproducir el sonido de alerta (no funciona en PythonAnywhere)
def reproducir_sonido():
    # Esta parte no funcionará en PythonAnywhere ya que no tiene soporte para sonido
    # if os.path.exists(SONIDO_ALERTA):
    #     os.system(f"mpg123 {SONIDO_ALERTA}")  # Ejecuta el archivo de sonido usando mpg123 (Linux/Mac) o ajusta para Windows
    # else:
    #     print(f"Archivo de sonido no encontrado: {SONIDO_ALERTA}. Asegúrate de que la ruta sea correcta.")
    pass

# Función para enviar notificaciones usando plyer (esto solo funciona en entornos locales)
def enviar_notificacion(registro):
    global notificaciones_enviadas

    if registro['numero'] not in notificaciones_enviadas:
        # Intentar reproducir el sonido localmente (no en PythonAnywhere)
        reproducir_sonido()

        # Implementación con plyer (no funcionará en PythonAnywhere, solo en entornos locales)
        notification.notify(
            title=f"Nuevo reporte en: {registro['zona']}",
            message=f"Hora: {registro['hora']}\nAtaque: {registro['ataco']}\nObservaciones: {registro['observaciones']}",
            app_name='Sistema de Alerta',
            app_icon=ICONO_PATH,  # Asegúrate de que esta ruta sea correcta
            timeout=10  # Duración de la notificación en segundos
        )

        notificaciones_enviadas.add(registro['numero'])

# Función principal para monitorear las alertas
def alerta():
    global is_alerting
    ultimo_numero_conocido = obtener_ultimo_numero()
    print("Sistema de alerta activado...")

    while is_alerting:
        nuevos_registros = verificar_nuevos_registros(ultimo_numero_conocido)
        for registro in nuevos_registros:
            enviar_notificacion(registro)
            ultimo_numero_conocido = registro['numero']
        
        time.sleep(3)  # Espera de 3 segundos antes de la siguiente verificación

# Ruta para iniciar el sistema de alertas
@alerta_blueprint.route('/start_alerta')
def start_alerta():
    global alerta_thread, is_alerting
    if not is_alerting:
        is_alerting = True
        alerta_thread = threading.Thread(target=alerta)
        alerta_thread.start()
        return jsonify({"status": "Sistema de alerta iniciado"})
    return jsonify({"status": "El sistema de alerta ya está en ejecución"})

# Ruta para detener el sistema de alertas
@alerta_blueprint.route('/stop_alerta')
def stop_alerta():
    global is_alerting
    if is_alerting:
        is_alerting = False
        return jsonify({"status": "Sistema de alerta detenido"})
    return jsonify({"status": "El sistema de alerta no está en ejecución"})

# Función para inicializar el sistema de alertas
def init_alerta():
    global alerta_thread, is_alerting
    is_alerting = True
    alerta_thread = threading.Thread(target=alerta)
    alerta_thread.start()
