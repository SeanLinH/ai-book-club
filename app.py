import streamlit as st
from api import ChatGPT
import sql
import uuid



st.session_state['show_user_form'] = True
st.session_state['username'] = ""

# 如果show_user_form狀態為True，則在側邊欄顯示表單
if st.session_state.get('show_user_form', False):
    with st.sidebar.form(key='user_info_form'):
        st.write("用戶資料表單")
        title = st.text_input("讀書會主題", placeholder='大型語言模型讀書會')
        username = st.text_input("你的名字", placeholder='王大強')
        domain = st.text_input("你的專業領域是什麼？", placeholder='智慧製造工程師')
        role = st.selectbox("你在這個讀書會擔任什麼角色?", ['學習者', '領域專家/導師', '群組幹部/組長'])
        goal = st.text_area("你的學習目標?", placeholder='我希望可以成為領域專家...')
        col1, col2 = st.columns([1,1])
        submit_button = col1.form_submit_button('提交')
        
        
        if submit_button:
            if username == '':
                username='王大強'
            if domain == '':
                domain = '智慧製造工程師'
            if role == '':
                role = '學習者'
            if goal == '':
                goal = '我希望可以成為領域專家'

            if st.session_state['username'] != username:
                
                
                st.session_state['user_id'] = f'{uuid.uuid4()}'
                sql_id, last_goal = sql.check_username(username)
        
                if sql_id is not None:
                    st.session_state['user_id'] = sql_id
                    st.warning('已經有你的資料，需要更新嗎？')
                    st.write(f'您上次的目標：{last_goal}')
                    st.session_state['username'] = username
                    st.session_state['domain'] = domain
                    st.session_state['role'] = role
                    st.session_state['goal'] = goal
                    st.session_state['tag'] = ChatGPT.sum_user(goal)
                    
                    
                else:
                    st.success('資料已提交')
                    st.session_state['username'] = username
                    st.session_state['domain'] = domain
                    st.session_state['role'] = role
                    st.session_state['goal'] = goal
                    st.session_state['tag'] = ChatGPT.sum_user(goal)
                    sql.insert_user(st.session_state['user_id'], st.session_state['username'], st.session_state['domain'], st.session_state['role'], st.session_state['goal'], st.session_state['tag'])
        
        if st.sidebar.button('更新'):
            sql.update(st.session_state['user_id'], st.session_state['username'], st.session_state['domain'], st.session_state['role'], st.session_state['goal'], st.session_state['tag'])
            st.success('已更新')

        feedback = st.sidebar.text_area("使用上有什麼需要改善的？")
        if st.sidebar.button('改善建議'):
            with open('feedback.txt', 'a') as ff:
                ff.write(f"{feedback}\n")
                ff.close()
            st.sidebar.success('謝謝您')
        
     



# 應用標題
if title =="":
    title="大型語言模型讀書會"
st.title(title)

# 問題輸入
user_question = st.text_input("請輸入你的問題")


# 問題提交按鈕
if st.button('提交問題'):
    st.session_state.input_text = ""
    # 暫時以列表形式保存問題（實際應用中應該保存到數據庫）
    if 'questions' not in st.session_state:
        st.session_state['questions'] = []
    
    sql.insert_qst(user_question, st.session_state['user_id'],'待解決')
    if user_question not in st.session_state['questions']:
        st.session_state['questions'].append(user_question)
    else:
        st.warning("這個問題已經提交過了")

st.markdown(f"""

---

""")

question_num = 0
# 顯示問題列表
if 'questions' in st.session_state:
    for question in st.session_state['questions']:
        col1, col2, col3 = st.columns([1,2,1]) # 調整列的寬度比例
        question_num += 1
        col1.text(str(question_num))
        col2.write(question)
        # st.text(question)

        
        if col3.button('回答', key=question):
            # 使用OpenAI API獲取答案
            stream = ChatGPT.ans_question(title, question, st.session_state['user_id'])
            container = st.empty()
            text = ""
            n = 0
            for chunk in stream:
                n += 1
                if chunk.choices[0].delta.content is not None:
                    if (n % 40) == 0:
                        text += "\n"
                    text += chunk.choices[0].delta.content
                    container.text(text)
            text = text.replace("\n", "")
            sql.ai_response(st.session_state['user_id'], question, text)
            


