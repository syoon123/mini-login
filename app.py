from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
@app.route("/login") #multiple routes go to same function
def login():
    return render_template('form.html', title = 'Login')

@app.route("/authenticate/", methods=['POST'])
def auth():
    correctuser = 'sarah'
    correctpass = 'pass1234'
    if request.form['user'] == correctuser and request.form['pass'] == correctpass:
        m = 'Login successful'
    else:
        m = 'Login failed'        
    return render_template('message.html', msg = m) 

if __name__ == '__main__':
    app.debug = True
    app.run()
