
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
        return redirect(url_for('main.meus_pedidos'))
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
            if user.is_admin:
                return redirect(url_for('main.pedidos'))
            return redirect(url_for('main.meus_pedidos'))
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
        status='realizado',
        data_criacao=datetime.now()
    )
    db.session.add(pedido)
    db.session.commit()
    return jsonify({'success': True})

import json

@main.route('/pedidos')
@login_required
def pedidos():
    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        return redirect(url_for('main.meus_pedidos'))

    pedidos_db = Pedido.query.order_by(Pedido.data_criacao.desc()).all()
    pedidos = []
    for pedido in pedidos_db:
        try:
            produtos = json.loads(pedido.produtos)
        except Exception:
            produtos = []

        cliente = User.query.get(pedido.usuario_id)
        pedidos.append({
            'id': pedido.id,
            'nome_usuario': pedido.nome_usuario,
            'email_usuario': cliente.email if cliente else 'N/A',
            'cep': cliente.cep if cliente else 'N/A',
            'complemento': cliente.complemento if cliente else 'N/A',
            'produtos': produtos,
            'status': pedido.status,
            'data_criacao': pedido.data_criacao
        })
    return render_template('requests.html', pedidos=pedidos)

@main.route('/meus-pedidos')
@login_required
def meus_pedidos():
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
            'status': pedido.status,
            'data_criacao': pedido.data_criacao
        })

    current_order = pedidos[0] if pedidos else None
    previous_orders = pedidos[1:] if len(pedidos) > 1 else []
    status_steps = [
        {'key': 'realizado', 'title': 'Pedido realizado', 'description': 'Recebemos seu pedido com sucesso.'},
        {'key': 'preparando', 'title': 'Estamos preparando', 'description': 'Seu pedido está sendo preparado.'},
        {'key': 'saiu_entrega', 'title': 'Saiu para entrega', 'description': 'O entregador está a caminho do seu pedido.'},
        {'key': 'entregue', 'title': 'Entregue', 'description': 'Pedido entregue com sucesso.'},
    ]
    active_step_index = 0
    if current_order:
        for index, step in enumerate(status_steps):
            if step['key'] == current_order['status']:
                active_step_index = index
                break

    return render_template('myRequests.html', current_order=current_order, previous_orders=previous_orders, status_steps=status_steps, active_step_index=active_step_index)

@main.route('/atualizar-status/<int:pedido_id>', methods=['POST'])
@login_required
def atualizar_status(pedido_id):
    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        return jsonify({'success': False, 'message': 'Acesso negado.'}), 403

    pedido = Pedido.query.get_or_404(pedido_id)
    data = request.get_json() or {}
    novo_status = data.get('status')
    status_validos = ['realizado', 'preparando', 'saiu_entrega', 'entregue']
    if novo_status not in status_validos:
        return jsonify({'success': False, 'message': 'Status inválido.'}), 400

    pedido.status = novo_status
    db.session.commit()
    return jsonify({'success': True, 'status': novo_status})

@main.route('/excluir-pedido/<int:pedido_id>', methods=['POST'])
@login_required
def excluir_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'success': False, 'message': 'Usuário não autenticado.'}), 401
    if not user.is_admin and pedido.usuario_id != session['user_id']:
        return jsonify({'success': False, 'message': 'Acesso negado.'}), 403
    db.session.delete(pedido)
    db.session.commit()
    return jsonify({'success': True})