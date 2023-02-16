import sqlite3
from flask import Flask, request, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emailTest', methods=['POST'])
def emailTest():
    connection = sqlite3.connect('DisposableEmail.db')
    cursor = connection.cursor()
    if request.method == 'POST':
        email = request.form.get('email')
        e1 = email.split('@')
        e = e1[1]
        cursor.execute('select * from disposableEmail where emailDomain = ?', ([e]))
        result = cursor.fetchone()
        if result:
            return ' <h3>Dispoable email domain </h3><b>' + e + "</b>&nbsp;&nbsp;<a href="+url_for('index')+">Home</a>"
        else:
            return ' <h3>Legit email domain </h3><b>' + e + "</b>&nbsp;&nbsp;<a href="+url_for('index')+">Home</a>"

@app.route('/saveDomain', methods=['POST'])
def saveDomain():
    connection = sqlite3.connect('DisposableEmail.db')
    cursor = connection.cursor()
    if request.method == 'POST':
        email = request.form.get('email')
        cursor.execute('insert into disposableEmail(emailDomain) values(?)', ([email]))
        connection.commit()
        return ' <h3>Domain recorded.</h3><b>'+"</b>&nbsp;&nbsp;<a href="+url_for('index')+">Home</a>"
    else:
        return ' <h3>Taking you back.</h3><b>'  + "</b>&nbsp;&nbsp;<a href="+url_for('index')+">Home</a>"
    connection.close()


if __name__ == "__main__":
    app.run()
