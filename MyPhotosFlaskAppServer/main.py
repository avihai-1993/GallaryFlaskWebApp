
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy,Model
import os
import uuid


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class User(db.Model):
    userName = db.Column(db.String(200), primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    def __init__(self,user,pwd):
        self.userName=user
        self.password = pwd

class Pics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(200),nullable=False)
    pic = db.Column(db.String(250), nullable=False)
    def __init__(self,user,pic):
        self.userName=user
        self.pic = pic

UPLOAD_FOLDER = 'static/pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#run one time For Creating The DB
db.create_all()

@app.route("/")
def home():
    return render_template('login.html')


@app.route('/MyPhotos' , methods=['POST'])
def phtos():
    user = request.form['userName']
    pwd =  request.form['password']
    u = User.query.filter_by(userName=user).first()
    if u is None or u.password != pwd:
        return redirect('/MyPhotos/'+user)
    else:
        newU = User(user,pwd)
        db.session.add(newU)
        db.session.commit()
        return redirect('/MyPhotos/'+user)

def getAllPhtosOfUser(user):
   return Pics.query.filter_by(userName=user).all()

@app.route('/MyPhotos/<user>' , methods=['GET'])
def phtosUser(user:str):
    ph = getAllPhtosOfUser(user)
    o = []
    for p in ph:
        o.append(p.pic)


    return render_template('MyPhotos.html',phtos=o,user=user)


@app.route('/addPhtos/<user>' , methods=['POST'])
def addPhto(user):
    for file in request.files.getlist("file[]"):
        filename = str(uuid.uuid4()) + ".jpg"
        #save File Name to table
        p = Pics(user,"/pics/"+filename)
        db.session.add(p)
        db.session.commit()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect('/MyPhotos/'+user)




if __name__ == "__main__":
    app.run('localhost',8000,debug=True)