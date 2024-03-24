import streamlit as st
import time
from sidebar_navigators import \
    navigators_generator, \
    navigators_logout_generator

## session state
permissible_keys = {
    "user", 
    "user_id",
    "user_info",
    "group_list",
    "user_email"
}

for key in st.session_state.keys():
    if key not in permissible_keys:
        st.session_state.pop(key)


## Meta
title = "LLM"
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



