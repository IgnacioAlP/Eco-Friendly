from bd import obtener_conexion

def insertar_producto(nombre, precio, estado, stock, descripcion, descuento,
                      id_tipo_producto, id_genero, id_marca, id_categoria,
                      id_presentacion):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO producto (nombre, precio, estado, stock, descripcion, descuento,
                                    id_tipo_producto, id_genero, id_marca, id_categoria,
                                    id_presentacion)
                VALUES (%s, %s, %s, %s, %s, %s, '%s', %s, %s, %s,  %s)
            """, (nombre, precio, estado, stock, descripcion, descuento,
                id_tipo_producto, id_genero, id_marca, id_categoria,
                 id_presentacion))
        conexion.commit()
    except Exception as e:
        if conexion:
            conexion.rollback()
        logger.error(f"Error al insertar producto: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()


def obtener_productos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT id, nombre, precio, estado, stock, descripcion, descuento,
                   id_tipo_producto, id_genero, id_marca, id_categoria,
                    id_presentacion
            FROM producto
        """)
        productos = cursor.fetchall()
    conexion.close()
    return productos


def obtener_producto_por_id(id):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT id, nombre, precio, estado, stock, descripcion, descuento,
                   id_tipo_producto, id_genero, id_marca, id_categoria,
                    id_presentacion
            FROM producto WHERE id = %s
        """, (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto


def actualizar_producto(id, nombre, precio, estado, stock, descripcion, descuento,
                        id_tipo_producto, id_genero, id_marca, id_categoria,
                         id_presentacion):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE producto
                SET nombre = %s, precio = %s, estado = %s, stock = %s,
                    descripcion = %s, descuento = %s, id_tipo_producto = %s,
                    id_genero = %s, id_marca = %s, id_categoria = %s,
                     id_presentacion = %s
                WHERE id = %s
            """, (nombre, precio, estado, stock, descripcion, descuento,
                id_tipo_producto, id_genero, id_marca, id_categoria,
                 id_presentacion, id))
        conexion.commit()
        return True
    except Exception as e:
        if conexion:
            conexion.rollback()
        logger.error(f"Error al actualizar producto: {str(e)}")
        return False
    finally:
        if conexion:
            conexion.close()


def eliminar_producto(id):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM producto WHERE id = %s", (id,))
        conexion.commit()
    except Exception as e:
        if conexion:
            conexion.rollback()
        logger.error(f"Error al eliminar producto: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

from bd import obtener_conexion

def insertar_producto(nombre, precio, estado, descripcion, descuento, id_tipo_producto, id_genero, id_marca, id_categoria,  nombre_imagen):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
            INSERT INTO producto (nombre, precio, estado, descripcion, descuento, id_tipo_producto, id_genero, id_marca, id_categoria,  enlace_imagen) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (nombre, precio, estado, descripcion, descuento, id_tipo_producto, id_genero, id_marca, id_categoria, nombre_imagen))
    conexion.commit()
    conexion.close()


def retornardsc(id):
    conexion = obtener_conexion()
    dsc= 0
    with conexion.cursor() as cursor:
        cursor.execute("""
            select descuento  from producto where id = %s;
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
                select stock from detalle_presentacion
                    where detalle_presentacion.id_presentacion = %s  and detalle_presentacion.id_producto = %s;
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
            SELECT p.id, p.nombre, p.precio, p.descuento, ROUND(p.precio - (p.precio * p.descuento), 2) AS precio_d, 
                p.descripcion, p.estado, tp.tipo AS tipo_producto, g.genero, m.marca, c.categoria, 
                p.enlace_imagen
            FROM producto p 
            INNER JOIN tipo_producto tp ON p.id_tipo_producto = tp.id 
            INNER JOIN marca m ON p.id_marca = m.id 
            INNER JOIN categoria c ON p.id_categoria = c.id 
            INNER JOIN genero g ON p.id_genero = g.id  
            ORDER BY p.id ASC;
        """)
        productos = cursor.fetchall()
    conexion.close()
    return productos


def obtener_calzados():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT p.id, p.nombre, p.precio, p.descuento, ROUND(p.precio - (p.precio * p.descuento), 2) AS precio_d, 
                p.descripcion, p.estado, tp.tipo AS tipo_producto, g.genero, m.marca, c.categoria, 
                p.enlace_imagen, pr.color
            FROM producto p 
            INNER JOIN tipo_producto tp ON p.id_tipo_producto = tp.id 
            INNER JOIN marca m ON p.id_marca = m.id 
            INNER JOIN categoria c ON p.id_categoria = c.id 
            INNER JOIN genero g ON p.id_genero = g.id 
            INNER JOIN detalle_presentacion dp ON p.id = dp.id_producto
            INNER JOIN presentacion pr ON pr.id = dp.id_presentacion
            WHERE c.categoria = "Calzado" 
            ORDER BY p.id ASC;
        """)
        productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_modahombre():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT p.id, p.nombre, p.precio, p.descuento, ROUND(p.precio - (p.precio * p.descuento), 2) AS precio_d, 
                p.descripcion, p.estado, tp.tipo AS tipo_producto, g.genero, m.marca, c.categoria, 
                p.enlace_imagen,pr.color
            FROM producto p 
            INNER JOIN tipo_producto tp ON p.id_tipo_producto = tp.id 
            INNER JOIN marca m ON p.id_marca = m.id 
            INNER JOIN categoria c ON p.id_categoria = c.id 
            INNER JOIN genero g ON p.id_genero = g.id 
            INNER JOIN detalle_presentacion dp ON p.id = dp.id_producto
            INNER JOIN presentacion pr ON pr.id = dp.id_presentacion
            WHERE c.categoria = "Ropa Hombre" 
            ORDER BY p.id ASC;

        """)
        productos = cursor.fetchall()
    conexion.close()
    return productos




def obtener_ropaniños():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT p.id, p.nombre, p.precio, p.descuento, ROUND(p.precio - (p.precio * p.descuento), 2) AS precio_d, 
                p.descripcion, p.estado, tp.tipo AS tipo_producto, g.genero, m.marca, c.categoria,
                p.enlace_imagen, pr.color
            FROM producto p 
            INNER JOIN tipo_producto tp ON p.id_tipo_producto = tp.id 
            INNER JOIN marca m ON p.id_marca = m.id 
            INNER JOIN categoria c ON p.id_categoria = c.id 
            INNER JOIN genero g ON p.id_genero = g.id 
            INNER JOIN detalle_presentacion dp ON p.id = dp.id_producto
            INNER JOIN presentacion pr ON pr.id = dp.id_presentacion
            WHERE c.categoria = "Ropa niños"
            ORDER BY p.id ASC;

        """)
        productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_modamujer():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT p.id, p.nombre, p.precio, p.descuento, ROUND(p.precio - (p.precio * p.descuento), 2) AS precio_d, 
                p.descripcion, p.estado, tp.tipo AS tipo_producto, g.genero, m.marca, c.categoria,
                p.enlace_imagen, pr.color
            FROM producto p 
            INNER JOIN tipo_producto tp ON p.id_tipo_producto = tp.id 
            INNER JOIN marca m ON p.id_marca = m.id 
            INNER JOIN categoria c ON p.id_categoria = c.id 
            INNER JOIN genero g ON p.id_genero = g.id 
            INNER JOIN detalle_presentacion dp ON p.id = dp.id_producto
            INNER JOIN presentacion pr ON pr.id = dp.id_presentacion
            WHERE c.categoria = "Ropa Mujer"
            ORDER BY p.id ASC;  
        """)
        productos = cursor.fetchall()
    conexion.close()
    return productos


def obtener_producto_por_id(id_producto):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.nombre, p.precio, p.descuento, p.descripcion, p.estado, tp.tipo AS tipo_producto, g.genero, m.marca, c.categoria, 
            p.enlace_imagen
            FROM producto p 
            INNER JOIN tipo_producto tp ON p.id_tipo_producto = tp.id 
            INNER JOIN marca m ON p.id_marca = m.id 
            INNER JOIN categoria c ON p.id_categoria = c.id 
            INNER JOIN genero g ON p.id_genero = g.id   where p.id= %s
        """, (id_producto,))
    producto = cursor.fetchone()
    conexion.close()
    return producto

def produ():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            select id,nombre, enlace_imagen from producto;
        """)
        productos = cursor.fetchall()
    conexion.close()
    return productos


def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM producto WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def actualizar_producto(id_producto, nombre, precio, estado, descripcion, descuento, id_tipo_producto, id_genero, id_marca, id_categoria, enlace_imagen):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE producto SET nombre = %s, precio = %s, estado = %s, descripcion = %s, descuento = %s, id_tipo_producto = %s, id_genero = %s, id_marca = %s, id_categoria = %s, id_grupo_edad = %s, enlace_imagen = %s WHERE id = %s",
                       (nombre, precio, estado, descripcion, descuento, id_tipo_producto, id_genero, id_marca, id_categoria, enlace_imagen, id_producto))
    conexion.commit()
    conexion.close()
