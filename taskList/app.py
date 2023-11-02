from flask import Flask, render_template
from taskList.ext.site.main import bp

def create_app():
    """ Initial app factory """

    app = Flask(__name__)
    app.register_blueprint(bp)
 
    return app

