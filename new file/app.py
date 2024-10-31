from flask import Flask, jsonify, request
from flask_cors import CORS
import MySQLdb

app = Flask(__name__)
CORS(app)

# MySQL 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',  # 替换为你的 MySQL 用户名
    'password': '123456',  # 替换为你的 MySQL 密码
    'database': 'web'  # 替换为你的数据库名
}


@app.route('/')
def home():
    return "欢迎来到日记应用！"


@app.route('/diary', methods=['POST'])
def add_diary_entry():
    entry = request.json
    username = entry['username']  # 获取用户名
    content = entry['content']

    # 连接数据库并插入数据
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO diary_entries (username, content) VALUES (%s, %s)", (username, content))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Entry added!'}), 201


@app.route('/diary', methods=['GET'])
def get_diary_entries():
    # 连接数据库并获取数据
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM diary_entries")
    entries = cursor.fetchall()

    # 将查询结果转换为 JSON 格式
    diary_entries = [{'id': entry[0], 'username': entry[1], 'content': entry[2], 'created_at': entry[3]} for entry in
                     entries]

    cursor.close()
    conn.close()

    return jsonify(diary_entries)


if __name__ == '__main__':
    app.run(debug=True)
