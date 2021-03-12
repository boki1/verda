from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socket = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def sessions():
    return render_template('chat.html')


def message_received(methods=['GET', 'POST']):
    print('message was received!!!')


@socket.on('send')
def send(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socket.emit('my response', json, callback=message_received)


if __name__ == '__main__':
    socket.run(app, debug=True)
