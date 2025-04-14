
from bd import obtener_conexion

def nombre_productos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT producto FROM producto order by producto asc")
        productos = cursor.fetchall()
    conexion.close()
    return productos

def nombre_producto_por_id(id_producto):
    conexion = obtener_conexion()
    nombre_producto = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT producto FROM producto WHERE id = %s", (id_producto,))
        resultado = cursor.fetchone()
        if resultado:
            nombre_producto = resultado[0]
    conexion.close()
    return nombre_producto


def id_producto_por_nombre(nombre_producto):
    conexion = obtener_conexion()
    id_producto = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM producto WHERE producto = %s", (nombre_producto,))
        resultado = cursor.fetchone()
        if resultado:
            id_producto = resultado[0]
    conexion.close()
    return id_producto


def insertar_producto(producto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('INSERT INTO producto (producto) VALUES (%s)', (producto,))
    conexion.commit()
    conexion.close()

def obtener_productos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, producto FROM producto")
        productos = cursor.fetchall()
    conexion.close()
    return productos

def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM producto WHERE id  = %s", (id,))
    conexion.commit()
    conexion.close()

def obtener_producto_por_id(id):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, producto FROM producto WHERE id = %s", (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto

def actualizar_producto(id, producto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE producto SET producto = %s WHERE id = %s", (producto, id))
    conexion.commit()
    conexion.close()
