import mariadb

config = {
  'host': 'localhost',
  'user': 'root',
  'password': '',
  'port': 3306  
}


try:
    conn = mariadb.connect(**config)
    cursor = conn.cursor()

    cursor.execute("DROP DATABASE IF EXISTS microqr")
    cursor.execute("CREATE DATABASE IF NOT EXISTS microqr")
    cursor.execute("USE microqr")

    cursor.execute("CREATE TABLE IF NOT EXISTS tipo (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS producto (id INT AUTO_INCREMENT PRIMARY KEY, cod VARCHAR(255), nombre VARCHAR(255),caducidad VARCHAR(255), tipo_id INT, FOREIGN KEY (tipo_id) REFERENCES tipo(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS sucursal (cod INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), ubicacion VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS sucursal_producto (sucursal_cod INT, producto_id INT, FOREIGN KEY (sucursal_cod) REFERENCES sucursal(cod), FOREIGN KEY (producto_id) REFERENCES producto(id))")


    cursor.execute("INSERT INTO tipo (nombre) VALUES ('Fruta')")

    sql = "INSERT INTO producto (cod, nombre,caducidad, tipo_id) VALUES (%s, %s, %s, %s)"
    values = [("4372666505625","Beef","2024-09-14", 1), ("6407405411573","Shrimp","2026-12-31", 1), ("4157094700968","Lamb","2027-03-26",1),("1123777462728","Tea","2023-10-01",1),("2656830670498","Cheese","2025-08-04",1),("1894689791181","Steam","2023-05-23",1),("2367547451025","Puree","2024-11-17",1),("8608522825964","Peeled","2026-02-28",1)]
    cursor.executemany(sql, values)

    sql = "INSERT INTO sucursal (name, ubicacion) VALUES (%s, %s)"
    values = [("Sucursal Cumavi", "Estanteria A1"), ("Sucursal Los Pinos", "Estanteria A2"), ("Sucursal Los Pozos", "Estanteria A3")]
    cursor.executemany(sql, values)

    sql = "INSERT INTO sucursal_producto (sucursal_cod, producto_id) VALUES (%s, %s)"
    values = [(1, 1), (2, 2), (3, 3), (1,4), (2,5), (3,6), (1,7), (2,8)]  
    cursor.executemany(sql, values)

    conn.commit()

    cursor.close()
    conn.close()

except mariadb.Error as e:
    print(f"Error de conexión a MariaDB: {e}")
