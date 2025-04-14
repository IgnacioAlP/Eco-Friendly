from bd import obtener_conexion

def insertar_producto(nombre, precio, estado, stock, descripcion, descuento,
                      id_tipo_producto, id_genero, id_marca, id_categoria,
                      id_grupo_edad, id_presentacion):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO producto (nombre, precio, estado, stock, descripcion, descuento,
                                    id_tipo_producto, id_genero, id_marca, id_categoria,
                                    id_grupo_edad, id_presentacion)
                VALUES (%s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s)
            """, (nombre, precio, estado, stock, descripcion, descuento,
                id_tipo_producto, id_genero, id_marca, id_categoria,
                id_grupo_edad, id_presentacion))
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
                   id_grupo_edad, id_presentacion
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
                   id_grupo_edad, id_presentacion
            FROM producto WHERE id = %s
        """, (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto


def actualizar_producto(id, nombre, precio, estado, stock, descripcion, descuento,
                        id_tipo_producto, id_genero, id_marca, id_categoria,
                        id_grupo_edad, id_presentacion):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE producto
                SET nombre = %s, precio = %s, estado = %s, stock = %s,
                    descripcion = %s, descuento = %s, id_tipo_producto = %s,
                    id_genero = %s, id_marca = %s, id_categoria = %s,
                    id_grupo_edad = %s, id_presentacion = %s
                WHERE id = %s
            """, (nombre, precio, estado, stock, descripcion, descuento,
                id_tipo_producto, id_genero, id_marca, id_categoria,
                id_grupo_edad, id_presentacion, id))
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
