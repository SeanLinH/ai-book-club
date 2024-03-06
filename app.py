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
        if 'upload_btn' not in st.session_state:
            submit_button = col1.form_submit_button('提交')
            if submit_button: # 用戶提交按鈕
                st.session_state['show_qst'] = True
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
                        
                        st.warning(f'嗨{username}! 已經有你的資料，需要更新嗎？')
                        st.write(f'您上次的目標：{last_goal}')
                        
                        st.session_state['upload_btn'] = True
                        
                    else:
                        st.session_state['upload_btn'] = False
                        st.success('資料已提交')
                        st.session_state['username'] = username
                        st.session_state['domain'] = domain
                        st.session_state['role'] = role
                        st.session_state['goal'] = goal
                        st.session_state['tag'] = ChatGPT.sum_user(goal)
                        sql.insert_user(st.session_state['user_id'], st.session_state['username'], st.session_state['domain'], st.session_state['role'], st.session_state['goal'], st.session_state['tag'])
        
        if 'upload_btn' in st.session_state:
            if st.session_state['upload_btn'] == True:
                if username == '':
                    username='王大強'
                if domain == '':
                    domain = '智慧製造工程師'
                if role == '':
                    role = '學習者'
                if goal == '':
                    goal = '我希望可以成為領域專家'
                sql_id, last_goal = sql.check_username(username)
                st.session_state['user_id'] = sql_id
                st.session_state['username'] = username
                st.session_state['domain'] = domain
                st.session_state['role'] = role
                st.session_state['goal'] = goal
                st.session_state['tag'] = ChatGPT.sum_user(goal)
                if col2.form_submit_button('更新'):
                    st.session_state['show_qst'] = True
                    if username == '':
                        username='王大強'
                    st.session_state['username'] = username
                    sql.update(st.session_state['user_id'], st.session_state['username'], st.session_state['domain'], st.session_state['role'], st.session_state['goal'], st.session_state['tag'])
                    st.success('已更新')
                    print(st.session_state)
        

        
        feedback = st.sidebar.text_area("使用上有什麼需要改善的？")
        if st.sidebar.button('提交改善建議'):
            with open('feedback.txt', 'a') as ff:
                ff.write(f"{feedback}\n")
                ff.close()
            st.sidebar.success('謝謝您')
        


if 'show_qst' not in st.session_state:
    st.markdown(f"""# AI智能讀書會平台介紹

## 簡介
AI智能讀書會是一個創新的學習共享平台，旨在促進知識的深度交流與協作學習。透過這個平台，用戶可以加入特定的學習群組，共同研究和討論學術論文或其他學習材料。本平台特色在於引入AI技術，以智能方式支持問題解答和內容理解，使學習過程更加高效、互動。

## 情境
- **學術研究**：學者和研究生可以上傳並討論最新的學術論文，深入探討研究方法和結果。
- **技術學習**：IT專業人士和學生可以分享技術文檔或教程，共同解決技術難題。
- **專業發展**：對特定領域感興趣的專業人士可以進行深入討論，擴展專業知識。

## 使用方法
1. **註冊並加入群組**：用戶首先需要註冊賬號，然後根據興趣或專業領域加入相應的學習群組。
2. **上傳學習材料**：用戶可以上傳學習材料，如學術論文或技術文檔，供群組成員共同學習。
3. **提問與回答**：針對材料，用戶可以提出問題，這些問題會被列入問題清單。用戶可以根據自己的知識和興趣回答問題，也可以使用AI輔助回答。

## 使用對象
- 學者、研究生和其他學術研究人員。
- IT專業人士、開發者和技術愛好者。
- 對特定領域有深入學習需求的專業人士。

## 應用技術
- **自然語言處理（NLP）**：用於理解和生成對學習材料的問題和回答。
- **機器學習與深度學習**：分析用戶行為，根據用戶的專業領域和興趣對問題和材料進行個性化排序。
- **知識圖譜**：構建專業領域內的知識關聯，幫助更準確地匹配問題和回答，並提供深入的學習資源。

AI智能讀書會平台致力於打造一個智能化、互動性強的學習社群，通過技術創新促進知識的交流與共享，為用戶提供一個全新的學習體驗。
""")

else:
    # 應用標題
    if title =="":
        title="大型語言模型讀書會"
    st.title(title)
    
    # 問題輸入
    user_question = st.text_input("請輸入你的問題")
    
    
    # 問題提交按鈕
    if st.button('提交問題'):
        st.session_state.text_input = ""
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
            


