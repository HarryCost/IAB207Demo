from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
app = Flask(__name__)

def create_app():
    Bootstrap5(app)
    app.secret_key = "somerandomvalue"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)

    UPLOAD_FOLDER = '/static/image'
    app.config['UPLAOD FOLDER'] = UPLOAD_FOLDER

    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #add Blueprints
    from . import views, destinations, auth
    
    app.register_blueprint(views.mainbp)
    app.register_blueprint(destinations.destbp)
    app.register_blueprint(auth.authbp)

    @app.errorhandler(404) 
    def not_found(e): 
        return render_template("404.html", error=e)

    return app

