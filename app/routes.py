from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/sobre')
def sobre():
    return render_template('aboutUs.html')

@main.route('/monte-sua-pizza')
def monte_sua_pizza():
    return render_template('assemblePizza.html')

@main.route('/pizzas')
def pizzas():
    return render_template('pizzas.html')

@main.route('/bebidas')
def bebidas():
    return render_template('drinks.html')

@main.route('/doces')
def doces():
    return render_template('candys.html')

@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cep = request.form.get('cep')
        complemento = request.form.get('complemento')
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'danger')
            return redirect(url_for('main.cadastro'))
        novo_user = User(nome=nome, email=email, senha=senha, cep=cep, complemento=complemento)
        db.session.add(novo_user)
        db.session.commit()
        return redirect(url_for('main.logged_user'))
    return render_template('register.html')

@main.route('/usuario-logado')
def logged_user():
    users = User.query.all()
    return render_template('loggedUser.html', users=users)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = User.query.filter_by(email=email).first()
        if user and user.senha == senha:
            return redirect(url_for('main.logged_user'))
        else:
            flash('E-mail ou senha inválidos!', 'danger')
            return redirect(url_for('main.login'))
    return render_template('login.html')

@main.route('/pedidos')
def pedidos():
    return render_template('requests.html')