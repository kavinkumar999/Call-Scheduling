import os
import bottle
from bottle import route, run, post, Response
from twilio import twiml
from twilio.rest import Client
from flask import Flask,render_template,request,redirect
from flaskext.mysql import MySQL
import pymysql

app=Flask(__name__)
mysql=pymysql.connect(host='localhost', user='root', password="Admin@123", db='db', charset='utf8', port=3306)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin@123'
app.config['MYSQL_DB'] = 'db'
twilio_client = Client('ACd404100b29e7d4c052c0cf232cb01d31' , '0acfff53a5b6effff6f9cda41ccd53ae')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '+16178198712')

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        detail=request.form
        name=detail['Name']
        phone=detail['phone']
        print(name,phone)
        cur=mysql.cursor()
        cur.execute("INSERT INTO user(name,phone) VALUES(%s,%s)",(name,phone))
        mysql.commit()
        cur.close()
        return redirect('/user')
    
    return render_template('index.html')


@app.route('/user',methods=["GET", "POST"])
def user():
    if request.method == "POST":
        jet=request.form
        callno=jet['subject']
        if len(callno)==10:
            return redirect("/dial/"+"+91"+callno)
        else:
            return "<h1>number is not correct</h1>"
    cur=mysql.cursor()
    ans=cur.execute("SELECT * FROM user")
    if ans >0 :
         userform=cur.fetchall()
         return render_template('user.html',userform=userform)

@app.errorhandler(Exception)
def handle_exception(e):
    return "hanging"

@app.route('/dial/<nume>')
def outbound_call(nume):
    try:
        twilio_client.calls.create(to=nume,
                               from_=TWILIO_NUMBER,
                               twiml='<Response><Say>hai kavin how are you</Say></Response>')
    except TypeError:
        print("ringing")
    return '<h1>phone is ringing</h1>'

if __name__ == '__main__':
    app.run(debug=True)
