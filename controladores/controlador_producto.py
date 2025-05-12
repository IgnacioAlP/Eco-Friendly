from bd import obtener_conexion

def insertar_producto(nombre, precio, descuento, descripcion, estado, id_tipo_producto, id_genero, id_marca, id_categoria, id_grupo_edad, enlace_imagen):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
            INSERT INTO producto (nombre, precio, descuento, descripcion, estado, enlace_imagen, id_tipo_producto, id_genero, id_marca, id_categoria, id_grupo_edad)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (nombre, precio, descuento, descripcion, estado, enlace_imagen, id_tipo_producto, id_genero, id_marca, id_categoria, id_grupo_edad))
    conexion.commit()
    conexion.close()

def retornar_descuento(id):
    conexion = obtener_conexion()
    dsc= 0
    with conexion.cursor() as cursor:
        cursor.execute("""
            select descuento from producto where id = %s;
        """,(id))
        dsc= cursor.fetchone()
    conexion.close()
    return dsc

def retornar_precio(id):
    conexion = obtener_conexion()
    precio= 0
    with conexion.cursor() as cursor:
        cursor.execute("""
            select precio  from producto where id = %s;
        """,(id))
        precio = cursor.fetchone()
    conexion.close()
    return precio

def stock(idpr, id_pro):
    conexion = obtener_conexion()
    stock = 0
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT stock FROM detalle_presentacion
                    WHERE detalle_presentacion.id_presentacion = %s  AND detalle_presentacion.id_producto = %s;
            ''',(idpr,id_pro))
            stock = cursor.fetchone()
        conexion.close()
    except:
        stock = 0
    return  stock

def obtener_productos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.nombre, p.precio, p.descuento, ROUND(p.precio - (p.precio * p.descuento), 2) AS precio_final, p.descripcion, p.estado, tp.tipo AS tipo_producto, g.genero, m.marca, c.categoria, ge.grupoedad, p.enlace_imagen
            FROM producto p 
            INNER JOIN tipo_producto tp ON p.id_tipo_producto = tp.id 
            INNER JOIN marca m ON p.id_marca = m.id 
            INNER JOIN categoria c ON p.id_categoria = c.id 
            INNER JOIN genero g ON p.id_genero = g.id 
            INNER JOIN grupo_edad ge ON p.id_grupo_edad = ge.id 
            ORDER BY p.id ASC;
        """)
        productos = cursor.fetchall()
    conexion.close()
    return productos


def obtener_producto_por_id(id):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.nombre, p.precio, p.descuento, ROUND(p.precio - (p.precio * p.descuento), 2) AS precio_final, p.descripcion, p.estado, tp.tipo AS tipo_producto, g.genero, m.marca, c.categoria, ge.grupoedad, p.enlace_imagen
            FROM producto p 
            INNER JOIN tipo_producto tp ON p.id_tipo_producto = tp.id 
            INNER JOIN marca m ON p.id_marca = m.id 
            INNER JOIN categoria c ON p.id_categoria = c.id 
            INNER JOIN genero g ON p.id_genero = g.id 
            INNER JOIN grupo_edad ge ON p.id_grupo_edad = ge.id
            WHERE p.id = %s
            ORDER BY p.id ASC;
        """,(id,))
        productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_producto_por_categoria(nombre_categoria):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.nombre, p.precio, p.descuento, ROUND(p.precio - (p.precio * p.descuento), 2) AS precio_final, p.descripcion, p.estado, tp.tipo AS tipo_producto, g.genero, m.marca, c.categoria, ge.grupoedad, p.enlace_imagen
            FROM producto p 
            INNER JOIN tipo_producto tp ON p.id_tipo_producto = tp.id 
            INNER JOIN marca m ON p.id_marca = m.id 
            INNER JOIN categoria c ON p.id_categoria = c.id 
            INNER JOIN genero g ON p.id_genero = g.id 
            INNER JOIN grupo_edad ge ON p.id_grupo_edad = ge.id
            WHERE c.categoria = %s
            ORDER BY p.id ASC;
        """,(nombre_categoria,))
        productos = cursor.fetchall()
    conexion.close()
    return productos


def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM producto WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def actualizar_producto(id, nombre, precio, descuento, descripcion, estado, id_tipo_producto, id_genero, id_marca, id_categoria, id_grupo_edad, enlace_imagen):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE producto SET nombre = %s, precio = %s, descuento = %s, descripcion = %s, estado = %s, id_tipo_producto = %s, id_genero = %s id_marca = %s, id_categoria = %s, id_grupo_edad = %s, enlace_imagen = %s WHERE id = %s",
                       (nombre, precio, descuento, descripcion, estado, id_tipo_producto, id_genero, id_marca, id_categoria, id_grupo_edad, enlace_imagen, id))
    conexion.commit()
    conexion.close()