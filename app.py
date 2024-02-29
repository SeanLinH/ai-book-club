import streamlit as st
import openai
from dotenv import load_dotenv
import os 

load_dotenv()

# 設置OpenAI API密鑰
openai.api_key = os.environ.get("OPENAI_API_KEY")



st.session_state['show_user_form'] = True
# 如果show_user_form狀態為True，則在側邊欄顯示表單
if st.session_state.get('show_user_form', False):
    with st.sidebar.form(key='user_info_form'):
        st.write("用戶資料表單")
        title = st.text_input("讀書會主題", placeholder='大型語言模型讀書會')
        username = st.text_input("你的名字", placeholder='王大強')
        domain = st.text_input("你的專業領域是什麼？", placeholder='智慧製造工程師')
        role = st.multiselect("你在這個讀書會擔任什麼角色?", ['群組幹部/組長','領域專家/導師', '學習者'], max_selections=2)
        goal = st.text_area("你的學習目標?", placeholder='我希望可以成為領域專家...')
        submit_button = st.form_submit_button('提交')
        
        if submit_button:
            if username == '':
                username='王大強'
            if domain == '':
                domain = '知識水平在大學的一般大眾'
            if role == '':
                role = '學習者'
            if goal == '':
                goal = '增進自己的知識水平'

            st.session_state['username'] = username
            st.session_state['domain'] = domain
            st.session_state['profession'] = role
            st.session_state['goal'] = goal
            st.success('資料已提交')
            print(st.session_state)


# 應用標題
if title =="":
    title="大型語言模型讀書會"
st.title(title)

# 問題輸入
user_question = st.text_input("請輸入你的問題")



# 問題提交按鈕
if st.button('提交問題'):
    # 暫時以列表形式保存問題（實際應用中應該保存到數據庫）
    if 'questions' not in st.session_state:
        st.session_state['questions'] = []
    
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
            stream = openai.chat.completions.create(
                model="gpt-4-1106-preview", 
                messages=[
                    {
                    "role": "system",
                    "content": f"""You are a professional AI expert. If I ask you question related to math, AI, DS, DL, ML, you can answer them from a professional perspective. You can choose to search online to get more accurate information.  If you feel that the question I asked may not be so important, or there are other more important questions that I may not understand, you can try to guide me to further understand the relevant technical knowledge. 
                    [INST]Rule:
                    1. you always follow user's language type.
                    2. you always be kind.
                    3. If you don't know the question, you should identify the user's qeustion.
                    4. If you ensure that the user's question is not an knowledge question, you should guide the user to ask questions related to the {title}. and you only reply simple conclusion within 1 sentence. For example, "I think the most important thing is to understand the core issues."
                    5. You should not answer questions that are irrelevant to the {title}. Instead, you should ask rhetorical questions to guide users to think about the core issues.
                    6. Do not use Simplified Chinese. [/INST]"""
                    },
                    {
                        "role": "user",
                        "content": f"Please answer question '{question}'. Then, give me an example."
                    }  
                ],
                max_tokens=500,
                stream=True)
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


