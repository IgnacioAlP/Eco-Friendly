from flask import Flask, render_template, request, redirect, url_for
from controladores import controlador_categoria
from controladores import controlador_marca
from controladores import controlador_producto
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

@app.route('/registrar_producto')
def registrar_producto():
    return render_template('registrar_producto.html')

@app.route('/insertar_producto', methods=['POST'])
def insertar_producto():
    nombre = request.form['nombre']
    precio = request.form['precio']
    estado = request.form['estado']
    stock = request.form['stock']
    descripcion = request.form['descripcion']
    descuento = request.form['descuento']
    id_tipo_producto = request.form['id_tipo_producto']
    id_genero = request.form['id_genero']
    id_marca = request.form['id_marca']
    id_categoria = request.form['id_categoria']
    id_grupo_edad = request.form['id_grupo_edad']
    id_presentacion = request.form['id_presentacion']
    controlador_producto.insertar_producto(
        nombre=nombre,
        precio=precio,
        estado=estado,
        stock=stock,
        descripcion=descripcion,
        descuento=descuento,
        id_tipo_producto=id_tipo_producto,
        id_genero=id_genero,
        id_marca=id_marca,
        id_categoria=id_categoria,
        id_grupo_edad=id_grupo_edad,
        id_presentacion=id_presentacion
    )
    return redirect(url_for('producto'))

@app.route('/eliminar_producto/<int:id>')
def eliminar_producto(id):
    controlador_producto.eliminar_producto(id)
    return redirect(url_for('producto'))

#Falta modificar
@app.route('/modificar_producto', methods=['POST'])
def modificar_producto():
    id = request.form['id']
    producto = controlador_producto.obtener_producto_por_id(id)
    return render_template('modificar_producto.html', producto=producto)

@app.route('/actualizar_producto', methods=['POST'])
def actualizar_producto():
    id = request.form['id']
    producto = request.form['producto']
    controlador_producto.actualizar_producto(id, producto)
    return redirect(url_for('producto'))
#-----FIN-PRODUCTO-----#










if __name__ ==  '__main__':
    app.run(debug=5000)