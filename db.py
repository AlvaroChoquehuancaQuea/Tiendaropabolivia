import sqlite3
import os


def get_db_Connection():
    conn = sqlite3.connect("productos.db")
    conn.row_factory = sqlite3.Row
    return conn


def crear_base_datos():
    try:
        with sqlite3.connect('productos.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL,
                    imagen TEXT NOT NULL
                )
            ''')
            conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")


def crear_base_datos():
    try:
        with sqlite3.connect('productos.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
              CREATE TABLE IF NOT EXISTS compras (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nombre TEXT NOT NULL,
                   telefono INT NOT NULL,
                   talla TEXT NOT NULL,
                   cantidad INTEGER NOT NULL,
                   fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")



def insertar_producto(nombre, precio, imagen):
    try:
        with sqlite3.connect('productos.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute('INSERT INTO productos (nombre, precio, imagen) VALUES (?, ?, ?)', 
                           (nombre, precio, imagen))
            conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al insertar el producto: {e}")


def obtener_productos():
    try:
        with sqlite3.connect('productos.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute('SELECT id, nombre, precio, imagen FROM productos')
            productos = cursor.fetchall()

        # Convertimos la tupla en un diccionario
        productos_dict = []
        for producto in productos:
            productos_dict.append({
                "id": producto[0],
                "nombre": producto[1],
                "precio": producto[2],
                "imagen": producto[3]
            })
        
        return productos_dict
    except sqlite3.Error as e:
        print(f"Error al obtener los productos: {e}")
        return []
    

def insertar_productos_iniciales():
    try:
        with sqlite3.connect('productos.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute('SELECT COUNT(*) FROM productos')
            cantidad = cursor.fetchone()[0]
            
            if cantidad == 0:
                productos = [
                    ('Camisa VueJS', 30, '1.jpg'),
                    ('Camisa Angular', 25, '2.jpg'),
                    ('Camisa React', 50, '3.jpg'),
                    ('Camisa Redux', 25, '4.jpg'),
                    ('Camisa Node.js', 23, '5.jpg'),
                    ('Camisa SASS', 45, '6.jpg'),
                    ('Camisa HTML5', 30, '7.jpg'),
                    ('Camisa Github', 25, '8.jpg'),
                    ('Camisa Bulma', 32, '9.jpg'),
                    ('Camisa TypeScript', 45, '10.jpg'),
                    ('Camisa Drupal', 10, '11.jpg'),
                    ('Camisa JavaScript', 26, '12.jpg'),
                    ('Camisa GraphQL', 36, '13.jpg'),
                    ('Camisa WordPress', 25, '14.jpg')
                    
                ]
                cursor.executemany('INSERT INTO productos (nombre, precio, imagen) VALUES (?, ?, ?)', productos)
                conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al insertar productos iniciales: {e}")
