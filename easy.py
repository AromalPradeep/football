# DBMS PROJECT : FOOTBALL MANAGEMENT LIVE
# MEMBERS : AJEED, ANNAMMA, AROMAL, DAN, JIBIN

# DESCRIPTION
# Lorem ipsum dolor sit amet consectetur, adipisicing elit.                    

# imports

# flask
from flask import Flask, render_template
app = Flask(__name__)

# functions

# links

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/profile')
def profile():
    return "hello profile world"

@app.route('/manage')
def manage():
    return render_template("manage.html")

@app.route('/transfer')
def transfer():
    return "hello transfer world"

@app.route('/signup')
def signup():
    return "hello signup world"

@app.route('/login')
def login():
    return "hello login world"

# main
if __name__ == '__main__':
    app.debug = True
    app.run()