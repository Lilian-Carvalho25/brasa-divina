from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/sobre')
def sobre():
    return render_template('sobre.html')

@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'danger')
            return redirect(url_for('main.cadastro'))
        novo_user = User(nome=nome, email=email, senha=senha)
        db.session.add(novo_user)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('main.home'))
    return render_template('cadastro.html')
