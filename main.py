from flask import Flask
import secrets
from extensions import db,migrate


def create_app():
    from routes import init

    app = Flask(__name__)
    app.debug = True

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = secrets.token_hex()

    app.register_blueprint(init.main)

    db.init_app(app)

    migrate.init_app(app,db)

    with app.app_context(): 
        db.create_all()

    return app
    

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)