#!/usr/bin/env python
from datetime import datetime
from flask import Flask, render_template, redirect, flash, session
#from flask import Flask, render_template, redirect, flash, session, url_for, #flash
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


#Estas class son para el logueo 
class MiFormulario(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = StringField('Password:')

#Esta class son para el registro de usuario
class RegForm(FlaskForm):
    name = StringField('Username:', validators=[DataRequired()])
    password = StringField('Password:', validators=[DataRequired()])
    repassword = StringField('Enter password again:', validators=[DataRequired()])
    

#Esta @app llama a la pagina principal
@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())

#Saludar es lista de clientes-------------------------------------------------------------------------------------
@app.route('/clientes', methods=['GET', 'POST'])
def saludar():
    """formulario = SaludarForm()
    if formulario.validate_on_submit():
        print(formulario.usuario.name)
        return redirect(url_for('saludar_persona', usuario=formulario.usuario.data))"""
    return render_template('clientes.html')#, form=formulario)


#Este @app es de productos-----------------------------------------------------------------------------------------------------

@app.route('/productos')
def proctos():
    return render_template('productos.html')#, nombre=usuario)


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

#Esta @app es para registrarse
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    """formulario = RegistrarForm()
    if formulario.validate_on_s-ubmit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')"""
    return render_template('registrar.html')#, form=formulario)


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
    """else:
        return redirect(url_for('index'))"""


#Estos dos @app son para los errores
@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)


