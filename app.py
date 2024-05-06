from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = "secret_key"
db = SQLAlchemy(app)

class User(db.Model):
    first_name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    username = db.Column(db.String, primary_key = True, nullable = False)
    password = db.Column(db.String, nullable = False)

@app.route('/', methods=['GET','POST'])
def login():
    if(request.method == 'GET'):
        return render_template('index.html',message = '')
    else:
        data = request.form
        user = db.session.query(User).filter_by(username = data['username']).first()
        if(user):
            if(user.password == data['password']):
                session['username'] = user.username
                return render_template('user_page.html',name = user.first_name)
            else:
                return render_template('index.html',message = 'Incorrect password !')
        else:
            return render_template('index.html',message = 'Username not found !')

@app.route('/sign_up', methods = ['GET','POST'])
def sign_up():
    if(request.method == 'GET'):
        return render_template('sign_up.html',message = '')
    else:
        data = request.form
        user = db.session.query(User).filter_by(username = data['username']).first()
        if(user):
            return render_template('sign_up.html',message = 'Username already exists !')
        else:
            new_user = User(first_name = data['first_name'],email = data['email'],username = data['username'],password = data['password'])
            db.session.add(new_user)
            db.session.commit()
            return render_template('index.html',message = 'Registration successful !')

@app.route('/logout',methods = ['GET'])
def logout():
    username = session.pop('username', None)
    return render_template('index.html',message = f'{username} logged out successfully !')
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)