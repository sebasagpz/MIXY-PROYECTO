from flask import Flask, request, jsonify
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
dbname = 'PROYECTO_MIXY' #nombre de la base de datos
username = 'postgres'
password = 123456

"""Se definen las constantes para conectarse a PostgreSQL:
host: dirección del servidor.
port: puerto de conexión (por defecto, 5432).
dbname: nombre de la base de datos.
username: usuario de PostgreSQL.
password: contraseña del usuario."""

def get_connection(): 
    #propiedades
    conn = connect(host=host, port=port, dbname=dbname, user=username, password=password)
    return conn
    """Esta función crea y devuelve una conexión activa con la base de datos 
    PostgreSQL usando los parámetros definidos anteriormente."""

@app.get('/api/users') #Ruta: /api/users  con metodo get
def get_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(users)
    """Se conecta a la base de datos.
Se ejecuta una consulta SQL que selecciona todos los usuarios.
Se devuelven los resultados como una lista de diccionarios JSON."""

@app.post('/api/users') #Ruta: /api/users
def create_user():
    new_user = request.get_json()
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute('INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *', 
                (email, password))
    new_created_user = cur.fetchone()
    print(new_created_user)
    conn.commit()

    cur.close()
    conn.close()
    return jsonify(new_created_user)
    """Se encripta la contraseña antes de insertarla en la base de datos usando Fernet.encrypt().
Se ejecuta una sentencia SQL INSERT.
Se devuelve el nuevo usuario creado."""

@app.delete('/api/users/<id>')  #Ruta: /api/users/<id>
def delete_user(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('DELETE FROM users WHERE id = %s RETURNING * ', (id))
    user = cur.fetchone()
    
    conn.commit()

    conn.close()
    cur.close()

    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user)
    """Se elimina el usuario con el id especificado.
Si no existe, se devuelve un mensaje de error 404.
Si existe, se devuelve el usuario eliminado."""

# @app.put('/api/users/<id>')
# def update_user(id):
    
#     conn = get_connection()
#     cur = conn.cursor(cursor_factory=extras.RealDictCursor)

#     new_user = request.get_json()
#     username = new_user['username']
#     email = new_user['email']
#     password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))

#     cur.execute('UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s RETURNIG *', (username, email, password, id))
#     updated_user = cur.fetchone()

#     conn.commit()

#     cur.close()
#     conn.close()


#     if updated_user is None:
#         return jsonify({'menssage': 'User not found'}), 404
    
#     return jsonify(updated_user)

@app.get('/api/users/<id>')
def get_user(id):
    
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cur.fetchone()
    
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)