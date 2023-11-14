from flask import Flask, request,render_template, redirect,session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, login_required,LoginManager
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError,InputRequired
from flask_bcrypt import Bcrypt

DATABASE_USER='root'
DATABASE_PASSWORD=''
DATABASE_HOST='localhost'
DATABASE_NAME='flask_lkm_new_db'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SECRET_KEY'] = 'thisisasecretkey'
#db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable =False)
    password = db.Column(db.String(100), nullable =False)

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired()],
                        render_kw={"placeholder": "Email"})
    password = StringField(validators=[InputRequired()],
                        render_kw={"placeholder":" Password"})
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(),
                        EqualTo('password', message='Passwords must match.')],
                        render_kw={"placeholder":" Retype Password"})
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired()],
                        render_kw={"placeholder":"Email"})
    password = StringField(validators=[InputRequired()],
                        render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")

with app.app_context():
    db.create_all()
    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                session['user_id'] = user.id
                flash('Login successful!', 'success')    
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "POST":
        new_email = request.form["email"]
        new_password = request.form["password"]

        validate_user = User.query.filter_by(email=new_email).first()

        if validate_user:
            flash("An account with this Email already exist, Please try with another one.", "danger")
        else:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            new_user = User(email=new_email, password= hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
