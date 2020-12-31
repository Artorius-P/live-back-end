import time
from db import *
from mail import send_mail
from flask import Flask, request, jsonify, make_response, g, render_template
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_socketio import SocketIO, join_room, leave_room, ConnectionRefusedError, send, emit
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = '1145141919819'
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*")


auth = HTTPTokenAuth(scheme='Token')

# 实例化一个签名序列化对象 serializer，有效期 24 小时
serializer = Serializer(app.config['SECRET_KEY'], expires_in=86400)
valid_code = {}


@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = serializer.loads(token)
    except:
        return False
    if 'id' in data:
        g.user = data['id']
        return True
    return False


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

# 基于jquery的白板，已弃用。
# @app.route('/whiteboard')
# def whiteboard():
#     return render_template('white.html')


@app.route('/api/regist', methods=['POST'])
def regist_student():
    try:
        content = request.json
        name = content['name']
        password = content['password']
        address = content['mail']
        uid = add_user(name, password, 0, address)
        return jsonify({'status': 1, 'uid': uid})
    except:
        return jsonify({'status': 0, 'uid': 0})


@app.route('/api/sendmail', methods=['POST'])
def send_code():
    global valid_code
    content = request.json
    uid = content['id']
    _, _, _, address = get_user_info(uid)
    code = randint(0, 999999)
    code = str(code).zfill(6)
    valid_code[uid] = (code, time.time())
    send_mail(address, code)
    return jsonify({'status': 1})


@app.route('/api/reset', methods=['POST'])
def reset_password():
    global valid_code
    try:
        content = request.json
        uid = content['id']
        code = content['code']
        new_password = content['password']
        if valid_code[uid][0] != code:
            return jsonify({'status': 0, 'info': 'invalid code'})
        else:
            if valid_code[uid][1] + 300 < time.time():
                valid_code.pop(uid)
                return jsonify({'status': 0, 'info': 'code timed out'})
            else:
                valid_code.pop(uid)
                _, uname, uidentity, address = get_user_info(uid)
                change_user(uid, uname, new_password, uidentity, address)
                return jsonify({'status': 1, 'info': 'valid code'})
    except:
        return jsonify({'status': 0, 'info': 'invalid code'})


@app.route('/api/login', methods=['POST'])
def login():
    content = request.json
    uid = content['id']
    password = content['password']
    if check_password(uid, password):
        token = serializer.dumps({'id': uid})
        token = token.decode()
        _, username, identity, address = get_user_info(uid)
        return jsonify({'status': 1, 'token': token, 'id': uid, 'username': username, 'identity': identity, 'mail': address})
    else:
        return jsonify({'status': 0, 'token': None, 'id': uid, 'username': None, 'identity': None, 'mail': None})


@app.route('/api/getRoom', methods=['GET'])
@auth.login_required
def get_room():
    # get user's room id list [ (1, ), (2, ), (3, )]
    # the id is wrapped in a tuple
    lines = get_user_room(g.user)
    res = []
    # rooms.id, users.id, username, name, profile
    for line in lines:
        rid = line[0]
        room_info_raw = get_room_info(rid)
        room_info = {
            'id': room_info_raw[0],
            'tid': room_info_raw[1],
            'teacher': room_info_raw[2],
            'name': room_info_raw[3],
            'profile': room_info_raw[4]
        }
        res.append(room_info)

    return jsonify(res)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(str(username) + ' joined ' + str(room))
    emit('stc', {'username': 'system', 'message': username +
                 '加入了房间。'}, room=room, json=True)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('stc', {'username': 'system',
                 'message': username+'离开了房间'}, room=room, json=True)


@socketio.on('cts')
def on_message(data):
    print(data)
    username = data['username']
    room = data['room']
    message = data['message']
    if message[0] == '@':
        at = message.split()[0][1:]
        print(at)
        emit('at', {'username': username, 'at': at}, room=room, json=True)
        print(username, 'at', at)
    print(username, 'send', message)
    emit('stc', {'username': username, 'message': message},
         room=room, json=True)

# whiteboard server


@socketio.on('wserver')
def on_whiteboard(data):
    print('got whiteboard data')
    room = data['room']
    history = data['history']
    emit('wclient', {'history': history, }, room=room, json=True)


@socketio.on('wjoin')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(username, 'join', room)


@socketio.on('connection')
def connect():
    # try:
    # content = request.json
    # token = content['token']
    # data = serializer.loads(token)
    # if 'id' not in data:
    #     raise ConnectionRefusedError('unauthorized!')
    print('Client connected')
    # except:
    #     raise ConnectionRefusedError('unauthorized!')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
    app.run()
