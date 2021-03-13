from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socket = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('homepage.html')


@socket.on('send_usr_message')
def send_usr_message(data, methods=['GET', 'POST']):
    socket.emit('print_usr_message', data)


@socket.on('send_bot_message')
def send_bot_message(data, methods=['GET', 'POST']):
    socket.emit('print_bot_message', data)  




if __name__ == '__main__':
    socket.run(app, debug=True)
