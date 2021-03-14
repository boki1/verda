from flask import Flask, render_template
from flask_socketio import SocketIO
from src.verda_implementation.engine import VerdaEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socket = SocketIO(app)
verda_enging = VerdaEngine()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('homepage.html')


@socket.on('send_usr_message')
def send_usr_message(data, methods=['GET', 'POST']):
    socket.emit('print_usr_message', data)


@socket.on('send_bot_message')
def send_bot_message(data, methods=['GET', 'POST']):
    socket.emit('print_bot_message', data)  


@socket.on('bot_speech_api')
def bot_speech_api(message_to_say, methods=['GET', 'POST']):
    ret = verda_enging.text_to_speech(message_to_say)
    pass


@socket.on('bot_speech_to_text_api')
def bot_speech_to_text_api(methods=['GET', 'POST']):
    ret = verda_enging.speech_and_text_to_speech()
    socket.emit('bot_digestion')


if __name__ == '__main__':
    socket.run(app, debug=True)
