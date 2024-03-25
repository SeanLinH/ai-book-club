import sqlite3
import uuid
from utils import is_email_valid

# 連接資料庫


### 新增用戶資料 -> register
def insert_user(user_id, pwd,email, name):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO user (user_id, pwd, email, name, group_id, group_name) VALUES (?, ?, ?, ?, ?, ?);", (user_id, pwd, email, name, "", ""))
        conn.commit()
        print("Command executed successfully")
        conn.close()
        return True, ""
    except Exception as e:
        print("Update Failed")
        print(e)
        conn.close()
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

### 抓取用戶的群組id 
def fetch_user_group(user_id) -> list:
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()

    if is_email_valid(user_id):
        c.execute("SELECT group_name, group_id FROM user WHERE email = ?;", (user_id,))
    else:
        c.execute("SELECT group_name, group_id FROM user WHERE user_id = ?;", (user_id,))
    group = c.fetchall()
    group_name = group[0][0].split(",")
    group_id = group[0][1].split(",")
    conn.close()
    return group_name, group_id

def join_user_group(user_id, group_id):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    c.execute("SELECT group_id, group_name FROM user")
    group = c.fetchall()
    new_group_name = ''
    for groupId, groupName in group:
        print(groupId)
        lst = groupId.split(',')
        if group_id in lst:
            idx = lst.index(group_id)
            new_group_name = groupName.split(',')[idx]
            break
    if new_group_name == "":
        return '此群組不存在'
    
    group_list, group_id_lst = fetch_user_group(user_id)
    if group_id in group_id_lst:
        return '已加入此群組'
    else:
        
        if group_list[0] == "":
            group_list = new_group_name
            group_id_lst = group_id
        else:
            group_list.append(new_group_name)
            group_list = ",".join(group_list)
            group_id_lst.append(group_id)
            group_id_lst = ",".join(group_id_lst)
        try:
            if is_email_valid(user_id):
                c.execute("UPDATE user SET group_name = ?, group_id = ? WHERE email = ?;", (group_list, group_id_lst, user_id))
            else:
                c.execute("UPDATE user SET group_name = ?, group_id = ? WHERE user_id = ?;", (group_list, group_id_lst, user_id))
            conn.commit()
            print("Command executed successfully")
            conn.close()
            return '加入成功'
        except Exception as e:
            print("Update Failed")
            print(e)
            conn.close()
            return f'加入失敗:{e}'

def drop_user_group(user_id, group_name, group_id):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    # 抓取用戶user_id 的群組id
    group_list, group_id_lst = fetch_user_group(user_id)
    if group_list[0] == "":
        return '此用戶尚未加入任何群組'
    else:
        if group_id in group_id_lst:
            group_list.remove(group_name)
            group_list = ",".join(group_list)
            group_id_lst.remove(group_id)
            group_id_lst = ",".join(group_id_lst)
            try:
                if is_email_valid(user_id):
                    c.execute("UPDATE user SET group_name = ?, group_id = ? WHERE email = ?;", (group_list, group_id_lst, user_id))
                else:
                    c.execute("UPDATE user SET group_name = ?, group_id = ? WHERE user_id = ?;", (group_list, group_id_lst, user_id))
                conn.commit()
                print("Command executed successfully")
                conn.close()
                return '已退出群組!'

            except Exception as e:
                print("Update Failed")
                print(e)
                conn.close()
                return f'更新失敗:{e}'
        else:
            
            return '此群組不存在'
    
### 先抓用戶的群組id，再更新用戶的群組id
def update_user_group(user_id, group_name, group_id):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    # 抓取用戶user_id 的群組id
    group_list, group_id_lst = fetch_user_group(user_id)

    if group_list[0] == "":
        group_list = group_name
        group_id_lst = group_id


    else:
        if group_id in group_id_lst:
            group_list = ",".join(group_list)
            group_id_lst = ",".join(group_id)
            conn.close()
            return '此群組已創立'
        else:
            group_list.append(group_name)
            group_list = ",".join(group_list)
            group_id_lst.append(group_id)
            group_id_lst = ",".join(group_id_lst)
            

    try:
        if is_email_valid(user_id):
            c.execute("UPDATE user SET group_name = ?, group_id = ? WHERE email = ?;", (group_list, group_id_lst, user_id))
        else:
            c.execute("UPDATE user SET group_name = ?, group_id = ? WHERE user_id = ?;", (group_list, group_id_lst, user_id))
        conn.commit()
        print("Command executed successfully")
        conn.close()
        return '建立成功'

    except Exception as e:
        print("Update Failed")
        print(e)
        conn.close()
        return f'建立失敗:{e}'
    


### update user 的domain, role, goal,tag
def update_user_info(user_id, domain, role, goal, tag):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE user SET domain = ?, role = ?, goal = ?, tag = ? WHERE user_id = ?;", (domain, role, goal, tag, user_id))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()

### fetch user info
def fetch_user_info(user_id):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    c.execute("SELECT name, domain, role, goal, tag FROM user WHERE user_id = ?;", (user_id,))
    user_info = c.fetchall()
    conn.close()
    return user_info

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