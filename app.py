from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socket = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('homepage.html')


@socket.on('send')
def send(data, methods=['GET', 'POST']):
    socket.emit('print_message', data)


if __name__ == '__main__':
    socket.run(app, debug=True, port=port)
