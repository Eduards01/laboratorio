import re
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.datastructures import ImmutableDict

app = Flask(__name__)

#mysql database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'laboratorio'
mysql = MySQL(app)

app.secret_key='mysecretkey'


#################### USUARIOS ###############################
@app.route('/')
def index():
    cursor =  mysql.connection.cursor()
    cursor.execute('select * from usuarios')
    data = cursor.fetchall()
    return render_template('index.html',contactos=data)
    #return 'Index - Diseño de software'

@app.route('/portal', methods=['POST'])
def acceso():

    cursor = mysql.connection.cursor()
    cursor.execute('select * from usuarios')
    data = cursor.fetchall()

    if request.method == 'POST':
        if request.form['submit'] == 'login':
            login = request.form['usuario']
            contraseña = request.form['contraseña']

            for x in range(len(data)):
                if data[x][3] == login:
                    if data[x][4] == contraseña:
                        print("Ingreso Exitoso")
                        if data[x][5] == 'alumno':
                            return render_template('alumno.html', usuarios = data)
                        if data[x][5] == 'profesor':
                            return render_template('profesor.html', usuarios = data)
            
        if request.form['submit'] == 'registrar':  
            return render_template('registro.html')
        return redirect(url_for('index'))

@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        login = request.form['login']
        clave = request.form['clave']
        tipo = request.form['tipo']

        cur = mysql.connection.cursor()
        cur.execute('insert usuarios(codigo,nombres,login,clave,tipo) values(%s,%s,%s,%s,%s)',(codigo,nombre,login,clave,tipo))
        mysql.connection.commit()
        return redirect(url_for('index'))
    return 'Usuario'

if __name__ == "__main__":
    app.run(port=4000, debug=True, use_reloader=True)