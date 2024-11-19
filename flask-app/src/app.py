from flask import Flask, redirect, request, jsonify, send_from_directory, session
from werkzeug.security import generate_password_hash, check_password_hash

import mysql.connector

app = Flask(__name__,static_folder='static')
app.secret_key = "super_secret_key"

# MySQL connection details
db_host = "mysql"
db_user = "user"
db_password = "password"
db_name = "mydatabase"

# Function to connect to the database
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None



@app.route('/')
def serve_index():
    if 'user_id' not in session:
        return send_from_directory('static', 'login.html')
    else:
        return send_from_directory('static', 'index.html') 
    

# Endpoint para login de usuario - lider@correo.com - 12345678
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return send_from_directory('static', 'login.html')  # Muestra el formulario de login

    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({'error': 'Email y contraseña son requeridos'}), 400

    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM usuarios WHERE email = %s"
    val = (email, )

    try:
        cursor.execute(sql, val) 
        usuario = cursor.fetchone() 
        
        if usuario and check_password_hash(usuario['password'], password):
            
            session['user_id'] = usuario['id_usuario']  # Guarda el id del usuario en la sesión
            return redirect('/')  # Redirige al index
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401
    except mysql.connector.Error as err:
        print(f"Error al autenticar usuario: {err}")
        return jsonify({'error': 'Error en el servidor'}), 500
    finally:
        cursor.close()
        conn.close()
            
@app.route('/registro', methods=['GET','POST'])
def registro(): 
    if request.method == 'GET':
        return send_from_directory('static', 'registro.html')  # Muestra el formulario de registro

    nombre = request.form.get('nombre')  # Cambiado de username a nombre
    email = request.form.get('email')
    password = request.form.get('password')
    apellido = request.form.get('apellido')
    fechanac = request.form.get('fechanac')
    
    if not nombre or not email or not password or not apellido or not fechanac:
        return jsonify({'error': 'Todos los campos son requeridos'}), 400

    hashed_password = generate_password_hash(password)

    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    # Verificar si el email ya está registrado
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({'error': 'El email ya está registrado'}), 409

    # Insertar el nuevo usuario en la base de datos
    try:
        sql = "INSERT INTO usuarios (nombre, email, password, apellido, fechanac) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nombre, email, hashed_password, apellido, fechanac))
        conn.commit()
        
        # Redirigir al usuario a la página de login después de registrarse con éxito
        return redirect('/login')
    except mysql.connector.Error as err:
        print(f"Error al registrar usuario: {err}")
        return jsonify({'error': 'Error en el servidor'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/logout', methods=['POST'])
def logout():
    # Elimina el usuario de la sesión
    session.pop('user_id', None)  # Elimina el id de usuario de la sesión
    return send_from_directory('static', 'login.html')  # Redirige a login.html

# Endpoint to create a new usuario
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    
    email = data.get('email')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    fechanac = data.get('fechanac')
    password = data.get('password')

    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "INSERT INTO usuarios (email, nombre, apellido, fechanac, password) VALUES (%s, %s, %s, %s, %s)"
    val = (email, nombre, apellido, fechanac, password)

    try:
        cursor.execute(sql, val)
        conn.commit()
        return jsonify({'message': 'Usuario creado correctamente'}), 200
    except mysql.connector.Error as err:
        print(f"Error inserting usuario: {err}")
        return jsonify({'error': 'Error al crear el usuario'}), 500
    finally:
        if conn:
            conn.close() 

# Endpoint to get all usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM usuarios"
    cursor.execute(sql)
    usuarios = cursor.fetchall()
    data = {
        "rta":"ok",
        "message":"usuarios encontrados",
        "rdo": usuarios
    }

    return jsonify(data), 200

# Endpoint to get a usuario by email
@app.route('/usuarios/<string:email>', methods=['GET'])
def get_usuario(email):
    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "SELECT * FROM usuarios WHERE email = '"+email+"';"
    val = (email,)
    cursor.execute(sql)
    print(email)
    usuario = cursor.fetchone()
    print(usuario)
    data = {
        "rta":"ok",
    }

    if usuario:
        data["usuarios"] = usuario
        return jsonify(data), 200
    else:
        data["error"] = "usuario no encontrado"
        return jsonify(data), 404

# Endpoint to update a usuario
@app.route('/usuarios/<string:email>', methods=['POST'])
def update_usuario(email):
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    fechanac = data.get('fechanac')

    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "UPDATE usuarios SET nombre = %s, apellido = %s, fechaNac = %s WHERE email = %s"
    val = (nombre, apellido, fechanac, email)

    try:
        cursor.execute(sql, val)
        conn.commit()
        return jsonify({'message': 'Usuario actualizado correctamente'}), 200
    except mysql.connector.Error as err:
        print(f"Error updating usuario: {err}")
        return jsonify({'error': 'Error al actualizar el usuario'}), 500
    finally:
        if conn:
            conn.close()

# Endpoint to delete a usuario
@app.route('/usuarios/<string:email>', methods=['DELETE'])
def delete_usuario(email):

    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "DELETE FROM usuarios WHERE email = %s"
    val = (email,)
    try:
        cursor.execute(sql, val)
        conn.commit()
        return jsonify({'message': 'Usuario eliminado correctamente'}), 200
    except mysql.connector.Error as err:
        print(f"Error deleting usuario: {err}")
        return jsonify({'error': 'Error al eliminar el usuario'}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')