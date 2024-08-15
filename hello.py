from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os


# Configurações do Mailgun
app.config['MAILGUN_API_KEY'] = os.environ.get('MAILGUN_API_KEY')
app.config['MAILGUN_DOMAIN'] = os.environ.get('MAILGUN_DOMAIN')
app.config['MAILGUN_FROM_EMAIL'] = 'seu_email@seudominio.com'  # Email que enviará as mensagens

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


def send_email(to, subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{app.config['MAILGUN_DOMAIN']}/messages",
        auth=("api", app.config['MAILGUN_API_KEY']),
        data={"from": app.config['MAILGUN_FROM_EMAIL'],
              "to": to,
              "subject": subject,
              "text": body})

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Parece que você mudou seu nome!')
        
        session['name'] = form.name.data
        
        # Enviar e-mail quando um novo nome é cadastrado
        send_email(
            to=["ana.caroline2@ifsp.edu.br"],
            subject="Novo usuário cadastrado",
            body=f"Um novo usuário chamado {form.name.data} foi cadastrado."
        )
        
        return redirect(url_for('index'))
    
    return render_template('index.html', form=form, name=session.get('name'))
