import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
import requests
from models import db, User, Message
from forms import LoginForm, RegisterForm, ContactForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# API endpoint for getting random quotes
QUOTE_API_URL = "https://api.quotable.io/random"

def get_random_quote():
    try:
        response = requests.get(QUOTE_API_URL)
        if response.status_code == 200:
            data = response.json()
            return data['content'], data['author']
    except:
        pass
    return "La connaissance est le pouvoir.", "Francis Bacon"

@app.route('/')
def home():
    quote, author = get_random_quote()
    return render_template('index.html', quote=quote, author=author)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nom d\'utilisateur ou mot de passe invalide')
            return redirect(url_for('login'))
        
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Félicitations, vous êtes maintenant inscrit !')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/ciel')
def ciel():
    quote, author = get_random_quote()
    return render_template('ciel.html', quote=quote, author=author)

@app.route('/snir')
def snir():
    quote, author = get_random_quote()
    return render_template('snir.html', quote=quote, author=author)

@app.route('/etudes-sup')
def etudes_sup():
    quote, author = get_random_quote()
    return render_template('etudes-sup.html', quote=quote, author=author)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = Message(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(message)
        db.session.commit()
        flash('Votre message a été envoyé avec succès !')
        return redirect(url_for('contact'))
    
    quote, author = get_random_quote()
    return render_template('contact.html', form=form, quote=quote, author=author)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
