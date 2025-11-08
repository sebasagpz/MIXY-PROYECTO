from flask import Flask, request, jsonify, send_file
from psycopg2 import connect, extras
from cryptography.fernet import Fernet

"""Flask: Framework que nos permite crear un servidor web y definir rutas para nuestra API.

request y jsonify: Permiten recibir datos del cliente (por ejemplo, en formato JSON) y enviar respuestas también en JSON.

psycopg2: Librería que facilita la conexión y consultas a bases de datos PostgreSQL.

extras.RealDictCursor: Permite que los resultados de las consultas se devuelvan como diccionarios, en lugar de tuplas.

cryptography.fernet: Librería para encriptar y desencriptar contraseñas de manera segura."""

app = Flask(__name__)
key = Fernet.generate_key()

#se crea las constante para conectarse a postgres
host = 'localhost' 
port = 5432
dbname = 'proyecto_mixy' #nombre de la base de datos
username = 'postgres'
password = '123456'

"""Se definen las constantes para conectarse a PostgreSQL:
host: dirección del servidor.
port: puerto de conexión (por defecto, 5432).
dbname: nombre de la base de datos.
username: usuario de PostgreSQL.
password: contraseña del usuario."""

@app.route('/')
def inicio():
    return send_file('templates/index.html')

def get_connection(): 
    #propiedades
    conn = connect(host=host, port=port, dbname=dbname, user=username, password=password)
    return conn
    """Esta función crea y devuelve una conexión activa con la base de datos 
    PostgreSQL usando los parámetros definidos anteriormente."""

@app.get('/datos') #Ruta: /api/users  con metodo get
def get_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    

    cur.execute('SELECT * FROM usuarios')
    users = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(users)
    """Se conecta a la base de datos.
Se ejecuta una consulta SQL que selecciona todos los usuarios.
Se devuelven los resultados como una lista de diccionarios JSON."""

@app.post('/dato/api' ) #Ruta: /api/users
def create_user():
    new_user = request.get_json()
    nombre = new_user['nombre']
    apellido = new_user['apellido']
    correo = new_user['correo']
    nacimiento = new_user['nacimiento']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute('INSERT INTO usuarios (nombre, apellido, correo, nacimiento, password) VALUES (%s, %s, %s, %s, %s) RETURNING *', 
            (nombre, apellido, correo, nacimiento, password))


    new_created_user = cur.fetchone()
    print(new_created_user)
    conn.commit()

    cur.close()
    conn.close()
    return jsonify(new_created_user)
    """Se encripta la contraseña antes de insertarla en la base de datos usando Fernet.encrypt().
Se ejecuta una sentencia SQL INSERT.
Se devuelve el nuevo usuario creado."""



if __name__ == '__main__':
    app.run(debug=True)