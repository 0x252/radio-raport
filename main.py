'''
    Create Read Update Delete radio reports app
'''
DEBUG_ENABLED = True

from flask import Flask, render_template, request, jsonify
import time, redis, json, os

# init dotenv
from dotenv import load_dotenv 
load_dotenv()
# initRedis
QSO_KEY = "qso_list"
redisClient = redis.Redis(
  host=os.getenv("REDIS_HOST"),
  port=os.getenv("REDIS_PORT"),
  password=os.getenv("REDIS_PASSWORD"),
  decode_responses=True
  )

# TODO: To an another a file
def debug(*args): # va_list
    if DEBUG_ENABLED:
        print(args)
# Structures
class QSOField:
    def __init__(self, callsignA, callsignB, rsta, rstb):
     self.callsignA = callsignA
     self.callsignB = callsignB
     self.rsta = rsta
     self.rstb = rstb
     self.timestamp = time.time()
    def to_dict(self):
        return {
            "callsignA": self.callsignA,
            "callsignB": self.callsignB,
            "rsta": self.rsta,
            "rstb": self.rstb,
            "timestamp": self.timestamp
        }
    def to_json(self):
        return json.dumps(self.to_dict())
#
# No REST
# GLOBAL VARS
QSO = []

app = Flask(__name__, static_url_path='',static_folder='static', template_folder='templates')

'''
Отдает базовую страницу
'''
@app.route('/')
def index():
    return render_template('index.html')

'''
Удаляет запись о QSO по его id
Пример: /api/QSOdel/1
Варианты ответа: {"error": `${error}`} если ошибка
{"ok": True} если запись удалена
'''
@app.route('/api/QSOdel/<int:qso_id>', methods=["DELETE"])
def delete(qso_id):
   qso_list = redisClient.lrange(QSO_KEY, 0, -1)

   if qso_id < 0 or qso_id >= len(qso_list):
       return jsonify({"error": "bad qso id"}), 404
   redisClient.lrem(QSO_KEY, 0, qso_list[qso_id])
   return jsonify({"ok": True, "message": "did drop"}), 201
'''
Обновление записи
Принимает данные в JSON callsignA - свой позывной,callsignB - чужой позывной,rsta - RST ведущего,rstb - RST второго кореспондента
'''
@app.route("/api/QSOPut/<int:qso_id>", methods=["PUT"])
def put(qso_id):
    qso_list = redisClient.lrange(QSO_KEY, 0, -1)

    if qso_id < 0 or qso_id >= len(qso_list):
        return jsonify({"error": "QSO not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    qso_data = json.loads(qso_list[qso_id])
    qso_data['callsignA'] = data.get('callsignA', qso_data['callsignA'])
    qso_data['callsignB'] = data.get('callsignB', qso_data['callsignB'])
    qso_data['rsta'] = data.get('RSTA', qso_data['rsta'])
    qso_data['rstb'] = data.get('RSTB', qso_data['rstb'])
    redisClient.lset(QSO_KEY, qso_id, json.dumps(qso_data))
    #QSO[qso_id].timestamp = time.time() 
    return jsonify({"ok": True, "message": "QSO updated"}), 200

'''
Получение записей. Аргументы offset и limit
'''
@app.route('/api/QSO', methods=['GET'])
def getQSO():
    qso_list = redisClient.lrange(QSO_KEY, 0, -1)
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)
    if limit > int(os.getenv("QSO_LIMIT")):
        limit = int(os.getenv("QSO_LIMIT"))
    QSOs = [json.loads(qso) for qso in qso_list[offset:offset+limit]]
    return jsonify({
        "offset": offset,
        "limit": limit,
        "result": QSOs
    }), 201

'''
Добавляет запись
Принимает данные в JSON callsignA - свой позывной,callsignB - чужой позывной,rsta - RST ведущего,rstb - RST второго кореспондента
'''
@app.route('/api/addQSO', methods=['POST'])
def add_qso():
    data = request.get_json()
    if not data:
        return jsonify({"error":"no data"}), 400
    callsignA = data.get('callsignA')
    callsignB = data.get('callsignB')
    rsta  = data.get('RSTA')
    rstb = data.get('RSTB')
    debug(f"[ADD]: {callsignA} {rsta} - {callsignB} ({rstb})")
    if not(all([callsignA, callsignB, rsta, rstb])):
        return jsonify({"error":"not enough data"})
    debug("[ADD]: add QSO")
    newField = QSOField(callsignA, callsignB, rsta, rstb)
    redisClient.rpush(QSO_KEY, newField.to_json())
    return jsonify({
        "id": len(QSO)-1,
        "ok": True
    }), 201

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()