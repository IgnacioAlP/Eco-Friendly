from bd import obtener_conexion

def cinco_productos_mas_vendidos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute('''select pr.nombre, sum(dp.subtotal) as subtotal  from producto pr inner join detalle_pedido dp
        on dp.id_producto = pr.id
        group by pr.nombre
        order by pr.nombre DESC
        LIMIT 5;''')
        productos = cursor.fetchall()
    conexion.close()
    return productos

def get_prconmasprecio():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute('''select producto.precio, producto.nombre from producto order by precio desc LIMIT 5;''')
        productos = cursor.fetchall()
    conexion.close()
    return productos

def cinco_productos_mas_costosos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute('''select pr.nombre, sum(dp.subtotal) as subtotal  from producto pr inner join detalle_pedido dp
        on dp.id_producto = pr.id
        group by pr.nombre
        order by pr.nombre DESC
        LIMIT 5;''')
        productos = cursor.fetchall()
    conexion.close()
    return productos

def sash():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute('''select * from departamento;;''')
        productos = cursor.fetchall()
    conexion.close()
    return productos