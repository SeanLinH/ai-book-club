import sqlite3
import uuid



def insert_user(user_id, name, domain, role, goal, tag):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    print(f"INSERT INTO users VALUES ({user_id}, {name}, {domain}, {role}, {goal}, {tag})")
    try:
        c.execute(f"INSERT INTO users (user_id, name, domain, role, goal, tag) VALUES (?, ?, ?, ?, ?, ?);",(user_id, name, domain, role, goal, tag))
        conn.commit()
        print("Command executed successfully")

    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()

def insert_qst(question, user_id, state='待解決'):
    qst_id = f'{uuid.uuid4()}'
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()

    try:
        c.execute(f"INSERT INTO question_cluster (qst_id, qst_text, ask_user, expert_user, ai_response, expert_response, state) VALUES (?, ?, ?, ?, ?, ?, ?);", (qst_id, question, user_id, None, None, None, '待解決'))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()


def ai_response(user_id, question, ans):
    qst_id = f'{uuid.uuid4()}'
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()

    try:
        c.execute(f"INSERT INTO question_cluster (qst_id, qst_text, ask_user, expert_user, ai_response, expert_response, state) VALUES (?, ?, ?, ?, ?, ?, ?);", (qst_id, question, None, user_id, ans, None, '已解決'))
        conn.commit()
        print("Command executed successfully")
    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()
    
    
    
def update(user_id, name, domain, role, goal, tag):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    
    try:
        c.execute(f"UPDATE users SET name = ?, domain = ?, role = ?, goal = ?, tag = ? WHERE user_id = ?",(name, domain, role, goal, tag, user_id))
        conn.commit()
        print("Command executed successfully")

    except Exception as e:
        print("Update Failed")
        print(e)
    conn.close()    
    
    

def check_username(name):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    c.execute("SELECT user_id, goal FROM users WHERE name = ? ORDER BY timestamp DESC;", (name,))
    user = c.fetchone()
    conn.commit()
    conn.close()
    if user:
        return user[0], user[1]
    else:
        return None, None
        
    
    
    

