from flask import Flask, render_template, request, url_for, redirect
import db  # Importamos el módulo de base de datos donde se encuentran las funciones de manejo de DB
from db import crear_base_datos, insertar_productos_iniciales, obtener_productos, get_db_Connection  # Importamos funciones específicas de db
from datetime import datetime  # Importamos datetime para gestionar fechas y horas
import pytz  # Importamos pytz para manejar zonas horarias

app = Flask(__name__)

# ----- Crear la función para la base de datos ------------
def setup():
    # Llamamos a la función para crear la base de datos y cargar los productos iniciales
    crear_base_datos() 
    insertar_productos_iniciales()

# Obtener la hora actual en Bolivia usando la zona horaria correspondiente
zona_bolivia = pytz.timezone('America/La_Paz')  # Definimos la zona horaria de Bolivia
fecha_bolivia = datetime.now(zona_bolivia).strftime('%Y-%m-%d %H:%M:%S')  # Obtenemos la hora actual formateada

# ----- Ruta principal (tienda) que muestra todos los productos -----
@app.route('/')
def tienda():
    # Establecemos la conexión con la base de datos
    conn = get_db_Connection()  
    # Ejecutamos una consulta SQL para obtener todos los productos de la tabla 'productos'
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()  # Cerramos la conexión a la base de datos
    # Renderizamos la plantilla 'index.html' y pasamos los productos obtenidos
    return render_template('index.html', productos=productos)

# -------- Ruta para ver detalles de un producto y realizar una compra --------
@app.route('/producto/<int:id>', methods=['GET', 'POST'])
def producto(id):
    # Establecemos la conexión con la base de datos
    conn = get_db_Connection()
    # Obtenemos el producto con el ID correspondiente
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()

    # Si no se encuentra el producto, mostramos un error 404
    if producto is None:
        return "Producto no encontrado", 404

    # Si la solicitud es de tipo POST (cuando se llena el formulario de compra)
    if request.method == 'POST':
        # Recibimos los datos del formulario de compra
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        talla = request.form['talla']
        cantidad = request.form['cantidad']
        
        # Insertamos la compra en la base de datos
        conn.execute('INSERT INTO compras (nombre, telefono, talla, cantidad) VALUES (?, ?, ?, ?)',
                     (nombre, telefono, talla, cantidad))
        conn.commit()  # Confirmamos los cambios
        conn.close()  # Cerramos la conexión
        # Redirigimos a la página principal (tienda) después de realizar la compra
        return redirect(url_for('tienda'))

    conn.close()  # Cerramos la conexión
    # Renderizamos la plantilla 'producto.html' con la información del producto
    return render_template('producto.html', producto=producto)

# ----- Ruta "Nosotros" para mostrar información sobre la tienda -----
@app.route('/nosotros')
def nosotros():
    # Renderizamos la plantilla 'nosotros.html'
    return render_template('nosotros.html')

# ----- Configuración inicial y ejecución de la app -----
if __name__ == '__main__':
    # Creamos la base de datos e insertamos productos iniciales cuando la aplicación arranca
    with app.app_context():
        db.crear_base_datos()  # Crear la base de datos
        db.insertar_productos_iniciales()  # Insertar los productos iniciales
    # Iniciamos la aplicación en modo debug
    app.run(debug=True)
