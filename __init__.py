from flask import Flask

def create_app(test_config= None):
    app = Flask(__name__) # flask app name and __name__ is module name
    app.secret_key = '1223aaa' # to keep it private from others than users

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app