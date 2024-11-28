# init dotenv
from flask import Flask, render_template, request, jsonify
from utils import isValidCallSign
import json, os, re
from models.QSOField import QSOField
from redisClient import RedisSingleton
from DB import DB
import time

from routes.qso import qso
from routes.radio_signals import rsignal

def createApp(port=8080, static_url_path='',static_folder='static', template_folder='templates'):
    #redisClient = RedisSingleton()

    app = Flask(__name__, static_url_path=static_url_path,static_folder=static_folder, template_folder=template_folder)
    
    app.register_blueprint(rsignal)
    app.register_blueprint(qso)

#TODO: app.routes to routes directory
    @app.route('/')
    def index():
        return render_template('index.html')
    return app
