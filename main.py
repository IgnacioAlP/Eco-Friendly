from flask import Flask, render_template, request, redirect, url_for
from controladores import controlador_categoria,controlador_marca 
app = Flask(__name__)

@app.route('/ini')
def ini():
    return  render_template('maestra.html')


@app.route('/inicio')
def index():
    return render_template('/templates/index.html')


@app.route('/acerca_de')
def acerca_de():
    return render_template('/templates/acerca_de.html')


#-------CATEGORIA------#
@app.route('/categoria')
def categoria():
    categorias = controlador_categoria.obtener_categorias()
    return render_template('categoria.html', categorias=categorias)

@app.route('/registrar_categoria')
def registrar_categoria():
    return render_template('registrar_categoria.html')

@app.route('/insertar_categoria', methods=['POST'])
def insertar_categoria():
    categoria = request.form['categoria']
    controlador_categoria.insertar_categoria(categoria)
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


#-------MARCA------#

@app.route('/marca')
def marca():
    marcas = controlador_marca.obtener_marcas()
    return render_template('marca.html', marcas=marcas)

@app.route('/registrarmarca')
def registrarmarca():
    return render_template('registrar_marca.html')

@app.route('/insertarmarca', methods=['POST'])
def insertar_marca():
    marca = request.form['marca']
    controlador_marca.insertar_marca(marca)
    return redirect('registrarmarca')

@app.route('/eliminarmarca/<int:id>')
def eliminar_marca(id):
    controlador_marca.eliminar_marca(id)
    return redirect(url_for('marca'))

#anggelo el def de marca era modificar_marca
@app.route('/modificarmarca', methods=['POST'])
def modificarmarca():
    id = request.form['id']
    marca = controlador_marca.obtener_marca_por_id(id)
    return render_template('modificar_marca.html', marca=marca)

@app.route('/actualizarmarca', methods=['POST'])
def actualizar_marca():
    id = request.form['id']
    marca = request.form['marca']
    controlador_marca.actualizar_marca(id,marca)
    return redirect('marca')

if __name__ ==  '__main__':
    app.run(debug=5000)