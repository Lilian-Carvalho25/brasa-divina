import os
from sqlalchemy import inspect
from app import create_app, db
from app.models import User

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()

        inspector = inspect(db.engine)
        if not inspector.has_table('user'):
            raise RuntimeError('A tabela user não foi criada. Verifique a configuração do banco e os models.')
        if not inspector.has_table('pedido'):
            raise RuntimeError('A tabela pedido não foi criada. Verifique a configuração do banco e os models.')

        user_columns = [column['name'] for column in inspector.get_columns('user')]
        pedido_columns = [column['name'] for column in inspector.get_columns('pedido')]

        if 'is_admin' not in user_columns:
            print('Adicionando coluna is_admin na tabela user...')
            db.engine.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0")

        if 'status' not in pedido_columns:
            print('Adicionando coluna status na tabela pedido...')
            db.engine.execute("ALTER TABLE pedido ADD COLUMN status VARCHAR(30) NOT NULL DEFAULT 'realizado'")

        admins = [
            ('pizzaiolo1@brasa.com', 'pizzaiolo1', 'Pizzaiolo Um'),
            ('pizzaiolo2@brasa.com', 'pizzaiolo2', 'Pizzaiolo Dois'),
            ('pizzaiolo3@brasa.com', 'pizzaiolo3', 'Pizzaiolo Três'),
        ]

        for email, senha, nome in admins:
            existing = User.query.filter_by(email=email).first()
            if existing:
                existing.is_admin = True
                existing.nome = nome
                existing.senha = senha
            else:
                user = User(nome=nome, email=email, senha=senha, is_admin=True)
                db.session.add(user)

        db.session.commit()
        print('Seed de pizzaiolos administradores concluída.')
        print('Logins disponíveis:')
        for email, senha, nome in admins:
            print(f'  {nome}: {email} / {senha}')