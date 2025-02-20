from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class RegisterForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Length(min=6, message='Le mot de passe doit contenir au moins 6 caractères')
    ])
    password2 = PasswordField(
        'Répéter le mot de passe', validators=[
            DataRequired(),
            EqualTo('password', message='Les mots de passe doivent correspondre')
        ]
    )
    submit = SubmitField('S\'inscrire')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cette adresse email est déjà utilisée.')

class ContactForm(FlaskForm):
    name = StringField('Nom', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Le nom doit contenir entre 2 et 100 caractères')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Veuillez entrer une adresse email valide')
    ])
    subject = StringField('Sujet', validators=[
        DataRequired(),
        Length(min=5, max=200, message='Le sujet doit contenir entre 5 et 200 caractères')
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=10, message='Le message doit contenir au moins 10 caractères')
    ])
    submit = SubmitField('Envoyer')
