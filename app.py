from flask import Flask, request, jsonify
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import mariadb

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'microqr'

def connect_to_database():
    return mariadb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
@app.route('/hello', methods=['GET'])
def hello():
    return { "message" : "hello"}

@app.route('/scan-qr', methods=['POST'])
def scan_qr():
    if 'image' not in request.files:
        return jsonify({'error': 'No se ha proporcionado ninguna imagen'}), 400

    image = request.files['image'].read()
    nparr = np.frombuffer(image, np.uint8)
    decoded_objects = decode(cv2.imdecode(nparr, cv2.IMREAD_COLOR))
    
    qr_code = decoded_objects[0].data.decode('utf-8')

    
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

    
        cursor.execute("SELECT * FROM producto WHERE cod = ?", (qr_code,))
        result = cursor.fetchone()
        if result:
            id_xd = result[0]
        else:
            return jsonify({'error': 'No se encontró ningún producto con el código QR proporcionado'}), 404

        print("respuesta id")
        print(id_xd)
   
        cursor.execute("SELECT producto.id, producto.nombre, sucursal.name, sucursal.ubicacion, producto.caducidad FROM producto "
                    "JOIN sucursal_producto ON producto.id = sucursal_producto.producto_id "
                    "JOIN sucursal ON sucursal_producto.sucursal_cod = sucursal.cod "
                    "WHERE producto.id = ?", (id_xd,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()


        print("Aswer")
        print(result)

        if result:
            product = {
                'id': result[0],
                'nombre_producto': result[1],
                'nombre_sucursal': result[2],
                'ubicacion_sucursal': result[3],
                'caducidad': result[4]
            }
            return jsonify({'product': product})
        else:
            return jsonify({'error': 'No se encontró ningún producto con el código QR proporcionado'}), 404

    except mariadb.Error as e:
        return jsonify({'error': f'Error de conexión a MariaDB: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
