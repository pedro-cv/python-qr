import mariadb

config = {
  'host': 'localhost',
  'user': 'root',
  'password': '',
  'port': 3306 
}

conn = mariadb.connect(**config)
cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS microqr")