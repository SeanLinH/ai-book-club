import sqlite3
import uuid

# 連接資料庫
conn = sqlite3.connect('src/db/database.db')
c = conn.cursor()

### 新增用戶資料
def insert_user(user_id, user_pwd, name, domain, role, goal, tag):
    try:
        c.execute("INSERT INTO user (user_id, user_pwd, name, domain, role, goal, tag) VALUES (?, ?, ?, ?, ?, ?, ?);", (user_id, user_pwd, name, domain, role, goal, tag))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)

### 新增問題到叢集裡
def insert_qst(qst_text, ask_user, state='待解決'):
    qst_id = str(uuid.uuid4())
    try:
        c.execute("INSERT INTO question_cluster (qst_id, qst_text, ask_user, state) VALUES (?, ?, ?, ?);", (qst_id, qst_text, ask_user, state))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)

### 新增專家回覆
def insert_expert_answer(qst_id, expert_user, expert_response):
    ans_id = str(uuid.uuid4())
    try:
        c.execute("INSERT INTO expert_answer (ans_id, qst_id, expert_user, expert_response) VALUES (?, ?, ?, ?);", (ans_id, qst_id, expert_user, expert_response))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)

### AI 回答問題
def insert_ai_answer(qst_id, user_id, ai_response):
    ans_id = str(uuid.uuid4())
    try:
        c.execute("INSERT INTO ai_answer (ans_id, qst_id, user_id, ai_response) VALUES (?, ?, ?, ?);", (ans_id, qst_id, user_id, ai_response))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)

### 更新用戶資料
def update_user(user_id, user_pwd, name, domain, role, goal, tag):
    try:
        c.execute("UPDATE user SET user_pwd = ?, name = ?, domain = ?, role = ?, goal = ?, tag = ? WHERE user_id = ?;", (user_pwd, name, domain, role, goal, tag, user_id))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)

### 查詢用戶名是否存在
def check_username(name):
    c.execute("SELECT user_id, goal FROM user WHERE name = ? ORDER BY timestamp DESC;", (name,))
    user = c.fetchone()
    if user:
        return user[0], user[1]
    else:
        return None, None

### 抓取用戶問題
def fetch_user_qst(user_id):
    c.execute("SELECT qst_id, qst_text FROM question_cluster WHERE ask_user = ?;", (user_id,))
    questions = c.fetchall()
    return questions

### 抓取群組問題
def fetch_group_qst(state=None):
    if state:
        c.execute("SELECT qst_id, qst_text FROM question_cluster WHERE state = ?;", (state,))
    else:
        c.execute("SELECT qst_id, qst_text FROM question_cluster;")
    questions = c.fetchall()
    return questions





# 關閉資料庫連線
conn.close()
