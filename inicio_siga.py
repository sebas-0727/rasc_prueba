from flask import Blueprint, request, redirect, url_for, render_template
import pymysql
import bcrypt

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'io0727.mysql.pythonanywhere-services.com',
    'user': 'io0727',
    'password': '^@k4,FB7RQ2?G_z',
    'database': 'io0727$default',
    'port': 3306
}

# Crear el blueprint
inicio_siga_blueprint = Blueprint('inicio_siga', __name__)

# Función para conectar a la base de datos
def conectar():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        db=DB_CONFIG['database'],  # Cambié 'db' a 'database' para coincidir con la configuración
        port=DB_CONFIG.get('port', 3306)
    )

# Ruta para el inicio de sesión
@inicio_siga_blueprint.route("/inicio_siga", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['correo']
        password = request.form['contraseña']

        # Verificar si el usuario es admin
        if email == 'admin' and password == '12345':
            return redirect(url_for('inicio_siga.admin_page'))

        # Verificación de formato de correo
        if '@' not in email:
            return render_template('inicio_siga.html', error="Por favor, ingrese un correo electrónico válido.")

        # Conexión a la base de datos
        conn = conectar()
        cursor = conn.cursor()

        # Consulta para obtener los datos del usuario
        cursor.execute("SELECT id, contraseña, activo FROM p_siga WHERE correo = %s", (email,))
        user = cursor.fetchone()

        # Verificar si el usuario existe y la contraseña es correcta
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            if user[2]:  # Verificar si la cuenta está activa
                return redirect(url_for('inicio_siga.siga_page'))
            else:
                return render_template('inicio_siga.html', error="Su cuenta no está activa. Por favor, contacte al administrador.")
        else:
            return render_template('inicio_siga.html', error="Correo o contraseña incorrectos.")

    return render_template('inicio_siga.html')

# Ruta para la página SIGA (usuario)
@inicio_siga_blueprint.route('/reptiles')
def siga_page():
    return "Bienvenido a la página SIGA!"

# Ruta para la página de administración
@inicio_siga_blueprint.route('/admin')
def admin_page():
    return "Bienvenido a la página de administración!"
