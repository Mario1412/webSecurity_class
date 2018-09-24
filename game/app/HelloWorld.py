# Import Statement
from flask import Flask, render_template, jsonify, request, json
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.debug = True

socketio = SocketIO(app)

cavans = [[0] * 15 for i in range(15)]

count = 0


# =================== server-client battle =========================
# Creating our main route
@app.route('/')
def index():
    return render_template('server_client_game.html')


@app.route('/decide', methods=['POST'])
def decide():
    is_white = json.loads(request.form.get('data'))['is_white']
    global count

    data = {"flag": "ok", "is_white": is_white}
    count = count + 1
    if count > 2:
        data['flag'] = "oversize"
    if count == 1:
        data['is_white'] = True
    else:
        data['is_white'] = is_white
    return jsonify(data)


@socketio.on('draw', namespace='/canvas')
def draw(msg):
    global cavans
    global count

    flag = 'fail'
    is_win = False

    x = json.loads(msg.get('data'))['xV']
    y = json.loads(msg.get('data'))['yV']
    is_white = json.loads(msg.get('data'))['is_white']

    if cavans[x][y] == 0:
        flag = 'ok'
        cavans[x][y] = 1 if is_white else 2
        is_win = is_win_method(is_white, x, y,cavans)

    data = {'flag': flag,
            'chess': {'x': x, 'y': y, 'is_white': is_white, 'is_win': is_win},
            'count': count
            }

    if is_win:
        cavans = [[0] * 15 for i in range(15)]
        count = 0

    emit('draw', data, broadcast=True)


def is_win_method(is_white, x, y, ca):
    count_left_right = count_up_down = count_leftUp_rightDown = count_leftDown_rightUp = 0
    temp = 1 if is_white else 2

    # left-right
    for i in range(x, -1, -1):
        if ca[i][y] != temp:
            break
        count_left_right = count_left_right + 1

    for i in range(x + 1, 15):
        if ca[i][y] != temp:
            break
        count_left_right = count_left_right + 1

    # up-down
    for i in range(y, -1, -1):
        if ca[x][i] != temp:
            break
        count_up_down = count_up_down + 1

    for i in range(y + 1, 15):
        if ca[x][i] != temp:
            break
        count_up_down = count_up_down + 1

    # left-up-right-down
    for i, j in zip(range(x, -1, -1), range(y, -1, -1)):
        if ca[i][j] != temp:
            break
        count_leftUp_rightDown = count_leftUp_rightDown + 1

    for i, j in zip(range(x + 1, 15), range(y + 1, 15)):
        if ca[i][j] != temp:
            break
        count_leftUp_rightDown = count_leftUp_rightDown + 1

    # left-down-right-up
    for i, j in zip(range(x, -1, -1), range(y, 15)):
        if ca[i][j] != temp:
            break
        count_leftDown_rightUp = count_leftDown_rightUp + 1

    for i, j in zip(range(x + 1, 15), range(y - 1, -1, -1)):
        if ca[i][j] != temp:
            break
        count_leftDown_rightUp = count_leftDown_rightUp + 1

    if count_left_right >= 5 or count_up_down >= 5 or count_leftDown_rightUp >= 5 or count_leftUp_rightDown >= 5:
        return True
    return False


# =================== AI battle =====================================
ai_count = 0

ai_cavans = [[0] * 15 for i in range(15)]
ai_cavans_value = [[0] * 15 for i in range(15)]

chess_color = 0

dic = {"0": 0, "1": 8, "2": 10, "11": 50, "22": 1000, "111": 2500, "222": 3000, "1111": 5000, "2222": 10000,
       "21": 4, "12": 2, "211": 25, "122": 20, "11112": 3000, "112": 30, "1112": 3000, "221": 500, "2221": 4000,
       "22221": 10000}


@app.route('/ai')
def ai():
    return render_template('ai_game.html')


@app.route('/ai_decide', methods=['POST'])
def ai_decide():
    global ai_count
    ai_count = ai_count + 1

    random_num = random.randint(1, 2)

    # is_white = True if (random_num == 1) else False
    is_white = True

    data = {'flag': 'ok', 'is_white': is_white}

    if ai_count > 1:
        data['flag'] = 'oversize'

    return jsonify(data)


@socketio.on('ai_draw', namespace='/ai_canvas')
def ai_draw(msg):
    flag = 'fail'
    is_win = False
    who_win = 'human'
    ai_x = 0
    ai_y = 0

    global ai_count
    global ai_cavans

    x = json.loads(msg.get('data'))['xV']
    y = json.loads(msg.get('data'))['yV']
    is_white = json.loads(msg.get('data'))['is_white']
    ai_is_white = not is_white

    # human
    if ai_cavans[x][y] == 0:
        flag = 'ok'
        ai_cavans[x][y] = 1 if is_white else 2
        is_win = is_win_method(is_white, x, y, ai_cavans)

        if is_win:
            ai_cavans = [[0] * 15 for i in range(15)]
            ai_count = 0
        else:
            # ai
            ai_x_y = ai_operate()
            ai_x = ai_x_y['x']
            ai_y = ai_x_y['y']
            ai_cavans[ai_x][ai_y] = 2 if is_white else 1
            is_win = is_win_method(ai_is_white, ai_x, ai_y, ai_cavans)
            if is_win:
                ai_cavans = [[0] * 15 for i in range(15)]
                ai_count = 0
                who_win = 'ai'

    data = {'flag': flag,
            'chess': {'x': x, 'y': y, 'is_white': is_white},
            'chess_ai': {'ai_x': ai_x, 'ai_y': ai_y, 'ai_is_white': ai_is_white},
            'count': ai_count,
            'is_win': is_win,
            'who_win': who_win
            }

    emit('ai_draw', data)


def ai_operate():
    global ai_x, ai_y
    global code
    global chess_color

    # iterate the whole chess board
    for i in range(0, 15):
        for j in range(0, 15):
            if ai_cavans[i][j] == 0:
                code = ''
                chess_color = 0
                # right
                for x in range(i + 1, 15):
                    if ai_cavans[x][j] == 0:
                        break
                    else:
                        if x == i + 1:
                            chess_color = ai_cavans[x][j]

                        code += str(ai_cavans[x][j])
                        if chess_color != ai_cavans[x][j]:
                            break
                value = dic.get(code)
                if value:
                    ai_cavans_value[i][j] += value

                # clear
                code = ''
                chess_color = 0
                # left
                for x in range(i - 1, -1, -1):
                    if ai_cavans[x][j] == 0:
                        break
                    else:
                        if x == i - 1:
                            chess_color = ai_cavans[x][j]

                        code += str(ai_cavans[x][j])
                        if chess_color != ai_cavans[x][j]:
                            break
                value = dic.get(code)
                if value:
                    ai_cavans_value[i][j] += value

                # clear
                code = ''
                chess_color = 0
                # up
                for y in range(j - 1, -1, -1):
                    if ai_cavans[i][y] == 0:
                        break
                    else:
                        if y == j - 1:
                            chess_color = ai_cavans[i][y]

                        code += str(ai_cavans[i][y])
                        if chess_color != ai_cavans[i][y]:
                            break
                value = dic.get(code)
                if value:
                    ai_cavans_value[i][j] += value

                # clear
                code = ''
                chess_color = 0
                # down
                for y in range(j + 1, 15):
                    if ai_cavans[i][y] == 0:
                        break
                    else:
                        if y == j + 1:
                            chess_color = ai_cavans[i][y]

                        code += str(ai_cavans[i][y])
                        if chess_color != ai_cavans[i][y]:
                            break
                value = dic.get(code)
                if value:
                    ai_cavans_value[i][j] += value

                # clear
                code = ''
                chess_color = 0
                # left-down
                for x, y in zip(range(i - 1, -1, -1), range(j + 1, 15)):
                    if ai_cavans[x][y] == 0:
                        break
                    else:
                        if x == i - 1 and y == j + 1:
                            chess_color = ai_cavans[x][y]

                        code += str(ai_cavans[x][y])
                        if chess_color != ai_cavans[x][y]:
                            break
                value = dic.get(code)
                if value:
                    ai_cavans_value[i][j] += value

                # clear
                code = ''
                chess_color = 0
                # right-up
                for x, y in zip(range(i + 1, 15), range(j - 1, -1, -1)):
                    if ai_cavans[x][y] == 0:
                        break
                    else:
                        if x == i + 1 and y == j - 1:
                            chess_color = ai_cavans[x][y]

                        code += str(ai_cavans[x][y])
                        if chess_color != ai_cavans[x][y]:
                            break
                value = dic.get(code)
                if value:
                    ai_cavans_value[i][j] += value

                # clear
                code = ''
                chess_color = 0
                # left-up
                for x, y in zip(range(i - 1, -1, -1), range(j - 1, -1, -1)):
                    if ai_cavans[x][y] == 0:
                        break
                    else:
                        if x == i - 1 and y == j - 1:
                            chess_color = ai_cavans[x][y]

                        code += str(ai_cavans[x][y])
                        if chess_color != ai_cavans[x][y]:
                            break
                value = dic.get(code)
                if value:
                    ai_cavans_value[i][j] += value

                # clear
                code = ''
                chess_color = 0
                # right-down
                for x, y in zip(range(i + 1, 15), range(j + 1, 15)):
                    if ai_cavans[x][y] == 0:
                        break
                    else:
                        if x == i + 1 and y == j + 1:
                            chess_color = ai_cavans[x][y]

                        code += str(ai_cavans[x][y])
                        if chess_color != ai_cavans[x][y]:
                            break
                value = dic.get(code)
                if value:
                    ai_cavans_value[i][j] += value
                # clear
                code = ''
                chess_color = 0

    max = 0
    for x in range(0, 15):
        for y in range(0, 15):
            if ai_cavans_value[x][y] > max and ai_cavans[x][y] == 0:
                max = ai_cavans_value[x][y]
                ai_x = x
                ai_y = y

    return {'x': ai_x, 'y': ai_y}


# Starting up our Flask Server (helps us run the application)
if __name__ == '__main__':
    # socketio.run(app,host='10.0.0.48',port=5000)
    socketio.run(app)
