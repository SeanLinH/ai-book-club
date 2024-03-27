import streamlit as st
import uuid
from typing import *
import openai
import os
import sql
import time
from api.ChatGPT import ans_question
from sidebar_navigators import \
    navigators_generator, \
    navigators_logout_generator

openai.api_key = os.environ.get("OPENAI_API_KEY")
## session state
permissible_keys = {
    "user", 
    "user_id",
    "user_info",
    "group_list",
    "group_id_list",
    "group_id",
    "user_email",
    "topic",
    "questions_list"
}

# for key in st.session_state.keys():
#     if key not in permissible_keys:
#         st.session_state.pop(key)

for key in permissible_keys:
    if key not in st.session_state.keys():
        st.session_state[key] = [""]
if st.session_state['user'] == [""]:
    st.session_state['user'] = False
    st.switch_page("./pages/Login.py")
    
st.set_page_config(
    page_title="AI智能讀書會-提問大廳",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

st.session_state['questions_list'] = []
for _,_,qst_text in sql.fetch_group_qst(st.session_state['group_id']):
    st.session_state['questions_list'].append(qst_text)

topic = st.session_state['topic']
if topic =="":
    st.switch_page("./pages/UserMain.py")



st.title(topic)

# 問題輸入
user_question = st.text_input("請輸入你的問題", value="")
summit = st.button("提交問題")

# 問題提交按鈕
if summit: #st.button('提交問題'):
    # 暫時以列表形式保存問題（實際應用中應該保存到數據庫）
    if user_question == '':
        st.warning("請輸入問題")
    elif user_question not in st.session_state['questions_list']:
        st.session_state['questions_list'].append(user_question)
        sql.insert_qst(group_id=st.session_state['group_id'], qst_text=user_question, ask_user=st.session_state['user_id'])
        st.success("已提交")
        stream = ans_question(topic, user_question, st.session_state['user_id'])
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
    else:
        st.warning("這個問題已經提交過了")

st.markdown(f"""

---

""")
question_num = 0

# 顯示問題列表
if 'questions_list' in st.session_state:
    
    for qst_id, ask_user, qst_text in sql.fetch_group_qst(st.session_state['group_id']):
        answers = sql.fetch_qst_ans(qst_id)
        col1, col2, col3 = st.columns([1,6,1]) # 調整列的寬度比例
        question_num += 1
        col1.text(str(question_num))
        if col1.button(":red[刪除問題]", key=f'{question_num}_delete'):
            sql.drop_qst(qst_id)
            st.rerun()
        col2.write(f'🙋‍♂️{ask_user} : {qst_text}')
        ans_btn = col3.button(f'智慧引導', key=f'{question_num}_ans')
        if ans_btn:
            # st.session_state[f'{question_num}_ans'] = True
            # 使用OpenAI API獲取答案
            stream = ans_question(topic, qst_text, st.session_state['user_id'])
            container = col2.empty()
            text = ""
            n = 0
            for chunk in stream:
                n += 1
                if chunk.choices[0].delta.content is not None:
                    if (n % 40) == 0:
                        text += "\n"
                    text += chunk.choices[0].delta.content
                    container.text(text)
        expert_ans = col2.text_area(" ",placeholder="專家回答", key=f'{question_num}_expert',label_visibility="collapsed")
        
        col_1, col_2, col_3 = st.columns([1,6,1]) # 調整列的寬度比例

        

        if col3.button('提交', key=f'{question_num}_submit'):
            if expert_ans == "":
                col_2.warning("請輸入文字")
                time.sleep(2)
                st.rerun()
            sql.insert_expert_answer(qst_id,st.session_state['group_id'], st.session_state['user_id'], expert_ans)
            col_2.write(f'🧐{st.session_state["user_id"]} : {expert_ans}')
            st.rerun()

        for ans_id, expertName, expertText in answers:
            col_2.write(f'🧐{expertName} : {expertText}')
            if col_3.button(":red[刪除回答]", key=f'{ans_id}_delete' ):
                sql.drop_expert_ans(ans_id)
                st.rerun()
            
        st.write('---')
    

        

#
## Sidebar
#

with st.sidebar:
    st.write("# 提問大廳")
    # st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator()
    navigators_logout_generator()

#
## TESTING COMPONENTS
#

# on_toggle_btn = st.toggle(":red[See Session state]")
# if on_toggle_btn:
#     st.write(f"Now session state is: :red[{st.session_state}]")
