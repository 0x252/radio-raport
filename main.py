'''
    Create Read Update Delete radio reports app
'''
import time, redis, os
from app import createApp as app 
from flask_socketio import SocketIO, emit, send

app = app(redisClient=redis.Redis(
                host=os.getenv("REDIS_HOST"),
                port=os.getenv("REDIS_PORT"),
                password=os.getenv("REDIS_PASSWORD"),
                decode_responses=True
                )
          )

socketio = SocketIO(app)
@socketio.on('message')
def handle_message(message):
    #print(f"Message received: {message}")
    try:
     #emit('message', {'username': message['username'], 'message':message['message']})
     send({'username': message['username'], 'message':message['message']},broadcast=True)
    except Exception as e:
       print(e)
       pass
    #TODO: fix logic


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
