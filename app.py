#!/usr/bin/env python
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import csv
from forms import LoginForm, SaludarForm, RegistrarForm

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'un string que funcione como llave'


#Estas class son para el logueo------------------------------------------------------------------------------ 
class MiFormulario(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = StringField('Password:')

#Esta class son para el registro de usuario-------------------------------------------------------------------
class RegForm(FlaskForm):
    name = StringField('Username:', validators=[DataRequired()])
    password = StringField('Password:', validators=[DataRequired()])
    repassword = StringField('Enter password again:', validators=[DataRequired()])


#Esta @app llama a la pagina principal-------------------------------------------------------------------------
@app.route('/')
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

#Esta @app es para registrarse------------------------------------------------------------------------------------------------
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_s-ubmit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
     
    return render_template('registrar.html'), form=formulario)


@app.route('/secret', methods=['GET'])
def secreto():
    if 'username' in session:
        return render_template('private.html')#, username=session['username'])
    """else:
        return render_template('sin_permiso.html')"""

@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index')


#Estos dos @app son para los errores----------------------------------------------------------------------
@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)


