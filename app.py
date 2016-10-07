from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import csv
app = Flask(__name__)

app.secret_key = '\xab\xa8\xb5o\x17\xc6\xda_+\xd7\xfe\xd0}\xd253\x90k\x9c\rGv\x02\x83w\xcc\x1b\xf0 Rdr'

@app.route("/")
def home():
    for user in session:
        return redirect(url_for('auth'))
    return redirect(url_for('login'))

@app.route("/welcome/")
def welcome():
    return render_template('message.html', title = 'Welcome', user = session['user'])

@app.route("/login/") #multiple routes go to same function
def login():
    return render_template('home.html', title = 'Login')

@app.route("/logout/", methods=['POST'])
def logout():
    if request.form['enter'] == 'Logout':
        session.pop('user')
        print "popped"
    return redirect(url_for('login'))

@app.route("/authenticate/", methods=['POST'])
def auth():
    username = request.form['user']
    password = hashlib.sha512(request.form['pass']).hexdigest()
    session['user'] = username

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
            return redirect(url_for('welcome'))
        
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
