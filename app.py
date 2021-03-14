from flask import Flask, render_template
from flask_socketio import SocketIO
from src.verda_implementation.engine import VerdaEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socket = SocketIO(app)
verda_engine = VerdaEngine()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('homepage.html')


@socket.on('send_usr_message')
def send_usr_message(data, methods=['GET', 'POST']):
    socket.emit('print_usr_message', data)


@socket.on('send_bot_message')
def send_bot_message(message_said, language, methods=['GET', 'POST']):
    print("entering message digestion")
    print(language)
    ret_val = verda_engine.only_text(message_said, language)
    socket.emit('print_bot_message', ret_val)


@socket.on('bot_speech_api')
def bot_speech_api(message_said, language, methods=['GET', 'POST']):
    print(language)
    ret_val = verda_engine.text_to_speech(message_said, language)
    socket.emit('print_bot_message', ret_val)


@socket.on('usr_speech')
def usr_speech(language, methods=['GET', 'POST']):
    print(language)
    ret_val = verda_engine.speech_to_text(language)
    socket.emit('print_usr_message', ret_val[0])
    socket.emit('print_bot_message', ret_val[1])


@socket.on('bot_speech_to_text_api')
def bot_speech_to_text_api(language, methods=['GET', 'POST']):
    print(language)
    ret_val = verda_engine.speech_and_text_to_speech(language)
    socket.emit('print_bot_message', ret_val)


if __name__ == '__main__':
    socket.run(app, debug=True)
