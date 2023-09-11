from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
# from app import create_app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(),'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# app = create_app()
db = SQLAlchemy(app)


class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        # print(request.form['title'])
        title= request.form['title']
        description= request.form['desc']
        if(len(title) !=0 and len(description)!=0):
            todo = ToDo(title = title, desc= description)
            db.session.add(todo)
            db.session.commit()
    allToDo = ToDo.query.all()
    # print(allToDo)
    return render_template('index.html',allToDo=allToDo )

# @app.route('/show')
# def update():
#     allToDo = ToDo.query.all()
#     # print(allToDo)
#     return 'this is products page'
 
@app.route('/delete/<int:sno>')
def deleteRec(sno):
    print("inside delete")
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    # print(allToDo)
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET','POST'])
def updateRec(sno):
    print("inside update")
    if request.method == 'POST':
        title= request.form['title']
        description= request.form['desc']
        if(len(title) !=0 and len(description)!=0):
            todo = ToDo.query.filter_by(sno=sno).first()
            todo.title = title
            todo.desc = description
            db.session.add(todo)
            db.session.commit()
        return redirect("/")

    todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo )

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
