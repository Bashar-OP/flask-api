from flask import Flask
import secrets
from extensions import db,migrate


def create_app():

    app = Flask(__name__)
    app.debug = True

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = secrets.token_hex()

    db.init_app(app)

    from routes import init,main_route,book_route,library_route,user_route

    migrate.init_app(app,db)

    app.register_blueprint(init.main)

    with app.app_context(): 
        db.create_all()

    return app
    

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)