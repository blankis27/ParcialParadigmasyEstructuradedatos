#!/usr/bin/env python
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import csv

from forms import LoginForm, SaludarForm, RegistrarForm

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'un string que funcione como llave'
#Funciones auxiliares-----------------------------------------------------------
def listClientes() :
    lista_clientes=[] 
    with open('archivo.csv') as archivo :
        arch_csv = csv.DictReader(archivo)
        arch_dic = list(arch_csv)
        for l in arch_dic :
            if l['CLIENTE'] not in lista_clientes :
               lista_clientes.append(l['CLIENTE'])
    return lista_clientes 
#Funcion Auxiliar-------------------------------------------------------------------------------
def listProducto():
    lista_productos=[]
    with open('archivo.csv') as archivo:
        arch_csv = csv.DictReader(archivo)
        productodic= list(arch_csv)
        for l in productodic :
            if l['PRODUCTO'] not in lista_productos :
               lista_productos.append(l['PRODUCTO'])
        return lista_productos


#Estas class son para el logueo------------------------------------------------------------------------------ 
class MiFormulario(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = StringField('Password:')

#Esta class son para el registro de usuario-------------------------------------------------------------------
class RegForm(FlaskForm):
    usuario = StringField('Username:', validators=[DataRequired()])
    password = StringField('Password:', validators=[DataRequired()])
    repassword = StringField('Enter password again:', validators=[DataRequired()])

<<<<<<< HEAD
#Consultas-----------------------------------------------------------------------------------------

  
class ConsultasForm(FlaskForm):
    autocompletar = StringField('autocompletar', validators=[DataRequired()])
    enviar = SubmitField('Buscar')
=======
>>>>>>> 227eec2f60f3290af5c1c6ef201955276cdab622

#Esta @app llama a la pagina principal-------------------------------------------------------------------------
@app.route('/index')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())


#usuario
@app.route('/usuario', methods =['GET', 'POST'])
def saludar():
    mi_formulario = MiFormulario()
    if mi_formulario.validate_on_submit():
        return "Funciono"
    return render_template('usuario.html', form=mi_formulario)


#Este @app es de productos-----------------------------------------------------------------------------------------------------

@app.route('/productos')
def productos():
    
    with open ('archivo.csv') as f:
        reader = csv.reader(f) #(csvfile)
        next(reader)
        lista = list(reader)
    return render_template('productos.html',lista=lista)#archivo_csv = archivo_csv, ,#cliente=cliente
<<<<<<< HEAD
=======

#consultas listar productos que compro un cliente----------------------------------------------------------------------------
@app.route('/clientes')
def clientes():
    with open('archivo.csv') as f:
        reader = csv.reader(f)
        cliente = 'FARMACIA NUEVA CHINGOLO'
        producto = []    
        for line in reader:
            if line [2] == cliente:
                producto.append(line[1])
    return render_template('clientes.html', producto=producto, cliente=cliente)

#listar todos los determinados clientes que compraron un determinado producto----------------------------------------------------------
@app.route('/ProductosClientes')
def producto():
    with open ('archivo.csv') as f:
        reader = csv.reader(f)
        producto = 'ALIVIOL3400' 
        #archivo_csv = csv.reader(csvfile)
        cliente = []
        #lista = list(reader)
        for line in archivo_csv:
            if line [1] == producto:
                cliente.append(line[2])
    return render_template('compras.html',producto=producto, cliente=cliente)  
  
>>>>>>> 227eec2f60f3290af5c1c6ef201955276cdab622

# cliente por producto----------------------------------------------------------------------------
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    consultasForm = ConsultasForm()
    listaClientes = []
    with open('archivo.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            if line[2] not in listaClientes:
                listaClientes.append(line[2])
    if consultasForm.autocompletar.data in listaClientes:
        cliente = consultasForm.autocompletar.data
        #print(cliente)
        #print("hola")
        with open('archivo.csv') as f:
            reader = csv.reader(f)
            resultados = []    
            for line in reader:
                if line[2] == cliente:
                    resultados.append(line)
        return render_template('clientes.html',form=consultasForm, listaClientes=listaClientes, resultados=resultados)
    return render_template('clientes.html',form=consultasForm, listaClientes=listaClientes)

#producto por cliente----------------------------------------------------------
@app.route('/ProductoCliente', methods=['GET', 'POST'])
def producto():
    consultasForm = ConsultasForm()
    listaProductos = []
    with open('archivo.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            if line[1] not in listaProductos:
                listaProductos.append(line[1])
    if consultasForm.autocompletar.data in listaProductos:
        producto = consultasForm.autocompletar.data
        with open('archivo.csv') as f:
            reader = csv.reader(f)
            resultados = []    
            for line in reader:
                if line[1] == producto:
                    resultados.append(line)
        return render_template('ProductoCliente.html',form=consultasForm, listaProductos=listaProductos, resultados=resultados)
    return render_template('ProductoCliente.html',form=consultasForm, listaProductos=listaProductos)

#Productos Mas Vendidos-----------------------------------------------------------------------------
@app.route("/MasVendidos", methods = ('GET', 'POST'))
def ProducMasVendidos(): 
    lista_de_producto = listProducto()
    productos_mas_vendidos = []
    producto = []
    lista = []
    for lisProduc in lista_de_producto:
        totalCant = 0
        with open('archivo.csv') as f:
            reader = csv.DictReader(f)
            produc = list (reader)
            for productos in produc:
                if lisProduc == productos['PRODUCTO']:
                    producto_total = float(productos ['CANTIDAD'])
                    totalCant =  producto_total + totalCant
        productos_mas_vendidos.append([totalCant, lisProduc])
    cont = 1
    productos_mas_vendidos.sort(reverse = True)
    for datos in  productos_mas_vendidos:
        if cont <=5:
            lista.append(datos)
        cont = cont + 1
    lista.sort(reverse = True)
        
    
    return render_template('MasVendidos.html', productos_mas_vendidos = lista) 
            


#Mejores Cliente--------------------------------------------------------------------------------------------------------------
@app.route("/Compras", methods = ('GET', 'POST'))
def MejoresClietes():    
    lista_clientes = listClientes()
    cliente_mas_gasto = []
    lista = []
    for liscliente in lista_clientes:
        totalgasto= 0
        with open('archivo.csv') as f:
            reader = csv.DictReader(f)
            listado = list (reader)
            for clientes in listado :
                if liscliente == clientes['CLIENTE']:
                    gasto = float(clientes['CANTIDAD']) * float(clientes['PRECIO'])
                    totalgasto = totalgasto + gasto
        cliente_mas_gasto.append([totalgasto, liscliente])
    cont = 1
    cliente_mas_gasto.sort(reverse = True)
    for datos in cliente_mas_gasto:
        if cont <=5:
            lista.append(datos)
        cont = cont + 1
    lista.sort(reverse = True)
        
    return render_template('compras.html', cliente_mas_gasto = lista) 

<<<<<<< HEAD
    
       
#para el login-------------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    testform = MiFormulario()
    if testform.validate_on_submit():
        user_password = [testform.name.data, testform.password.data]
        with open('usuarios.csv', newline='') as f:
            filereader = csv.reader(f)
            found = False
            for row in filereader:
                if user_password == row:
                    found = True
                    session['username'] = testform.name.data
                    return redirect('/index')
            if found is False:
                return 'Incorrect username or password.<br><a href="/login"> Back to Login </a>'
    return render_template('login.html', form=testform, username=session.get('username'))

=======
#Ingresar es Precios-----------------------------------------------------------------------------------------------------------
@app.route('/precios', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('precios.html')#, formulario=formulario)
>>>>>>> 227eec2f60f3290af5c1c6ef201955276cdab622

#Esta @app es para registrarse------------------------------------------------------------------------------------------------
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
<<<<<<< HEAD
    formulario = RegForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.repassword.data:
=======
    formulario = RegistrarForm()
    if formulario.validate_on_s-ubmit():
        if formulario.password.data == formulario.password_check.data:
>>>>>>> 227eec2f60f3290af5c1c6ef201955276cdab622
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
     
<<<<<<< HEAD
    return render_template('registrar.html',form=formulario)
=======
    return render_template('registrar.html'), form=formulario)

>>>>>>> 227eec2f60f3290af5c1c6ef201955276cdab622


#Para desloguearte-----------------------------------------------------------------------
@app.route('/logout', methods=['GET']) 
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
<<<<<<< HEAD
        return redirect(url_for('index'))


#Estos dos son para los errores----------------------------------------------------------------------
=======
        return redirect(url_for('index')


#Estos dos @app son para los errores----------------------------------------------------------------------
>>>>>>> 227eec2f60f3290af5c1c6ef201955276cdab622
@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)


