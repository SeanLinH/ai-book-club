import sqlite3
import uuid

# 連接資料庫


### 新增用戶資料 -> register
def insert_user(user_id, pwd,email, name):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO user (user_id, pwd, email, name) VALUES (?, ?, ?, ?);", (user_id, pwd, email, name))
        conn.commit()
        print("Command executed successfully")
        conn.close()
        return True, ""
    except Exception as e:
        print("Update Failed")
        print(e)
        return False, e

### 新增問題到叢集裡
def insert_qst(qst_text, ask_user, state='待解決'):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    qst_id = str(uuid.uuid4())
    try:
        c.execute("INSERT INTO question_cluster (qst_id, qst_text, ask_user, state) VALUES (?, ?, ?, ?);", (qst_id, qst_text, ask_user, state))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()

### 新增專家回覆
def insert_expert_answer(qst_id, expert_user, expert_response):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    ans_id = str(uuid.uuid4())
    try:
        c.execute("INSERT INTO expert_answer (ans_id, qst_id, expert_user, expert_response) VALUES (?, ?, ?, ?);", (ans_id, qst_id, expert_user, expert_response))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()

### AI 回答問題
def insert_ai_answer(qst_id, user_id, ai_response):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    ans_id = str(uuid.uuid4())
    try:
        c.execute("INSERT INTO ai_answer (ans_id, qst_id, user_id, ai_response) VALUES (?, ?, ?, ?);", (ans_id, qst_id, user_id, ai_response))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()

### 更新用戶資料
def update_user(user_id, user_pwd, name, domain, role, goal, tag):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE user SET user_pwd = ?, name = ?, domain = ?, role = ?, goal = ?, tag = ? WHERE user_id = ?;", (user_pwd, name, domain, role, goal, tag, user_id))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()

### 查詢用戶名是否存在
def check_username(user_id=None, email=None, pwd=None):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    if user_id:
        c.execute("SELECT user_id, pwd FROM user WHERE user_id = ? ORDER BY timestamp DESC;", (user_id,))
    elif email:
        c.execute("SELECT user_id, pwd FROM user WHERE email = ? ORDER BY timestamp DESC;", (email,))    
    user = c.fetchone()
    conn.close()
    if user:
        if user[1] == pwd:
            return True, "登入成功"
        return False, "請檢查帳號密碼是否正確"
    else:
        return False, "此帳號尚未註冊，請先註冊。"

### 抓取用戶問題
def fetch_user_qst(user_id):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    c.execute("SELECT qst_id, qst_text FROM question_cluster WHERE ask_user = ?;", (user_id,))
    questions = c.fetchall()
    conn.close()
    return questions

### 抓取群組問題
def fetch_group_qst(state=None):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    if state:
        c.execute("SELECT qst_id, qst_text FROM question_cluster WHERE state = ?;", (state,))
    else:
        c.execute("SELECT qst_id, qst_text FROM question_cluster;")
    questions = c.fetchall()
    conn.close()
    return questions