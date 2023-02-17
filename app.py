import sqlite3
from flask import Flask, request, render_template, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password'
app.config['MYSQL_DB'] = 'disposableemail'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emailTest', methods=['POST'])
def emailTest():
    #connection = sqlite3.connect('DisposableEmail.db')
    #cursor = connection.cursor()
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        email = request.form.get('email')
        e1 = email.split('@')
        e = e1[1]
        cursor.execute('select * from disposableEmail where emailDomain = %s', ([e]))
        result = cursor.fetchone()
        if result:
            return render_template('success.html', data = str(e))
        else:
            return ' <h3>Legit email domain </h3><b>' + e + "</b>&nbsp;&nbsp;<a href="+url_for('index')+">Home</a>"

@app.route('/saveDomain', methods=['POST'])
def saveDomain():
    #connection = sqlite3.connect('DisposableEmail.db')
    #cursor = connection.cursor()
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        email = request.form.get('email')
        cursor.execute('insert into disposableEmail(emailDomain) values(%s)', ([email]))
        mysql.connection.commit()
        return render_template('thankyou.html')
    else:
        return ' <h3>Taking you back.</h3><b>'  + "</b>&nbsp;&nbsp;<a href="+url_for('index')+">Home</a>"
    connection.close()


if __name__ == "__main__":
    app.run()
