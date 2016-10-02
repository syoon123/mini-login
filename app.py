from flask import Flask, render_template, request
import hashlib
import csv
app = Flask(__name__)

@app.route("/")
@app.route("/login") #multiple routes go to same function
def login():
    return render_template('home.html', title = 'Login')

@app.route("/authenticate/", methods=['POST'])
def auth():
    username = request.form['user']
    password = hashlib.sha512(request.form['pass']).hexdigest()

    if request.form['enter'] == 'Register':
        if existingAcct(username, password):
            return render_template('home.html', title = 'Register Failed', existing_acct = True)
        else:
            createAcct(username, password)
            return render_template('home.html', title = 'New Account Created', successful_register = True)
        

    if request.form['enter'] == 'Login':
        if checkAcct(username, password) == False:
            return render_template('home.html', title = 'Login Failed', login = False)
        else:
            return render_template('message.html', title = 'Welcome', user = username)

def existingAcct(username, password):
    d = csv.reader( open("data/passwords.csv") )
    for i in d:
        if username == i[0]:
            return True
    return False

def checkAcct(username, password):
    d = csv.reader( open("data/passwords.csv") )
    for i in d:
        if username == i[0]:
            if password == i[1]:
                return True
    return False

def createAcct(username, password):
    with open("data/passwords.csv", 'a') as f:
        w = csv.writer(f)
        w.writerow([username, password])

if __name__ == '__main__':
    app.debug = True
    app.run()
