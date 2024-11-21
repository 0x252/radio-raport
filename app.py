# init dotenv
from dotenv import load_dotenv 
from flask import Flask, render_template, request, jsonify
from utils import isValidCallSign
import json, os, re
from models import QSOField

#TODO: redisClient to globalVar/to a class
def getQSOs(redisClient):
    qso_list = redisClient.lrange(QSOField.REDIS_KEY, 0, -1)
    return qso_list

#TODO: redisClient to globalVar/to a class
def addQSO(redisClient,callsignA, callsignB, rsta, rstb):
    newField = QSOField.QSOField(callsignA, callsignB, rsta, rstb)
    redisClient.rpush(QSOField.REDIS_KEY, newField.json)


def createApp(port=8080, static_url_path='',static_folder='static', template_folder='templates', redisClient=None):
    app = Flask(__name__, static_url_path=static_url_path,static_folder=static_folder, template_folder=template_folder)
    def isValidCallSigns(a,b): return all([isValidCallSign(a),isValidCallSign(b)])
    load_dotenv()
#TODO: app.routes to routes directory
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/QSOdel/<int:qso_id>', methods=["DELETE"])
    def delete(qso_id):
        qso_list = getQSOs(redisClient)
        if qso_id < 0 or qso_id >= len(qso_list):
            return jsonify({"error": "bad qso id"}), 404
        redisClient.lrem(QSOField.REDIS_KEY, 0, qso_list[qso_id])
        return jsonify({"ok": True, "message": "did drop"}), 201

    @app.route("/api/QSOPut/<int:qso_id>", methods=["PUT"])
    def put(qso_id):
        qso_list = getQSOs(redisClient)
        if qso_id < 0 or qso_id >= len(qso_list):
            return jsonify({"error": "QSO not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid data"}), 400
        qso_data = json.loads(qso_list[qso_id])
        callsignA = data.get('callsignA', qso_data['callsignA'])
        callsignB = data.get('callsignB', qso_data['callsignB'])
        #TODO: Refactoring logic
        if not isValidCallSigns(callsignA,callsignB):
            return jsonify({
                "error": "not valid callsign"
            }),403
        qso_data['callsignA'] = callsignA
        qso_data['callsignB'] = callsignB
        qso_data['rsta'] = data.get('RSTA', qso_data['rsta'])
        qso_data['rstb'] = data.get('RSTB', qso_data['rstb'])
        redisClient.lset(QSOField.REDIS_KEY, qso_id, json.dumps(qso_data))
        #QSO[qso_id].timestamp = time.time() 
        return jsonify({"ok": True, "message": "QSO updated"}), 200


    @app.route('/api/QSO', methods=['GET'])
    def getQSO():
        qso_list = getQSOs(redisClient)
        offset = request.args.get('offset', default=0, type=int)
        limit = request.args.get('limit', default=10, type=int)
        if limit > int(os.getenv("QSO_LIMIT")):
            limit = int(os.getenv("QSO_LIMIT"))

        QSOs = {id:json.loads(qso) for qso,id in zip(qso_list[:], range(0,offset+limit))}

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
        addQSO(redisClient,callsignA, callsignB, rsta, rstb)
        qso_list = getQSOs(redisClient)
        QSOs = [json.loads(qso) for qso in qso_list[:]]
        return jsonify({
            "id": len(QSOs)-1,
            "ok": True
        }), 201
    return app