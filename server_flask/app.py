from pydub import AudioSegment
from flask import Flask, request, send_file, render_template, make_response, abort, jsonify
import sqlite3
import time
import requests
from cut import cut
import io
from CUT200 import CUT200
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def inner(user_agent, remote_addr, current_route):
    import sqlite3
    import datetime
    # 连接到数据库
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 添加数据
    insert_data_sql = '''
    INSERT INTO log_data (user_agent, remote_addr, current_route ,time)
    VALUES (?, ?, ?,?)
    '''

    cursor.execute(insert_data_sql, (user_agent, remote_addr, current_route, time))

    # 提交更改
    conn.commit()

    # 关闭连接
    conn.close()


def delete_record(remote_addr):
    # 连接到数据库
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # 删除数据
    delete_data_sql = '''
    DELETE FROM log_data
    WHERE remote_addr = ?
    '''

    cursor.execute(delete_data_sql, (remote_addr,))

    # 提交更改
    conn.commit()

    # 关闭连接
    conn.close()


@app.route('/data', methods=['GET'])
def show_inner():
    import sqlite3
    delete_record('183.253.127.72')
    delete_record('220.196.160.95')
    # 连接到数据库
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # 查询数据
    select_data_sql = '''
    SELECT * FROM log_data
    '''
    cursor.execute(select_data_sql)

    # 获取查询结果
    rows = cursor.fetchall()

    # for row in rows:
    #     print(row)

    # 关闭连接
    conn.close()

    return rows


@app.before_request
def block_ip():
    # blocked_ips = ['91.188.254.31', '45.56.108.128']  # 被禁止的 IP 列表

    # client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    remote_addr = request.remote_addr
    current_route = request.url

    if request.path == '/online':
        pass
    else:
        inner(user_agent, remote_addr, current_route)

    # if client_ip in blocked_ips:
    #     abort(403)  # 返回 403 Forbidden 错误页面


def get_speaker():
    with open('speaker.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    decoded_string = content.encode().decode('unicode_escape')
    result_list = eval(decoded_string)
    return result_list


def role2id(role):
    speaker = get_speaker()
    import re
    for e in range(len(speaker)):
        pattern = r"\（.*?\）"
        name = re.sub(pattern, "", speaker[e], re.S)
        if name != speaker[e]:
            speaker[e] = name
    for s in range(len(speaker)):
        if role == speaker[s]:
            return s


def id2role(id):
    import re
    speaker = get_models()
    for e in range(len(speaker)):
        pattern = r"\（.*?\）"
        speaker[e] = re.sub(pattern, "", speaker[e], re.S)
    return speaker[int(id)]


#


def get_location(ip):
    url = f'https://res.abeim.cn/api-ip_info?ip={ip}'
    r = requests.get(url)
    data = r.json()['data']
    ip_pos = data['ip_pos']
    ip_isp = data['ip_isp']
    end = f'{ip_pos}{ip_isp}{ip}'
    return end


@app.errorhandler(404)
def page_not_found(error=None):
    # 自定义的 404 错误处理函数
    return '404 Not Found', 404


def show_table():
    import sqlite3

    # 连接到数据库
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # 查询表中的所有数据
    cursor.execute("SELECT * FROM records")
    rows = cursor.fetchall()

    # 打印查询结果

    # 关闭数据库连接
    conn.close()
    return rows


def inner_text(client_ip, speak_text, id_speaker, url):
    import time
    local_time = time.localtime(time.time())

    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

    # 连接到数据库
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # 插入数据
    time = formatted_time
    location = client_ip
    text = speak_text
    url = url
    speaker = id2role(id_speaker)

    cursor.execute("INSERT INTO records (time, location, text, url, speaker) VALUES (?, ?, ?, ?, ?)",
                   (time, location, text, url, speaker))

    # 提交更改
    conn.commit()

    # 关闭数据库连接
    conn.close()


@app.route('/models', methods=['GET'])
def get_models_api():

    models = ['阿尔卡米', '凯瑟琳', '阿贝多', '云堇', '烟绯', '常九爷', '史瓦罗', '卡维', '雷电将军', '掇星攫辰天君']
    models_with_index = [f"{index}:{name}" for index, name in enumerate(models)]

    response = make_response(models_with_index)

    return response


def get_models():
    models = ['阿尔卡米', '凯瑟琳', '阿贝多', '云堇', '烟绯', '常九爷', '史瓦罗', '卡维', '雷电将军', '掇星攫辰天君',
              '枫原万叶', '希儿', '夏洛蒂', '符玄', '派蒙', '「白老先生」', '早柚', '阿守', '迈勒斯', '香菱', '元太',
              '刻晴', '陆景和', '珐露珊', '娜维娅', '「散兵」', '荒泷一斗', '玛格丽特', '纳比尔', '哲平', '戴因斯雷布',
              '萍姥姥', '欧菲妮', '式大将', '迪希雅', '回声海螺', '嘉良', '凯亚', '白术', '伦纳德', '林尼', '慧心',
              '埃舍尔', '莫娜', '瓦尔特', '行秋', '吴船长', '奥列格', '爱德琳', '班尼特', '深渊法师', '「女士」',
              '娜塔莎', '坎蒂丝', '纳西妲', '流浪者', '天目十五', '奥兹', '温迪', '希露瓦', '阿洛瓦', '琳妮特',
              '螺丝咕姆', '玛塞勒', '刃', '影', '阿扎尔', '埃德', '多莉', '停云', '康纳', '八重神子', '宛烟', '罗刹',
              '雷泽', '塞琉斯', '景元', '阿娜耶', '恕筠', '罗莎莉亚', '佩拉', '申鹤', '海芭夏', 'anzai', '瑶瑶', '桑博',
              '知易', '托马', '胡桃', '阿圆', '陆行岩本真蕈·元素生命', '石头', '伊利亚斯', '米卡', '白露', '菲米尼',
              '阿祇', '九条镰治', '萨齐因', '鹿野院平藏', '星', '海妮耶', '晴霓', '荧', '旁白', '久利须', '斯坦利',
              '妮露', '魈', '钟离', '佐西摩斯', '天叔', '伊迪娅', '玛乔丽', '柊千里', '霍夫曼', '阿晃', '安西',
              '塞塔蕾', '阿巴图伊', '迈蒙', '青雀', '丽莎', '阿拉夫', '浮游水蕈兽·元素生命', '鹿野奈奈', '艾莉丝',
              '杜拉夫', '穹', '「大肉丸」', '舒伯特', '五郎', '帕姆', '萨赫哈蒂', '丹吉尔', '琴', '艾尔海森', '丹恒',
              '艾伯特', '银狼', '嘉玛', '莺儿', '「公子」', '赛诺', '巴达维', '安柏', '深渊使徒', '克罗索', '悦',
              '笼钓瓶一心', '北斗', '昆钧', '杰帕德', '艾丝妲', '宵宫', '珊瑚', '沙扎曼', '那维莱特', '帕斯卡', '拉齐',
              '珊瑚宫心海', '绿芙蓉', '卡芙卡', '迪卢克', '卡波特', '塔杰·拉德卡尼', '空', '黑塔', '驭空', '羽生田千鹤',
              '费斯曼', '「博士」', '久岐忍', '莫塞伊思', '诺艾尔', '莱依拉', '留云借风真君', '恶龙', '镜流', '爱贝尔',
              '虎克', '神里绫人', '达达利亚', '长生', '蒂玛乌斯', '彦卿', '埃泽', '埃尔欣根', '上杉', '重云', '阿兰',
              '辛焱', '拉赫曼', '言笑', '甘雨', '克列门特', '龙二', '田铁嘴', '迪奥娜', '姬子', '老孟', '凝光',
              '迪娜泽黛', '女士', '埃洛伊', '柯莱', '艾文', '西拉杰', '砂糖', '阿佩普', '芭芭拉', '布洛妮娅', '毗伽尔',
              '百闻', '大毫', '「信使」', '查尔斯', '左然', '绮良良', '半夏', '七七', '松浦', '莎拉', '埃勒曼', '三月七',
              '神里绫华', '夜兰', '丹枢', '博来', '大慈树王', '公输师傅', '提纳里', '芙宁娜', '托克', '素裳', '博易',
              '可可利亚', '青镞', '夏彦', '优菈', '可莉', '九条裟罗', '纯水精灵？', '菲谢尔', '克拉拉', '莫弈',
              '德沃沙克']

    return models


def id2role2(id):
    models = get_models()
    return models[int(id)]


def get_url(text, id, length, noise, noisew):
    # url = f'http://100.92.125.90:23456/voice/vits?text={text}&id={id}&lang=zh&format=wav&length={length}&noise={noise}&noisew={noisew}'
    url = f'https://genshinvoice.top/api?speaker={id2role2(id)}_ZH&text={text}&format=wav&length={length}&noise={noise}&noisew={noisew}&sdp=0.2&language=ZH'
    return url




@app.route('/run', methods=['GET'])
def run():
    speak_text = request.args.get('text')
    client_ip = request.remote_addr

    if len(speak_text) > 250:
        return '合成过长，250'
    id_speaker = request.args.get('id_speaker', type=str)
    voice_length = request.args.get('length', type=float)
    voice_noise = request.args.get('noise', type=float)
    noisew = request.args.get('noisew', type=float)

    if noisew is None:
        noisew = 0.4
    if voice_noise is None:
        voice_noise = 0.25
    if voice_length is None:
        voice_length = 1
    speak_text = speak_text.replace('\n ', '').replace('\n', '')

    # user_agent = request.headers.get('User-Agent')
    # if client_ip == '182.127.9.193':
    #     return page_not_found()
    url = f'https://genshinvoice.top/api?speaker={id2role2(id)}_ZH&text={speak_text}&format=wav&length={length}&noise={noise}&noisew={noisew}&sdp=0.2&language=ZH'
    # url = get_url(speak_text, id_speaker, voice_length, voice_noise, noisew)
    r = requests.get(url)
    new_url = f'http://www.纯度.site/second_run?text={speak_text}&id_speaker={id_speaker}&length={voice_length}&noise={voice_noise}&noisew={noisew}'

    # inner_text(client_ip, speak_text, id_speaker, new_url)

    stream = io.BytesIO(r.content)
    # 其他代码...

    return send_file(stream, mimetype='audio/wav')


#


@app.route('/second_run', methods=['GET'])
def second_run():
    speak_text = request.args.get('text')

    id_speaker = request.args.get('id_speaker', type=str)
    voice_length = request.args.get('length', type=float)
    voice_noise = request.args.get('noise', type=float)
    noisew = request.args.get('noisew', type=float)

    if noisew is None:
        noisew = 0.4
    if voice_noise is None:
        voice_noise = 0.25
    if voice_length is None:
        voice_length = 1.8
    speak_text = speak_text.replace('\n ', '').replace('\n', '')

    url = get_url(speak_text, id_speaker, voice_length, voice_noise, noisew)
    r = requests.get(url)

    stream = io.BytesIO(r.content)

    return send_file(stream, mimetype='audio/wav')


def get_table(begin):
    # 连接到数据库
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # 查询表中的所有数据
    cursor.execute(f"SELECT * FROM records ORDER BY time DESC LIMIT 40 OFFSET {begin}")

    rows = cursor.fetchall()

    # 打印查询结果

    # 关闭数据库连接
    conn.close()
    return rows


def get_base_table(begin):
    # 连接到数据库
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # 查询表中的所有数据
    cursor.execute(f"SELECT * FROM log_data ORDER BY time DESC LIMIT 40 OFFSET {begin}")

    rows = cursor.fetchall()

    # 关闭数据库连接
    conn.close()
    return rows


@app.route('/getdata/<int:page>')
def get(page):
    start = (page - 1) * 40
    # end = page * 40
    rows = get_table(start)

    datas = []
    for r in rows:
        id, crutime, text, url, speaker = r[0], r[1], r[3], r[4], r[5]
        url = url.replace('http', 'https')

        data = [id, crutime, text, url, speaker]
        datas.append(data)

        # temp=
        # if "second_run" in temp[4]:
        # temp[4]=temp[4].replace("second_run", "run")

    return jsonify(datas=datas)
    # 使用 page 变量来处理请求


@app.route('/get_base_table/<int:page>')
def get_base_table_api(page):
    start = (page - 1) * 40
    # end = page * 40
    rows = get_base_table(start)
    delete_record('183.253.127.72')
    delete_record('220.196.160.95')
    delete_record('127.0.0.1')
    datas = []
    for r in rows:
        # id, user_agent, remote_addr, current_route, time = r[0], r[1], r[3], r[4], r[5]
        user_agent, remote_addr, current_route, time, tryw = r[0], r[1], r[2], r[3], r[4]
        data = [user_agent, remote_addr, current_route, time, tryw]
        datas.append(data)

    return jsonify(datas=datas)


@app.route('/if', methods=['GET'])
def if_online():
    return '之前的版本无法正常使用，请使用最新版本1.6及以上，如果你使用的是1.6版本请忽略此条信息'


# @app.route('/data/standard', methods=['GET'])
# def standard():
#     return render_template('data.html')


@app.route('/online', methods=['GET'])
def online():
    return '1'


@app.route('/')
def html():
    # return render_template('main.html')
    return render_template('try.html')


def convert_to_numbers(board):
    conversion_dict = {None: 0, 'black': 1, 'white': 2}
    converted_board = [[conversion_dict[cell] for cell in row] for row in board]
    game.board = converted_board
    return converted_board


def convert_to_symbols(converted_board):
    conversion_dict = {0: None, 1: 'black', 2: 'white'}
    board = [[conversion_dict[cell] for cell in row] for row in converted_board]
    return board


class Gobang:
    def __init__(self):
        self.board = [[0] * 15 for _ in range(15)]
        self.current_player = 1
        self.last_black_move = None


    def check_winner(self, board):

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(15):
            for col in range(15):
                player = board[row][col]
                if player == 0:
                    continue
                for direction in directions:
                    dx, dy = direction
                    count = 1
                    for i in range(1, 5):
                        new_row = row + dx * i
                        new_col = col + dy * i
                        if not (0 <= new_row < 15 and 0 <= new_col < 15):
                            break
                        if board[new_row][new_col] == player:
                            count += 1
                        else:
                            break
                    if count == 5:
                        return player
        return 0



    def make_ai_move(self):
        best_score = -float('inf')
        best_move = None
        for row in range(15):
            for col in range(15):
                if self.board[row][col] == 0:

                    self.board[row][col] = 2
                    score = self.evaluate_board_for_ai(self.board, row, col)

                    self.board[row][col] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        if best_move:
            self.board[best_move[0]][best_move[1]] = 2
        return best_move

    def evaluate_board_for_ai(self, board, row, col):
        # 启发式评估
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for direction in directions:
            dx, dy = direction
            for dist in range(-5, 6):
                new_row = row + dx * dist
                new_col = col + dy * dist
                if 0 <= new_row < 15 and 0 <= new_col < 15:

                    if board[new_row][new_col] == 2:
                        score += 1
                    elif board[new_row][new_col] == 1:
                        score -= 1
        return score


@app.route('/send_board', methods=['POST'])
def tryit_go():
    data = request.get_json()
    board = data['board']
    board = convert_to_numbers(board)
    print('Received POST request:', board)

    winner = game.check_winner(board)
    if winner == 0 and data['currentPlayer'] == 'black':
        ai_row, ai_col = game.make_ai_move()
        board[ai_row][ai_col] = 2
        game.last_black_move = (ai_row, ai_col)
        return jsonify(winner=winner, ai_move=(ai_row, ai_col))
    else:
        return jsonify(winner=winner)


# @app.route('/try')
# def tryit():
#     return render_template('try.html')
#

# @app.route('/double', methods=['GET'])
# def double():
#     speak_text = request.args.get('text')
#
#     id_speaker_0 = request.args.get('id_speaker_0', type=str)
#
#     id_speaker_1 = request.args.get('id_speaker_1', type=str)
#
#     length_0 = 1
#     length_1 = 1
#     noise_0 = 0.32
#     noise_1 = 0.32
#     noisew_0 = 0.232
#     noisew_1 = 0.232
#
#     content_list, indices = C1.cut_Chinese_double_quotation_marks(speak_text)
#     # print(content_list)
#     # print(indices)
#     audio_bytes = BytesIO()
#     audios = []
#     for j, i in enumerate(indices):
#         if i == 0:  # 遍历旁白
#             url = get_url(content_list[j], id_speaker_0, length_0, noise_0, noisew_0)
#             r = requests.get(url)
#             audio = AudioSegment.from_file(BytesIO(r.content), format="wav")
#             audios.append(audio)
#
#         if i == 1:  # 遍历对话
#             url = get_url(content_list[j], id_speaker_1, length_1, noise_1, noisew_1)
#             r = requests.get(url)
#             audio = AudioSegment.from_file(BytesIO(r.content), format="wav")
#             audios.append(audio)
#
#     combined_audio = audios[0]
#     for audio in audios[1:]:
#         combined_audio += audio
#     output_filename = "combined_audio_double.wav"
#     combined_audio.export(output_filename, format="wav")
#
#     return send_file(
#         output_filename,
#         mimetype="audio/wav",
#
#     )
# @app.route('/can_only_myself', methods=['GET'])
# def content():
#     rows = show_table()
#     urls = []
#     rows.reverse()
#     for row in rows:
#         urls.append(
#             f'|{row[1]}|{row[2]}|<span class="styled-text">{row[3]}</span>|<a href="{row[4]} "target="_blank">播放</a>|{row[5]}')
#
#     urls = [elem for elem in urls if elem]
#     page = int(request.args.get('page', 1))
#
#     # 计算总页数
#     total_pages = (len(urls) - 1) // 40 + 1
#
#     # 根据当前页码和每页显示的数量计算切片范围
#     start = (page - 1) * 40
#     end = page * 40
#
#     # 对列表进行切片，获取当前页的数据
#     current_data = urls[start:end]
#
#     return render_template('page.html', data=current_data, page=page, total_pages=total_pages, urls=urls)


# @app.route('/api2', methods=['GET'])
# def api():
#     speak_text = request.args.get('text')
#     # print(f'speak_text1{speak_text}')
#     client_ip = request.remote_addr
#     speak_text = c1.str2list(speak_text)
#     # speak_text = c1.str2list(speak_text)
#     id_speaker = request.args.get('id_speaker', type=str)
#     voice_length = request.args.get('length', type=float)
#     voice_noise = request.args.get('noise', type=float)
#     noisew = request.args.get('noisew', type=float)
#
#     if noisew is None:
#         noisew = 0.4
#     if voice_noise is None:
#         voice_noise = 0.25
#     if voice_length is None:
#         voice_length = 1.8
#     speak_text = [s.replace('\n ', '').replace('\n', '') for s in speak_text]
#     # print(f'speak_text2{speak_text}')
#     # user_agent = request.headers.get('User-Agent')
#     audio_bytes = BytesIO()
#
#     audios = []
#     for s in speak_text:
#         url = get_url(s, id_speaker, voice_length, voice_noise, noisew)
#         r = requests.get(url)
#         audio = AudioSegment.from_file(BytesIO(r.content), format="wav")
#         audios.append(audio)
#
#     combined_audio = audios[0]
#     for audio in audios[1:]:
#         combined_audio += audio
#
#     output_filename = "combined_audio.wav"
#     combined_audio.export(output_filename, format="wav")
#     # new_url = f'http://www.纯度.site/api?text={speak_text}&id_speaker={id_speaker}&length={voice_length}&noise={voice_noise}&noisew={noisew}'
#
#     # inner_text(get_location(disguise_ip(client_ip)), speak_text, id_speaker, new_url)
#     return send_file(
#         output_filename,
#         mimetype="audio/wav",
#
#     )

if __name__ == '__main__':
    C1 = cut()
    c1 = CUT200()
    # c3 = CUT200()
    game = Gobang()
    # print(get_speaker())
    app.run(host='0.0.0.0', port=5000)
