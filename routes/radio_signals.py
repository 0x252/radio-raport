from flask import Blueprint, jsonify
from flask import Flask, render_template, request, jsonify
from DB import DB

rsignal = Blueprint('rsignal', __name__)

@rsignal.route('/addRSignal')
def addRadioSignal():
        return jsonify({"ok": "ok"})
