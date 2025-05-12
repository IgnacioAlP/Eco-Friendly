from bd import obtener_conexion

def obtener_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT id, numdocumento, apellidos, nombres, telefono, correo, estado, id_tipo_usuario 
            FROM usuario 
            ORDER BY id_tipo_usuario ASC, apellidos ASC
        """)
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

def eliminar_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def suspender_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # Verificar el estado actual
        cursor.execute("SELECT estado FROM usuario WHERE id = %s", (id,))
        estado_actual = cursor.fetchone()
        # Si no está suspendido, lo suspendemos
        if estado_actual and estado_actual[0] != 'S':
            cursor.execute("UPDATE usuario SET estado = 'S' WHERE id = %s", (id,))
            conexion.commit()
    conexion.close()

def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT id, numdocumento, apellidos, nombres, telefono, correo, estado, id_tipo_usuario
            FROM usuarios WHERE id = %s
        """, (id,))
        usuario = cursor.fetchone()
    conexion.close()
    return usuario

def actualizar_usuario(id, numdocumento, apellidos, nombres, telefono, correo, estado, id_tipo_usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE usuarios 
            SET numdocumento = %s, apellidos = %s, nombres = %s, telefono = %s, 
                correo = %s, estado = %s, id_tipo_usuario = %s 
            WHERE id = %s
        """, (numdocumento, apellidos, nombres, telefono, correo, estado, id_tipo_usuario, id))
    conexion.commit()
    conexion.close()
