
from flask_bootstrap import Bootstrap
# from flaskr.scraper import scrap_itviec, scrap_vietnamwork
from pymongo import InsertOne, DeleteOne, ReplaceOne
from .db import get_db
from utils.scraper import scrap_itviec, scrap_vietnamwork
import os
from flaskr.home import load_data
from flask_pymongo import PyMongo
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Flask
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # app.config["MONGO_URI"] = "mongodb://localhost:27017/data_intergration"
    app.config["MONGO_URI"] = "mongodb+srv://duongnb:18071999@cluster0.9r4fz.mongodb.net/data_intergration?retryWrites=true&w=majority"
    Bootstrap(app)
    mongo = PyMongo(app)
    app.db = mongo.db
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    from . import auth
    app.register_blueprint(auth.bp)
    # a simple page that says hello

    @app.route('/hello')
    def hello():
        db = get_db()
        jobs_count = db.jobs_info.count()
        return jsonify(jobs_count)

    @app.route('/itviec', methods=['GET'])
    def itviec():
        result = jsonify(result=scrap_itviec())
        return redirect(url_for('home'))

    @ app.route('/vietnamwork')
    def vietnamwork():
        result = jsonify(result=scrap_vietnamwork())
        return redirect(url_for('home'))

    @ app.route('/home')
    def home():
        res = load_data()
        print(res['data_count'])
        jobs_count = res['data_count']
        text_s = 'aaa'
        return render_template("jobs/home.html", jobs_count=jobs_count, demo_itviec=res['demo_data_itviec'], demo_vietnamwork=res['demo_data_vietnamwork'], last_update=res['last_update'])
    return app
