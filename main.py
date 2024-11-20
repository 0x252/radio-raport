'''
    Create Read Update Delete radio reports app
'''
DEBUG_ENABLED = True

# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, jsonify
import json, time

# TODO: To an another a file
def debug(*args): # va_list
    if DEBUG_ENABLED:
        print(args)
# GLOBAL VARS
QSO = []
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
#
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
   if qso_id < 0 or qso_id >= len(QSO):
       return jsonify({"error": "bad qso id"})
   QSO.pop(qso_id)
   return jsonify({"ok": True, "message": "did drop"})
'''
Обновление записи
Принимает данные в JSON callsignA - свой позывной,callsignB - чужой позывной,rsta - RST ведущего,rstb - RST второго кореспондента
'''
@app.route("/api/QSOPut/<int:qso_id>", methods=["PUT"])
def put(qso_id):
    if qso_id < 0 or qso_id >= len(QSO):
        return jsonify({"error": "QSO not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    QSO[qso_id].callsignA = data.get('callsignA', QSO[qso_id].callsignA)
    QSO[qso_id].callsignB = data.get('callsignB', QSO[qso_id].callsignB)
    QSO[qso_id].rsta = data.get('RSTA', QSO[qso_id].rsta)
    QSO[qso_id].rstb = data.get('RSTB', QSO[qso_id].rstb)
    #QSO[qso_id].timestamp = time.time() 
    return jsonify({"ok": True, "message": "QSO updated"}), 200

'''
Получение записей. Аргументы offset и limit
'''
@app.route('/api/QSO', methods=['GET'])
def getQSO():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)
    QSOs = [qso.to_dict() for qso in QSO[offset:offset+limit]]
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
    QSO.append(newField)
    return jsonify({
        "id": len(QSO)-1,
        "ok": True
    }), 201

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()