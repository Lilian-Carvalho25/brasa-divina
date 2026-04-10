
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from .models import User, Pedido
from . import db
from datetime import datetime
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Faça login para acessar esta página.', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

main = Blueprint('main', __name__)

@main.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('main.login'))

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
            session['user_id'] = user.id
            session['user_nome'] = user.nome
            return redirect(url_for('main.pedidos'))
        else:
            flash('E-mail ou senha inválidos!', 'danger')
            return redirect(url_for('main.login'))
    return render_template('login.html')

@main.route('/salvar-pedido', methods=['POST'])
def salvar_pedido():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Usuário não autenticado.'}), 401
    data = request.get_json()
    produtos = data.get('produtos')
    # Buscar nome do usuário na sessão ou no banco
    user_nome = session.get('user_nome')
    if not user_nome:
        user = User.query.get(session['user_id'])
        user_nome = user.nome if user else 'Usuário'
    primeiro_nome = user_nome.split()[0] if user_nome else 'Usuário'
    if not produtos:
        return jsonify({'success': False, 'message': 'Dados incompletos.'}), 400
    pedido = Pedido(
        usuario_id=session['user_id'],
        nome_usuario=primeiro_nome,
        produtos=produtos,
        data_criacao=datetime.now()
    )
    db.session.add(pedido)
    db.session.commit()
    return jsonify({'success': True})

import json

@main.route('/pedidos')
@login_required
def pedidos():
    user_id = session['user_id']
    pedidos_db = Pedido.query.filter_by(usuario_id=user_id).order_by(Pedido.data_criacao.desc()).all()
    pedidos = []
    for pedido in pedidos_db:
        try:
            produtos = json.loads(pedido.produtos)
        except Exception:
            produtos = []
        pedidos.append({
            'id': pedido.id,
            'nome_usuario': pedido.nome_usuario,
            'produtos': produtos,
            'data_criacao': pedido.data_criacao
        })
    return render_template('requests.html', pedidos=pedidos)

@main.route('/excluir-pedido/<int:pedido_id>', methods=['POST'])
@login_required
def excluir_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.usuario_id != session['user_id']:
        return jsonify({'success': False, 'message': 'Acesso negado.'}), 403
    db.session.delete(pedido)
    db.session.commit()
    return jsonify({'success': True})