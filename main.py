from flask import Flask, render_template, request, url_for, session
from werkzeug.utils import redirect
from flask import Flask,render_template,request
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
# data base
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    class User(UserMixin, db.Model):
        __tablename__ = 'User'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        score = db.Column(db.Integer)

    class College(UserMixin, db.Model):
        __tablename__ = 'College    '
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        score = db.Column(db.Integer)

    db.session.commit()
    db.create_all()
class MyModelView(ModelView):
    def is_accessible(self):

            return True
admin = Admin(app)
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(College, db.session))

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        user = User.query.all()
        collges=College.query.all()

        final=[]
        for i in user:
            if i.name == name and i.password == password:
                user_score=i.score
                print(user_score)
                print(collges)
                for c in collges:
                    print(c.score)
                    if c.score<= user_score:
                        final.append(c)


                return render_template("college.html",items=final)
        return redirect("/register")
    return render_template("login.html")
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
      name=request.form.get("name")
      password=request.form.get("password")
      score=request.form.get("score")
      new=User(
          name=name,
          password=password,
          score=score,
      )

      db.session.add(new)
      db.session.commit()
      return redirect("/login")
    return render_template("register.html", )

if __name__==("__main__"):
    app.run(debug=True)