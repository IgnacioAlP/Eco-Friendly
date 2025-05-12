from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,Response 
from clases import clase_categoria as clscat
from controladores import controlador_categoria
from controladores import controlador_dashboard
from controladores import controlador_tipo_usuario
from controladores import controlador_detalle_presentacion
from controladores import controlador_envio
from controladores import controlador_genero
from controladores import controlador_grupo_edad
from controladores import controlador_marca
from controladores import controlador_transaccion
from controladores import controlador_presentacion
from controladores import controlador_producto
from controladores import controlador_tipo_producto
from controladores import controlador_usuario
from controladores import controlador_distrito
from controladores import controlador_departamento
from controladores import controlador_provincia
import os, json

app = Flask(__name__)

#---RUTAS FIJAS---#

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/acerca_de')
def acerca_de():
    return render_template('/templates/acerca_de.html')

@app.route('/libro_de_reclamaciones')
def libro_de_reclamaciones():
    return render_template('/templates/libro_de_reclamaciones.html')




@app.route('/monto_envio/<string:departamento>/<string:provincia>/<string:distrito>', methods=['POST'])
def monto_envio(departamento, provincia, distrito):
    dato = controlador_envio.direccion_envio(distrito, provincia, departamento)
    return jsonify(dato)
    

@app.route('/preguntas_frecuentes')
def preguntas_frecuentes():
    return render_template('/templates/centrodeayuda.html')

@app.route('/registro_de_usuario')
def registro_de_usuario():
    return render_template('/templates/registrar.html')

@app.route('/ubicanos')
def ubicanos():
    return render_template('/templates/ubicanos.html')

###############################


###############################




##--NO TOCASDE AQUI HACIA ABAJO--#

#-----INICIO-USUARIO-----#
@app.route("/inicio_sesion")
def inicio_sesion():
    return render_template('categoria.html')

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    tipo = request.form["tipo"]
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    dni = request.form["dni"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    contraseña = request.form["contraseña"]
    usuario = ''
    estado = "Activo"
    controlador_usuario.insertar_usuario(dni, apellidos, nombre, telefono, email, usuario, contraseña, estado, tipo)

    return redirect('/ini')
#-----FIN-USUARIO-----#


#-----INICIO-CATEGORIA-----#
@app.route('/dashboard/resumen')
def resumen():
    return render_template('/dashboard/resumen.html')

@app.route('/dashboard/categoria')
def categoria():
    categorias = controlador_categoria.obtener_categorias()
    return render_template('dashboard/categoria.html', categorias=categorias)

@app.route('/dashboard/registrar_categoria')
def registrar_categoria():
    return render_template('dashboard/registrar_categoria.html')

@app.route('/dashboard/insertar_categoria', methods=['POST'])
def insertar_categoria():
    categoria = request.form['categoria']
    controlador_categoria.insertar_categoria(
        categoria=categoria
    )
    return redirect(url_for('categoria'))

@app.route('/dashboard/eliminar_categoria/<int:id>')
def eliminar_categoria(id):
    controlador_categoria.eliminar_categoria(id)
    return redirect(url_for('categoria'))

@app.route('/dashboard/modificar_categoria', methods=['POST'])
def modificar_categoria():
    id = request.form['id']
    categoria = controlador_categoria.obtener_categoria_por_id(id)
    return render_template('dashboard/modificar_categoria.html', categoria=categoria)

@app.route('/dashboard/actualizar_categoria', methods=['POST'])
def actualizar_categoria():
    id = request.form['id']
    categoria = request.form['categoria']
    controlador_categoria.actualizar_categoria(id, categoria)
    return redirect(url_for('categoria'))
#------FIN-CATEGORIA-----#

#-----INICIO-MARCA-----#

@app.route('/dashboard/marca')
def marca():
    marcas = controlador_marca.obtener_marcas()
    return render_template('/dashboard/marca.html', marcas=marcas)

@app.route('/dashboard/registrar_marca')
def registrar_marca():
    return render_template('/dashboard/registrar_marca.html')

@app.route('/dashboard/insertar_marca', methods=['POST'])
def insertar_marca():
    marca = request.form['marca']
    controlador_marca.insertar_marca(marca)
    return redirect(url_for('marca'))

@app.route('/dashboard/eliminar_marca/<int:id>')
def eliminar_marca(id):
    controlador_marca.eliminar_marca(id)
    return redirect(url_for('marca'))


@app.route('/dashboard/modificar_marca', methods=['POST'])
def modificar_marca():
    id = request.form['id']
    marca = controlador_marca.obtener_marca_por_id(id)
    return render_template('/dashboard/modificar_marca.html', marca=marca)


@app.route('/actualizarmarca', methods=['POST'])
def actualizar_marca():
    id = request.form['id']
    marca = request.form['marca']
    controlador_marca.actualizar_marca(id,marca)
    return redirect('marca')
#-----FIN-MARCA-----#

#-----INICIO-PRODUCTO-----#
@app.route('/dashboard/producto')
def producto():
    productos = controlador_producto.obtener_productos()
    return render_template('/dashboard/producto.html', productos=productos)


@app.route('/dashboard/registrar_producto')
def registrar_producto():
    datos = {
        'tipo_productos' : controlador_tipo_producto.nombres_tipo_producto(),
        'generos': controlador_genero.nombre_generos(),
        'marcas': controlador_marca.nombre_marcas(),
        'categorias': controlador_categoria.nombre_categorias(),
        'grupo_edad': controlador_grupo_edad.nombres_grupo_edad(),
    }
    return render_template('/dashboard/registrar_producto.html', **datos )


@app.route('/dashboard/insertar_producto', methods=['POST'])
def insertar_producto():
    nombre = request.form['nombre']
    precio = request.form['precio']
    estado = request.form['estado']
    if estado == "Activo":
        estado = 'A'
    else:
        estado = 'I'
    descripcion = request.form['descripcion']
    descuento = request.form['descuento']
    tipo_producto = request.form['tipo_producto']
    id_tipopr = controlador_tipo_producto.obtener_id_por_nombre(tipo_producto)  
    genero = request.form['genero']
    id_genero = controlador_genero.id_genero_por_nombre(genero)
    marca = request.form['marca']
    id_marca = controlador_marca.id_marca_por_nombre(marca)
    categoria = request.form['categoria']
    id_categoria = controlador_categoria.id_categoria_por_nombre(categoria)
    grupo_edad = request.form['grupo_edad']
    id_grupo_edad = controlador_grupo_edad.id_grupo_edad_por_nombre(grupo_edad)

    imagen_producto = request.files['imagen_producto']

    ruta_carpeta = "./static/img"
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    nombre_imagen = imagen_producto.filename
    ruta_anidada = os.path.join(ruta_carpeta, nombre_imagen)  

    imagen_producto.save(ruta_anidada)
    controlador_producto.insertar_producto(nombre, precio, estado, descripcion, descuento, id_tipopr, id_genero, id_marca, id_categoria, id_grupo_edad, nombre_imagen)
    
    return redirect(url_for('producto'))
    
@app.route('/dashboard/registrar_detalle_presentacion')
def registrar_detalle_presentacion():
    productos = controlador_producto.produ()
    presentaciones = controlador_presentacion.obtener_presentaciones()
    return render_template("/dashboard/registrar_detalle_presentacion.html", productos = productos, presentaciones=presentaciones)

@app.route('/dashboard/eliminar_producto/<int:id>')
def eliminar_producto(id):
    controlador_producto.eliminar_producto(id)
    return redirect(url_for('producto'))


@app.route('/dashboard/insertar_detalle_presentacion', methods=['POST'])
def insertar_detalle_presentacion():
    # Obtener los datos del formulario
    producto_id = request.form['producto']
    presentacion_id = request.form['presentacion']
    stock = request.form['stock']
    #Recuerda poner los mensajes de validacion
    try:
         controlador_detalle_presentacion.insertar_detalle(producto_id, presentacion_id, stock) 
    except:
        return redirect(url_for('registrar_detalle_presentacion'))
    return redirect(url_for('registrar_detalle_presentacion'))

@app.route('/dashboard/modificar_producto', methods=['POST'])
def modificar_producto():
    id = request.form['id_pr']
    datos = {
        'tipo_productos' : controlador_tipo_producto.nombres_tipo_producto(),
        'generos': controlador_genero.nombre_generos(),
        'marcas': controlador_marca.nombre_marcas(),
        'categorias': controlador_categoria.nombre_categorias(),
        'grupo_edad': controlador_grupo_edad.nombres_grupo_edad(),
    }
    pr = list(controlador_producto.obtener_producto_por_id(id))
    return render_template('/dashboard/modifiar_producto.html', **datos, pr=pr)

@app.route('/dashboard/modificar_detalle_presentacion', methods=['POST'])
def modificar_detalle_presentacion():
    idpre = request.form['idpre']
    idpro = request.form['idpro']   
    datos = {
        'productos' : controlador_producto.obtener_producto_por_id(idpro),
        'presentaciones': controlador_presentacion.obtener_presentacion_por_id(idpre),
    }
    pr = list(controlador_detalle_presentacion.obtener_dp(idpre,idpro))
    return render_template('/dashboard/modificar_detalle_presentacion.html', **datos, pr=pr)


@app.route('/dashboard/actualizar_detalle_presentacion', methods=['POST'])
def actualizar_detalle_presentacion():
    idpre = request.form['id_pre']
    idpro = request.form['id_pro']  
    stock = request.form['stock']
    controlador_detalle_presentacion.actualizar_detallepre(idpre,idpro,stock)
    return redirect(url_for('detalle_presentacion'))

@app.route('/dashboard/actualizar_producto', methods=['POST'])
def actualizar_producto():
    id_producto = request.form['id']
    nombre = request.form['nombre']
    precio = request.form['precio']
    estado = request.form['estado']
    imagen_pr1 = request.form.get('imagen_producto')
    imagen_pr2 = request.files['imagen_producto2']
    if (imagen_pr2.filename != ""):
        #Imgresamos imagen
        ruta = "/static/img"
        n_ruta = os.path.join(ruta,imagen_pr2.filename)
        imagen_pr2.save(n_ruta)
        enlace_imagen = imagen_pr2.filename
    else:
        enlace_imagen = imagen_pr1     
    if estado == "Activo":
        estado = 'A'
    else:
        estado = 'I'

    descripcion = request.form['descripcion']
    descuento = request.form['descuento']
    tipo_producto = request.form['tipo_producto']
    id_tipopr = controlador_tipo_producto.obtener_id_por_nombre(tipo_producto)
    genero = request.form['genero']
    id_genero = controlador_genero.id_genero_por_nombre(genero)
    marca = request.form['marca']
    id_marca = controlador_marca.id_marca_por_nombre(marca)
    categoria = request.form['categoria']
    id_categoria = controlador_categoria.id_categoria_por_nombre(categoria)
    grupo_edad = request.form['grupo_edad']
    id_grupo_edad = controlador_grupo_edad.id_grupo_edad_por_nombre(grupo_edad)
    controlador_producto.actualizar_producto(id_producto, nombre, precio, estado, descripcion, descuento, id_tipopr, id_genero, id_marca, id_categoria, id_grupo_edad, enlace_imagen)
    return redirect(url_for('producto'))

#-----FIN-PRODUCTO-----#

#-------INICIO-TIPO PRODUCTO-----#
@app.route('/dashboard/tipo_producto')
def tipo_producto():
    tipos_productos = controlador_tipo_producto.obtener_tipo_producto()
    return render_template('/dashboard/tipo_producto.html', tipos_productos = tipos_productos)

@app.route('/dashboard/registrar_tipo_producto')
def registrar_tipo_producto():
    return render_template('/dashboard/registrar_tipo_producto.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/olddashboard.html')


@app.route('/getprconmas')
def getprconmas():
    datos = controlador_dashboard.get_prconmasprecio()
    da = []
    for data in datos:
        objData = {
            "precio": data[0],
            "nombre": data[1]
        }
        da.append(objData)
    return jsonify(da)


@app.route('/s5pmv')
def s5pmv():
    productos = controlador_dashboard.cinco_productos_mas_vendidos()
    nombres = list()
    valores = list()
    for pr in productos:
        nombres.append(pr[0])
        valores.append(pr[1])
    
    s5pmv= {
        "nombres": nombres,
        "valores" : valores
    }
    return jsonify(s5pmv)

@app.route('/dashboard/insertar_tipo_producto', methods=['POST'])
def insertar_tipo_producto():
    tipo = request.form['tipo']
    descripcion= request.form['descripcion']
    controlador_tipo_producto.insertar_tipo_producto(tipo,descripcion)
    return redirect('tipo_producto')

@app.route('/dashboard/eliminar_tipo_producto/<int:id>')
def eliminar_tipo_producto(id):
    controlador_tipo_producto.eliminar_tipo_producto(id)
    return redirect(url_for('tipo_producto'))

#modifique el def antes era modificar_tipo_producto
@app.route('/dashboard/modificar_tipo_producto', methods=['POST'])
def modificar_tipo_producto():
    
    id = request.form['id']
    tipo_producto = controlador_tipo_producto.obtener_tipo_producto_id(id)
    return render_template('/dashboard/modificar_tipo_producto.html', tipo_producto = tipo_producto)

@app.route('/dashboard/actualizar_tipo_producto', methods=['POST'])
def actualizar_tipo_producto():
    id = request.form['id']
    tipo = request.form['tipo']
    descripcion = request.form['descripcion']
    controlador_tipo_producto.actualizar_tipo_producto(id,tipo,descripcion)
    return redirect('tipo_producto')
#-----FIN-TIPO PRODUCTO-----#

#----PRESENTACION-----#
@app.route('/dashboard/presentacion')
def presentacion():
    presentaciones = controlador_presentacion.obtener_presentaciones()
    return render_template('/dashboard/presentacion.html', presentaciones=presentaciones)

@app.route('/dashboard/registrar_presentacion')
def registrar_presentacion():
    return render_template('/dashboard/registrar_presentacion.html')

@app.route('/dashboard/insertar_presentacion', methods=['POST'])
def insertar_presentacion():
    color = request.form['color']
    talla = request.form['talla']
    controlador_presentacion.insertar_presentacion(color, talla)
    return redirect(url_for('presentacion'))

@app.route('/dashboard/eliminar_presentacion/<int:id>')
def eliminar_presentacion(id):
    controlador_presentacion.eliminar_presentacion(id)
    return redirect(url_for('presentacion'))

@app.route('/dashboard/modificar_presentacion', methods=['POST'])
def modificar_presentacion():
    id = request.form['id']
    presentacion = controlador_presentacion.obtener_presentacion_por_id(id)
    return render_template('/dashboard/modificar_presentacion.html', presentacion=presentacion)

@app.route('/dashboard/actualizar_presentacion', methods=['POST'])
def actualizar_presentacion():
    id = request.form['id']
    color = request.form['color']
    talla = request.form['talla']
    controlador_presentacion.actualizar_presentacion(id, color, talla)
    return redirect(url_for('presentacion'))
#-----FIN-PRESENTACION-----#

#-----INICIO-GRUPO EDAD-----#
@app.route('/dashboard/grupo_edad')
def grupo_edad():
    grupos_edad = controlador_grupo_edad.obtener_grupo_edad()
    return render_template('/dashboard/grupo_edad.html', grupos_edad=grupos_edad)

@app.route('/dashboard/registrar_grupo_edad')
def registrar_grupo_edad():
    return render_template('/dashboard/registrar_grupo_edad.html')

@app.route('/dashboard/insertar_grupo_edad', methods=['POST'])
def insertar_grupo_edad():
    grupo_edad = request.form['grupo_edad']
    controlador_grupo_edad.insertar_grupo_edad(grupo_edad)
    return redirect(url_for('grupo_edad'))

@app.route('/dashboard/eliminar_grupo_edad/<string:id>')
def eliminar_grupo_edad(id):
    controlador_grupo_edad.eliminar_grupo_edad(id)
    return redirect(url_for('grupo_edad'))

#anggelo mofique el def era modificar_grupo_edad
@app.route('/dashboard/modificar_grupo_edad', methods=['POST'])
def modificar_grupo_edad():
    id = request.form['id']
    grupo_edad = controlador_grupo_edad.obtener_grupo_edad_id(id)
    return render_template('/dashboard/modificar_grupo_edad.html', grupo_edad=grupo_edad)

@app.route('/dashboard/actualizar_grupo_edad', methods=['POST'])
def actualizar_grupo_edad():
    id = request.form['id']
    grupo_edad = request.form['grupo_edad']
    controlador_grupo_edad.actualizar_grupo_edad(id, grupo_edad)
    return redirect(url_for('grupo_edad'))
#-----FIN-GRUPO EDAD-----#

#-----INICIO-GENERO-----#
@app.route('/dashboard/genero')
def genero():
    generos = controlador_genero.obtener_generos()
    return render_template('/dashboard/genero.html', generos=generos)


@app.route('/dashboard/detalle_presentacion')
def detalle_presentacion():
    dprs = controlador_detalle_presentacion.listar_detalleproducto()
    return render_template('/dashboard/detalle_presentacion.html', dprs=dprs )

@app.route('/dashboard/registrar_genero')
def registrar_genero():
    return render_template('/dashboard/registrar_genero.html')

@app.route('/dashboard/insertar_genero', methods=['POST'])
def insertar_genero():
    genero = request.form['genero']
    controlador_genero.insertar_genero(genero)
    return redirect(url_for('genero'))

@app.route('/dashboard/eliminar_genero/<int:id>')
def eliminar_genero(id):
    controlador_genero.eliminar_genero(id)
    return redirect(url_for('genero'))

@app.route('/dashboard/modificar_genero', methods=['POST'])
def modificar_genero():
    id = request.form['id']
    genero = controlador_genero.obtener_genero_por_id(id)
    return render_template('/dashboard/modificar_genero.html', genero=genero)

@app.route('/dashboard/actualizar_genero', methods=['POST'])
def actualizar_genero():
    id = request.form['id']
    genero = request.form['genero']
    controlador_genero.actualizar_genero(id, genero)
    return redirect(url_for('genero'))

#-----FIN-GENERO-----#

#-----INICIO DEPARTAMENTO-----#
@app.route('/dashboard/departamento')
def departamento():
    departamento = controlador_departamento.obtener_departamentos()
    return render_template('/dashboard/departamento.html', departamentos=departamento)

@app.route('/dashboard/registrar_departamento')
def registrar_departamento():
    return render_template('/dashboard/registrar_departamento.html')

@app.route('/dashboard/insertar_departamento', methods=['POST'])
def insertar_departamento():
    departamento = request.form['departamento']
    controlador_departamento.insertar_departamento(departamento)
    return redirect(url_for('departamento'))

@app.route('/dashboard/eliminar_departamento/<int:id>')
def eliminar_departamento(id):
    controlador_departamento.eliminar_departamento(id)
    return redirect(url_for('departamento'))

@app.route('/dashboard/modificar_departamento', methods=['POST'])
def modificar_departamento():
    id = request.form['id']
    departamento = controlador_departamento.obtener_departamento_por_id(id)
    return render_template('/dashboard/modificar_departamento.html', departamento = departamento)

@app.route('/dashboard/actualizar_departamento', methods=['POST'])
def actualizar_departamento():
    id = request.form['id']
    departamento = request.form['departamento']
    controlador_departamento.actualizar_departamento(id, departamento, )
    return redirect(url_for('departamento'))
#-----FIN DEPARTAMENTO-----#

#-----INICIO PROVINCIA-----#
@app.route('/dashboard/provincia')
def provincia():
    provincia = controlador_provincia.obtener_provincia()
    return render_template('/dashboard/provincia.html', provincias = provincia)

@app.route('/dashboard/registrar_provincia')
def registrar_provincia():
    departamentos = controlador_departamento.obtener_departamentos()
    return render_template('/dashboard/registrar_provincia.html', departamentos=departamentos)

@app.route('/dashboard/insertar_provincia', methods=['POST'])
def insertar_provincia():
    provincia = request.form['provincia']
    departamento = int(request.form['departamento'])
    controlador_provincia.insertar_provincia(provincia,departamento)
    return redirect(url_for('provincia'))

@app.route('/dashboard/eliminar_provincia/<int:id>')
def eliminar_provincia(id):
    controlador_provincia.eliminar_provincia(id)
    return redirect(url_for('provincia'))

@app.route('/dashboard/modificar_provincia', methods=['POST'])
def modificar_provincia():
    id = request.form['id']
    departamentos = controlador_departamento.obtener_departamentos()
    provincia = controlador_provincia.obtener_provincia_por_id(id)
    return render_template('/dashboard/modificar_provincia.html', provincia = provincia, departamentos = departamentos)

@app.route('/dashboard/actualizar_provincia', methods=['POST'])
def actualizar_provincia():
    id = request.form['id']
    provincia = request.form['provincia']
    departamento = request.form['departamento']
    id_departamento = controlador_departamento.id_departamento_por_nombre(departamento)
    controlador_provincia.actualizar_provincia(id , provincia , id_departamento)
    return redirect(url_for('provincia'))
#-----FIN PROVINCIA-----#

#-----INICIO DISTRITO-----#
@app.route('/dashboard/distrito')
def distrito():
    distrito = controlador_distrito.obtener_distrito()
    return render_template('/dashboard/distrito.html', distritos = distrito)

@app.route('/dashboard/registrar_distrito')
def registrar_distrito():
    provincias = controlador_provincia.obtener_provincia()
    return render_template('/dashboard/registrar_distrito.html', provincias = provincias)

@app.route('/dashboard/insertar_distrito', methods=['POST'])
def insertar_distrito():
    distrito = request.form['distrito']
    provincia = int(request.form['provincia'])
    controlador_distrito.insertar_distrito(distrito,provincia)
    return redirect(url_for('distrito'))

@app.route('/dashboard/eliminar_distrito/<int:id>')
def eliminar_distrito(id):
    controlador_distrito.eliminar_distrito(id)
    return redirect(url_for('distrito'))

@app.route('/dashboard/modificar_distrito', methods=['POST'])
def modificar_distrito():
    id = request.form['id']
    distrito = controlador_distrito.obtener_distrito_por_id(id)
    return render_template('/dashboard/modificar_distrito.html', distrito = distrito)

@app.route('/dashboard/actualizar_distrito', methods=['POST'])
def actualizar_distrito():
    id = request.form['id']
    distrito = request.form['distrito']
    provincia = int(request.form['provincia'])
    controlador_distrito.actualizar_distrito(id, distrito, provincia)
    return redirect(url_for('distrito'))
#-----FIN DISTRITO-----#
## ---rutas para retornar provincias
@app.route('/retornar_provincias/<string:departamento>')
def retornar_provincias(departamento):
    id_departamento = controlador_departamento.id_departamento_por_nombre(departamento)
    provincias = controlador_provincia.nombre_provinciasxdepartamento(id_departamento)
    return  jsonify(provincias)

## ---rutas para retornar distritos
@app.route('/retornar_distritos/<string:provincia>')
def retornar_distritos(provincia):
    distritos = controlador_provincia.id_provincia_por_nombre(provincia)
    return  jsonify(distritos)

@app.route('/insertar_provincia', methods=['POST'])
def insertar_provincia_route():
    provincia = request.form['provincia']
    id_departamento = request.form['departamento']
    insertar_provincia(provincia, id_departamento)
    return redirect(url_for('registrar_provincia'))

@app.route('/mostrar')
def mostrar():
    valores = controlador_dashboard.sash()
    lista_vl = []

    for valor in valores :
        obj = {
            "id" :  valor[0],
            "departamento" : valor[1]
        }
        lista_vl.append(obj)
    return jsonify(lista_vl)


##-----INICIO ENVIO--------
@app.route('/dashboard/envio')
def envio():
    return redirect(url_for('distrito'))

##------FIN ENVIO-------


##-----INICIO PEDIDO--------
@app.route('/dashboard/pedido')
def pedido():
    return redirect(url_for('distrito'))

##------FIN PEDIDO-------


##-----INICIO COMPROBANTE--------
@app.route('/dashboard/comprobante')
def comprobante():
    return redirect(url_for('distrito'))

##------FIN COMPROBANTE-------

##-----INICIO USUARIO--------
@app.route('/dashboard/usuario')
def usuario():
    usuario = controlador_usuario.obtener_usuarios()
    return render_template('/dashboard/usuario.html', usuarios=usuario)

## Solo el mismo usuario puede registra una cuenta
# @app.route('/dashboard/registrar_usuario')
# def registrar_departamento():
#     return render_template('/dashboard/registrar_departamento.html')
#
# @app.route('/dashboard/insertar_departamento', methods=['POST'])
# def insertar_departamento():
#     departamento = request.form['departamento']
#     controlador_departamento.insertar_departamento(departamento)
#     return redirect(url_for('departamento'))

@app.route('/dashboard/suspender_usuario', methods=['POST'])
def suspender_estado_usuario():
    id = request.form['new_id']
    controlador_usuario.suspender_usuario(id)
    return redirect(url_for('usuario'))

@app.route('/dashboard/eliminar_usuario/<int:id>')
def eliminar_usuario(id):
    controlador_usuario.eliminar_usuario(id)
    return redirect(url_for('departamento'))

@app.route('/dashboard/modificar_usuario', methods=['POST'])
def modificar_usuario():
    id = request.form['id']
    usuario = controlador_usuario.obtener_usuario_por_id(id)
    return render_template('/dashboard/modificar_usuario.html', usuario = usuario)

@app.route('/dashboard/actualizar_usuario', methods=['POST'])
def actualizar_usuario():
    id = request.form['id']
    departamento = request.form['usuario']
    controlador_usuario.actualizar_usuario(id,  )
    return redirect(url_for('usuario'))
##------FIN USUARIO-------

if __name__ ==  '__main__':
    app.run(debug=5000)