from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,Response 
from clases import clase_categoria as clscat
from controladores import controlador_categoria,controlador_dashboard,controlador_tipo_usuario,controlador_detallepresentacion,controlador_envio,controlador_genero,controlador_grupoedad,controlador_marca,controlador_transaccion,controlador_presentacion,controlador_producto,controlador_tipoproducto,controlador_usuario, controlador_distrito, controlador_departamento, controlador_provincia
import os, json
app = Flask(__name__)

@app.route('/ini')
def ini():
    return  render_template('maestra.html')

@app.route('/acerca_de')
def acerca_de():
    return render_template('/acerca_de.html')


#-----INICIO-USUARIO-----#
@app.route("/inicio_sesion")
def inicio_sesion():
    email = request.form['email']
    password = request.form['password']

@app.route("/registrar_usuario")
def registrar_usuario():
    try:
        nombre = request.form['nombre']
        ape_paterno = request.form['ape_paterno']
        ape_materno = request.form['ape_materno']
        email = request.form['email']
        password = request.form['password']
        return
    except:
        raise
#-----FIN-USUARIO-----#


#-----INICIO-CATEGORIA-----#
@app.route('/categoria')
def categoria():
    categorias = controlador_categoria.obtener_categorias()
    return render_template('categoria.html', categorias=categorias)

@app.route('/registrar_categoria')
def registrar_categoria():
    return render_template('registrar_categoria.html')

@app.route('/insertar_categoria', methods=['POST'])
def insertar_categoria():
    categoria = request.form['nombre']
    controlador_categoria.insertar_categoria(
        categoria=categoria
    )
    return redirect(url_for('categoria'))

@app.route('/eliminar_categoria/<int:id>')
def eliminar_categoria(id):
    controlador_categoria.eliminar_categoria(id)
    return redirect(url_for('categoria'))

@app.route('/modificar_categoria', methods=['POST'])
def modificar_categoria():
    id = request.form['id']
    categoria = controlador_categoria.obtener_categoria_por_id(id)
    return render_template('modificar_categoria.html', categoria=categoria)

@app.route('/actualizar_categoria', methods=['POST'])
def actualizar_categoria():
    id = request.form['id']
    categoria = request.form['categoria']
    controlador_categoria.actualizar_categoria(id, categoria)
    return redirect(url_for('categoria'))
#------FIN-CATEGORIA-----#

#-----INICIO-MARCA-----#

@app.route('/marca')
def marca():
    marcas = controlador_marca.obtener_marcas()
    return render_template('marca.html', marcas=marcas)

@app.route('/registrarmarca')
def registrar_marca():
    return render_template('registrar_marca.html')

@app.route('/insertar_marca', methods=['POST'])
def insertar_marca():
    marca = request.form['marca']
    controlador_marca.insertar_marca(marca)
    return redirect(url_for('marca'))

@app.route('/eliminar_marca/<int:id>')
def eliminar_marca(id):
    controlador_marca.eliminar_marca(id)
    return redirect(url_for('marca'))

#anggelo el def de marca era modificar_marca
@app.route('/modificar_marca', methods=['POST'])
def modificar_marca():
    id = request.form['id']
    marca = controlador_marca.obtener_marca_por_id(id)
    return render_template('modificar_marca.html', marca=marca)

@app.route('/actualizarmarca', methods=['POST'])
def actualizar_marca():
    id = request.form['id']
    marca = request.form['marca']
    controlador_marca.actualizar_marca(id,marca)
    return redirect('marca')
#-----FIN-MARCA-----#

#-----INICIO-PRODUCTO-----#
@app.route('/producto')
def producto():
    productos = controlador_producto.obtener_productos()
    return render_template('producto.html', productos=productos)


@app.route('/registrarproducto')
def registrarproducto():
    datos = {
        'tipo_productos' : controlador_tipoproducto.nombres_tipoproducto(),
        'generos': controlador_genero.nombre_generos(),
        'marcas': controlador_marca.nombre_marcas(),
        'categorias': controlador_categoria.nombre_categorias(),
        'grupo_edad': controlador_grupoedad.nombres_grupo_edad(),
    }
    return render_template('registrar_producto.html', **datos )


@app.route('/insertar_producto', methods=['POST'])
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
    id_tipopr = controlador_tipoproducto.obtener_id_por_nombre(tipo_producto)  
    genero = request.form['genero']
    id_genero = controlador_genero.id_genero_por_nombre(genero)
    marca = request.form['marca']
    id_marca = controlador_marca.id_marca_por_nombre(marca)
    categoria = request.form['categoria']
    id_categoria = controlador_categoria.id_categoria_por_nombre(categoria)
    grupoedad = request.form['grupoedad']
    id_grupo_edad = controlador_grupoedad.id_grupo_edad_por_nombre(grupoedad)

    imagen_producto = request.files['imagen_producto']

    ruta_carpeta = "./static/img"
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    nombre_imagen = imagen_producto.filename
    ruta_anidada = os.path.join(ruta_carpeta, nombre_imagen)  

    imagen_producto.save(ruta_anidada)
    controlador_producto.insertar_producto(nombre, precio, estado, descripcion, descuento, id_tipopr, id_genero, id_marca, id_categoria, id_grupo_edad, nombre_imagen)
    
    return redirect(url_for('producto'))
    
@app.route('/registrar_detallepresentacion')
def registrar_detallepresentacion():
    productos = controlador_producto.produ()
    presentaciones = controlador_presentacion.obtener_presentaciones()
    return render_template("registrar_detallepresentacion.html", productos = productos, presentaciones=presentaciones)

@app.route('/eliminar_producto/<int:id>')
def eliminar_producto(id):
    controlador_producto.eliminar_producto(id)
    return redirect(url_for('producto'))


@app.route('/insertar_detallepresentacion', methods=['POST'])
def insertar_detallepresentacion():
    # Obtener los datos del formulario
    producto_id = request.form['producto']
    presentacion_id = request.form['presentacion']
    stock = request.form['stock']
    #Recuerda poner los mensajes de validacion
    try:
         controlador_detallepresentacion.insertar_detalle(producto_id, presentacion_id, stock) 
    except:
        return redirect(url_for('registrar_detallepresentacion'))
    return redirect(url_for('registrar_detallepresentacion'))

@app.route('/modificar_producto', methods=['POST'])
def modificar_producto():
    id = request.form['id_pr']
    datos = {
        'tipo_productos' : controlador_tipoproducto.nombres_tipoproducto(),
        'generos': controlador_genero.nombre_generos(),
        'marcas': controlador_marca.nombre_marcas(),
        'categorias': controlador_categoria.nombre_categorias(),
        'grupo_edad': controlador_grupoedad.nombres_grupo_edad(),
    }
    pr = list(controlador_producto.obtener_producto_por_id(id))
    return render_template('modifiar_producto.html', **datos, pr=pr)

@app.route('/modificar_detallepresentacion', methods=['POST'])
def modificar_detallepresentacion():
    idpre = request.form['idpre']
    idpro = request.form['idpro']   
    datos = {
        'productos' : controlador_producto.obtener_producto_por_id(idpro),
        'presentaciones': controlador_presentacion.obtener_presentacion_por_id(idpre),
    }
    pr = list(controlador_detallepresentacion.obtener_dp(idpre,idpro))
    return render_template('modificar_detallepresentacion.html', **datos, pr=pr)


@app.route('/actualizar_detallepresentacion', methods=['POST'])
def actualizar_detallepresentacion():
    idpre = request.form['id_pre']
    idpro = request.form['id_pro']  
    stock = request.form['stock']
    controlador_detallepresentacion.actualizar_detallepre(idpre,idpro,stock)
    return redirect(url_for('detallepresentacion'))

@app.route('/actualizar_producto', methods=['POST'])
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
    id_tipopr = controlador_tipoproducto.obtener_id_por_nombre(tipo_producto)
    genero = request.form['genero']
    id_genero = controlador_genero.id_genero_por_nombre(genero)
    marca = request.form['marca']
    id_marca = controlador_marca.id_marca_por_nombre(marca)
    categoria = request.form['categoria']
    id_categoria = controlador_categoria.id_categoria_por_nombre(categoria)
    grupoedad = request.form['grupoedad']
    id_grupo_edad = controlador_grupoedad.id_grupo_edad_por_nombre(grupoedad)
    controlador_producto.actualizar_producto(id_producto, nombre, precio, estado, descripcion, descuento, id_tipopr, id_genero, id_marca, id_categoria, id_grupo_edad, enlace_imagen)
    return redirect(url_for('producto'))

#-----FIN-PRODUCTO-----#

#-------INICIO-TIPO PRODUCTO-----#
@app.route('/tipo_producto')
def tipo_producto():
    tipos_productos = controlador_tipoproducto.obtener_tipoproducto()
    return render_template('tipo_producto.html', tipos_productos = tipos_productos)

@app.route('/registrar_tipoproducto')
def registrar_tipoproducto():
    return render_template('registrar_tipoproducto.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html')


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

@app.route('/insertar_tipoproducto', methods=['POST'])
def insertar_tipo_proucto():
    tipo = request.form['tipo']
    descripcion= request.form['descripcion']
    controlador_tipoproducto.insertar_tipoproducto(tipo,descripcion)
    return redirect('tipo_producto')

@app.route('/eliminar_tipoproducto/<int:id>')
def eliminar_tipoproducto(id):
    controlador_tipoproducto.eliminar_tipoproducto(id)
    return redirect(url_for('tipo_producto'))

#modifique el def antes era modificar_tipo_producto
@app.route('/modificar_tipoproducto', methods=['POST'])
def modificar_tipoproducto():
    id = request.form['id']
    tipo_producto = controlador_tipoproducto.obtener_tipoproducto_id(id)
    return render_template('modificar_tipoproducto.html', tipo_producto = tipo_producto)

@app.route('/actualizar_tipoproducto', methods=['POST'])
def actualizar_tipoproducto():
    id = request.form['id']
    tipo = request.form['tipo']
    descripcion = request.form['descripcion']
    controlador_tipoproducto.actualizar_tipoproducto(id,tipo,descripcion)
    return redirect('tipo_producto')
#-----FIN-TIPO PRODUCTO-----#

#----PRESENTACION-----#
@app.route('/presentacion')
def presentacion():
    presentaciones = controlador_presentacion.obtener_presentaciones()
    return render_template('presentacion.html', presentaciones=presentaciones)

@app.route('/registrar_presentacion')
def registrar_presentacion():
    return render_template('registrar_presentacion.html')

@app.route('/insertar_presentacion', methods=['POST'])
def insertar_presentacion():
    color = request.form['color']
    talla = request.form['talla']
    controlador_presentacion.insertar_presentacion(color, talla)
    return redirect(url_for('presentacion'))

@app.route('/eliminar_presentacion/<int:id>')
def eliminar_presentacion(id):
    controlador_presentacion.eliminar_presentacion(id)
    return redirect(url_for('presentacion'))

@app.route('/modificar_presentacion', methods=['POST'])
def modificar_presentacion():
    id = request.form['id']
    presentacion = controlador_presentacion.obtener_presentacion_por_id(id)
    return render_template('modificar_presentacion.html', presentacion=presentacion)

@app.route('/actualizar_presentacion', methods=['POST'])
def actualizar_presentacion():
    id = request.form['id']
    color = request.form['color']
    talla = request.form['talla']
    controlador_presentacion.actualizar_presentacion(id, color, talla)
    return redirect(url_for('presentacion'))
#-----FIN-PRESENTACION-----#

#-----INICIO-GRUPO EDAD-----#
@app.route('/grupo_edad')
def grupo_edad():
    grupos_edad = controlador_grupoedad.obtener_grupo_edad()
    return render_template('grupoedad.html', grupos_edad=grupos_edad)

@app.route('/registrargrupoedad')
def registrargrupoedad():
    return render_template('registrar_grupoedad.html')

@app.route('/insertar_grupo_edad', methods=['POST'])
def insertar_grupo_edad():
    grupo_edad = request.form['grupo_edad']
    controlador_grupoedad.insertar_grupo_edad(grupo_edad)
    return redirect(url_for('grupo_edad'))

@app.route('/eliminar_grupo_edad/<string:id>')
def eliminar_grupo_edad(id):
    controlador_grupoedad.eliminar_grupo_edad(id)
    return redirect(url_for('grupo_edad'))
#anggelo mofique el def era modificar_grupo_edad
@app.route('/modificar_grupoedad', methods=['POST'])
def modificar_grupoedad():
    id = request.form['id']
    grupo_edad = controlador_grupoedad.obtener_grupo_edad_id(id)
    return render_template('modificar_grupoedad.html', grupo_edad=grupo_edad)

@app.route('/actualizar_grupo_edad', methods=['POST'])
def actualizar_grupo_edad():
    id = request.form['id']
    grupo_edad = request.form['grupo_edad']
    controlador_grupoedad.actualizar_grupo_edad(id, grupo_edad)
    return redirect(url_for('grupo_edad'))
#-----FIN-GRUPO EDAD-----#

#-----INICIO-GENERO-----#
@app.route('/genero')
def genero():
    generos = controlador_genero.obtener_generos()
    return render_template('genero.html', generos=generos)


@app.route('/detallepresentacion')
def detallepresentacion():
    dprs = controlador_detallepresentacion.listar_detalleproducto()
    return render_template('detalle_presentacion.html', dprs=dprs )

@app.route('/registrargenero')
def registrargenero():
    return render_template('registrar_genero.html')

@app.route('/insertar_genero', methods=['POST'])
def insertar_genero():
    genero = request.form['genero']
    controlador_genero.insertar_genero(genero)
    return redirect(url_for('genero'))

@app.route('/eliminar_genero/<int:id>')
def eliminar_genero(id):
    controlador_genero.eliminar_genero(id)
    return redirect(url_for('genero'))

@app.route('/modificar_genero', methods=['POST'])
def modificar_genero():
    id = request.form['id']
    genero = controlador_genero.obtener_genero_por_id(id)
    return render_template('modificar_genero.html', genero=genero)

@app.route('/actualizar_genero', methods=['POST'])
def actualizar_genero():
    id = request.form['id']
    genero = request.form['genero']
    controlador_genero.actualizar_genero(id, genero)
    return redirect(url_for('genero'))

#-----FIN-GENERO-----#

#-----INICIO DEPARTAMENTO-----#
@app.route('/departamento')
def departamento():
    departamento = controlador_departamento.obtener_departamentos()
    return render_template('departamento.html', departamentos=departamento)

@app.route('/registrar_departamento')
def registrar_departamento():
    return render_template('registrar_departamento.html')

@app.route('/insertar_departamento', methods=['POST'])
def insertar_departamento():
    departamento = request.form['departamento']
    controlador_departamento.insertar_departamento(departamento)
    return redirect(url_for('departamento'))

@app.route('/eliminar_departamento/<int:id>')
def eliminar_departamento(id):
    controlador_departamento.eliminar_departamento(id)
    return redirect(url_for('departamento'))

@app.route('/modificar_departamento', methods=['POST'])
def modificar_departamento():
    id = request.form['id']
    departamento = controlador_departamento.obtener_departamento_por_id(id)
    return render_template('modificar_departamento.html', departamento = departamento)

@app.route('/actualizar_departamento', methods=['POST'])
def actualizar_departamento():
    id = request.form['id']
    departamento = request.form['departamento']
    controlador_departamento.actualizar_departamento(id, departamento, )
    return redirect(url_for('departamento'))
#-----FIN DEPARTAMENTO-----#

#-----INICIO PROVINCIA-----#
@app.route('/provincia')
def provincia():
    provincia = controlador_provincia.obtener_provincia()
    return render_template('provincia.html', provincias = provincia)

@app.route('/registrar_provincia')
def registrar_provincia():
    departamentos = controlador_departamento.obtener_departamentos()
    return render_template('registrar_provincia.html', departamentos=departamentos)

@app.route('/insertar_provincia', methods=['POST'])
def insertar_provincia():
    provincia = request.form['provincia']
    departamento = int(request.form['departamento'])
    controlador_provincia.insertar_provincia(provincia,departamento)
    return redirect(url_for('provincia'))

@app.route('/eliminar_provincia/<int:id>')
def eliminar_provincia(id):
    controlador_provincia.eliminar_provincia(id)
    return redirect(url_for('provincia'))

@app.route('/modificar_provincia', methods=['POST'])
def modificar_provincia():
    id = request.form['id']
    departamentos = controlador_departamento.obtener_departamentos()
    provincia = controlador_provincia.obtener_provincia_por_id(id)
    return render_template('modificar_provincia.html', provincia = provincia, departamentos = departamentos)

@app.route('/actualizar_provincia', methods=['POST'])
def actualizar_provincia():
    id = request.form['id']
    provincia = request.form['provincia']
    departamento = request.form['departamento']
    id_departamento = controlador_departamento.id_departamento_por_nombre(departamento)
    controlador_provincia.actualizar_provincia(id , provincia , id_departamento)
    return redirect(url_for('provincia'))
#-----FIN PROVINCIA-----#

#-----INICIO DISTRITO-----#
@app.route('/distrito')
def distrito():
    distrito = controlador_distrito.obtener_distrito()
    return render_template('distrito.html', distritos = distrito)

@app.route('/registrar_distrito')
def registrar_distrito():
    provincias = controlador_provincia.obtener_provincia()
    return render_template('registrar_distrito.html', provincias = provincias)

@app.route('/insertar_distrito', methods=['POST'])
def insertar_distrito():
    distrito = request.form['distrito']
    provincia = int(request.form['provincia'])
    controlador_distrito.insertar_distrito(distrito,provincia)
    return redirect(url_for('distrito'))

@app.route('/eliminar_distrito/<int:id>')
def eliminar_distrito(id):
    controlador_distrito.eliminar_distrito(id)
    return redirect(url_for('distrito'))

@app.route('/modificar_distrito', methods=['POST'])
def modificar_distrito():
    id = request.form['id']
    distrito = controlador_distrito.obtener_distrito_por_id(id)
    return render_template('modificar_distrito.html', distrito = distrito)

@app.route('/actualizar_distrito', methods=['POST'])
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
    return redirect(url_for('registrarprovincia'))

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


if __name__ ==  '__main__':
    app.run(debug=5000)