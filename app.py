# init dotenv
from flask import Flask, render_template, request, jsonify
from utils import isValidCallSign
import json, os, re
from models.QSOField import QSOField
from redisClient import RedisSingleton
from DB import DB
import time

def getQSOs(offset=0, limit=os.getenv("QSO_LIMIT")):
    db = DB()
    qso_list = db.query(QSOField).offset(offset).limit(int(limit)).all()
    return qso_list


def createApp(port=8080, static_url_path='',static_folder='static', template_folder='templates'):
    redisClient = RedisSingleton()

    app = Flask(__name__, static_url_path=static_url_path,static_folder=static_folder, template_folder=template_folder)
    def isValidCallSigns(a,b): return all([isValidCallSign(a),isValidCallSign(b)])
    
#TODO: app.routes to routes directory
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/QSOdel/<int:qso_id>', methods=["DELETE"])
    def delete(qso_id):
        db = DB()
        qso = db.query(QSOField).get(qso_id)
        if not qso:
            return jsonify({"error": "Not found QSO"})
        db.session.delete(qso)
        db.session.commit()
        return jsonify({"ok": True, "message": "did drop"}), 200

    @app.route("/api/QSOPut/<int:qso_id>", methods=["PUT"])
    def put(qso_id):
        db = DB()
        qso = db.query(QSOField).get(qso_id)
        
        if not qso:
            return jsonify({"error": "QSO not found"}), 404 

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid data"}), 400  
        
 
        callsignA = data.get('callsignA', qso.callsignA)  
        callsignB = data.get('callsignB', qso.callsignB)

        
        if not isValidCallSigns(callsignA, callsignB):
            return jsonify({"error": "Invalid callsign"}), 403
        
        
        qso.callsignA = callsignA
        qso.callsignB = callsignB
        qso.rsta = data.get('RSTA', qso.rsta)
        qso.rstb = data.get('RSTB', qso.rstb)

        
        db.session.commit()
        
        return jsonify({"ok": True, "message": "QSO updated"}), 200


    @app.route('/api/QSO', methods=['GET'])
    def getQSO():
        offset = request.args.get('offset', default=0, type=int)
        limit = request.args.get('limit', default=10, type=int)
        if limit > int(os.getenv("QSO_LIMIT")):
            limit = int(os.getenv("QSO_LIMIT"))
        qso_list = getQSOs(offset, limit)
        print(qso_list)
        QSOs = {qso.id: json.loads(qso.json) for qso in qso_list}

        return jsonify({
            "offset": offset,
            "limit": limit,
            "result": QSOs
        }), 201


    @app.route('/api/addQSO', methods=['POST'])
    def add_qso():
        data = request.get_json()
        if not data:
            return jsonify({"error":"no data"}), 400
        callsignA = data.get('callsignA')
        callsignB = data.get('callsignB')
        #TODO: Refactoring logic
        if not isValidCallSigns(callsignA,callsignB):
            return jsonify({
                "error": "not valid callsign"
            }),403
        rsta  = data.get('RSTA')
        rstb = data.get('RSTB')
        print(f"[ADD]: {callsignA} {rsta} - {callsignB} ({rstb})")
        if not(all([callsignA, callsignB, rsta, rstb])):
            return jsonify({"error":"not enough data"})
        new_qso = QSOField(
            callsignA=data['callsignA'],
            callsignB=data['callsignB'],
            rsta=data['RSTA'],
            rstb=data['RSTB'],
            timestamp=time.time()
        )
        db = DB()
        db.session.add(new_qso)
        db.session.commit()
        count = db.query(QSOField).count()
        return jsonify({
            "id": count-1,
            "ok": True
        }), 201
    return app