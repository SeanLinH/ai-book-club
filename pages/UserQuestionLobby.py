import streamlit as st
import uuid
from typing import *
import openai
import os
import sql
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
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)



# st.session_state 暫時的 Database API 模擬，需要被 API 方法替代
# _test_bookclub_name = [
#     "LLM 讀書會", "AI 醫療讀書會", "紅樓夢讀書會", "余光中精選讀書會"
# ]

# # 根據每個讀書會獲取其個別的 question_id 和具體 question 的敘述整合
# # 後續可以方便地由 question_id 找 question
# _test_questions = {
#     "asd1": "我家的老鼠生病了，應該給它吃老鼠藥嗎?", 
#     "asd2": "地球的望遠鏡那麼厲害，為什麼看不到地球?", 
#     "asd3": "地球上有 70% 的海洋和 30% 的陸地，那另外 30% 的海洋和 70% 的陸地在哪裡?", 
#     "asd4": "我的藍牙耳機壞了，應該去看牙科還是耳鼻喉科?",
#     "asd125": "Lorem ipsum consectetur Lorem ipsum consectetur adipisicing elit. Ut, sunt! adipisicing elit. Ut, sunt!Lorem ipsum consectetur adipisicing elit. Ut, sunt!Lorem ipsum consectetur adipisicing elit. Ut, sunt!Lorem ipsum consectetur adipisicing elit. Ut, sunt!",
#     "asd1546": "Lorem Ut, sunt!",
#     "asd3546": "Lorem ipsum dolor. Ut, sunt!",
#     "asd146": "Lorem ipsum consectetur adipisicing elit. Ut, sunt!",
#     "as23546": "Lorem ipsum dolor sit amet elit. Ut, sunt!",
#     "a546": "Lorem ipsum dolor sunt!",
# }

# _test_question_id_1_1 = ["asd1", "asd2", "asd3", "asd4"]
# _test_question_id_2_1 = ["asd125", "asd1546", "asd3546", "asd146", "as23546", "a546"]
# _test_question_id_3_1 = ["asd3", "asd2", "asd1", "asd4"]

# _test_question_id_1_2 = ["asd1", "asd2", "asd3", "asd4"]
# _test_question_id_2_2 = ["asd125", "asd1546", "asd3546", "asd146", "as23546", "a546"]
# _test_question_id_3_2 = ["asd3", "asd4", "asd2", "asd1"]

# _test_question_id_1_3 = ["asd1", "asd2", "asd3", "asd4"]
# _test_question_id_2_3 = ["asd125", "asd1546", "asd4", "asd3546", "asd146", "as23546", "a546"]
# _test_question_id_3_3 = ["asd3", "asd2", "asd1"]

# _test_question_id_1_4 = ["asd1", "asd2", "asd3", "asd4"]
# _test_question_id_2_4 = ["asd125", "asd1546", "asd3546", "asd146", "as23546", "a546"]
# _test_question_id_3_4 = ["asd3", "asd2", "asd1", "asd4"]

# _test_bookclub_info = {
#     "LLM 讀書會": [_test_question_id_1_1, _test_question_id_2_1, _test_question_id_3_1], 
#     "AI 醫療讀書會": [_test_question_id_1_2, _test_question_id_2_2, _test_question_id_3_2], 
#     "紅樓夢讀書會": [_test_question_id_1_3, _test_question_id_2_3, _test_question_id_3_3], 
#     "余光中精選讀書會": [_test_question_id_1_4, _test_question_id_2_4, _test_question_id_3_4]
# }


# def set_question_widget(
#     bookclub_name: str, 
#     attr: Literal["hot", "interest", "old"], 
#     question_id_list: List[str], 
#     expanded: bool = False, 
# ):
#     """專門用於設置 `hot (熱門)` 、 `interest (你可能感興趣)` 、 `old (久久未答)` \
#     的統一模板。會針對不同的 attr 生成對應的該區塊。

#     Args:
#         `bookclub_name` (str):
#             讀書會名稱
#         `attr` (Literal["hot", "interest", "old"]):
#             問題欄位屬性
#         `question_id_list` (List[str]):
#             全部為 question_id 的 list ，目前暫定傳入的是
#             `st.session_state["bookclub_info"][bookclub_name][i]` 的第 i 個 list
#         `expanded` (bool): (default = False 不攤開)
#             是否要預設讓這個介面部分攤開

#     Change Global:
#         可能更動到
#         `st.session_state["bookclub_info"][bookclub_name]` 的數據
#         `st.session_state["questions"]` 的數據
#     """

#     mapping = {
#         "hot": "熱門",
#         "interest": "你可能感興趣",
#         "old": "久久未答",
#     }
#     mapping_attr = mapping[attr]

#     with st.expander(f"顯示{mapping_attr}的問題", expanded=expanded):
#         for question_id in question_id_list:
#             question = st.session_state["questions"][question_id]
            
#             cols = st.columns([5, 1])
#             with cols[0]:
#                 st.markdown(f"#### Q{question_id}  \n {question}")
#             with cols[1]:
#                 check_btn_key = f"{bookclub_name}-{attr}-{question_id}-check"
#                 st.button("查看", key=check_btn_key, use_container_width=True)    

#         more_btn_key = f"{bookclub_name}-more-{attr}"
#         if st.button("更多問題", key=more_btn_key, use_container_width=True):
#             # 由數據庫載入更多問題到對應的 question_id_list 中，
#             # question_id_list 表示為
#             # st.session_state["_test_bookclub_info"][bookclub_name][i] 的第 i 個 list
#             new_id = str(uuid.uuid4())
#             question_id_list.append(new_id)
#             st.session_state["questions"][new_id] = "default new"
#             st.rerun()


#
## Session state
#

# TODO: 目前 API 暫時未定，確定後再確定保留哪些環境狀態
# permissible_keys = {"user", "user_id"}

# for key in st.session_state.keys():
#     if key not in permissible_keys:
#         st.session_state.pop(key)

# if "bookclub_name" not in st.session_state:
#     st.session_state["bookclub_name"] = _test_bookclub_name

# if "bookclub_info" not in st.session_state:
#     st.session_state["bookclub_info"] = _test_bookclub_info

# if "questions" not in st.session_state:
#     st.session_state["questions"] = _test_questions



# #
# ## Meta
# #

# st.set_page_config(
#     page_title="智能讀書會-等你回答"
# )

# #
# ## Main
# #

# st.markdown("# 等你來答")



# tabs = st.tabs(st.session_state["bookclub_name"])
# for bookclub_order, tab in enumerate(tabs):
#     # 可能需要做這樣: {"bookclub_name1": [questions_id_1, questions_id_2, questions_id_3]}
#     with tab:
#         bookclub_name = st.session_state["bookclub_name"][bookclub_order]
        
#         st.markdown(f"## {bookclub_name} 空間")

#         st.markdown("### 熱門")
#         set_question_widget(
#             bookclub_name, 
#             "hot", 
#             st.session_state["bookclub_info"][bookclub_name][0],
#         )

#         st.markdown("### 你可能感興趣")
#         set_question_widget(
#             bookclub_name, 
#             "interest", 
#             st.session_state["bookclub_info"][bookclub_name][1],
#             expanded=True
#         )
        
#         st.markdown("### 幫幫他們吧~~")
#         set_question_widget(
#             bookclub_name, 
#             "old", 
#             st.session_state["bookclub_info"][bookclub_name][2],
#         )


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
        for expertName, expertText in answers:
            col2.write(f'🧐{expertName} : {expertText}')

        if col3.button('提交', key=f'{question_num}_submit'):
            sql.insert_expert_answer(qst_id,st.session_state['group_id'], st.session_state['user_id'], expert_ans)
            col2.write(f'🧐{st.session_state["user_id"]} : {expert_ans}')
            
        st.write('---')
    

        

#
## Sidebar
#

with st.sidebar:
    st.write("# 等你回答")
    # st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator()
    navigators_logout_generator()

#
## TESTING COMPONENTS
#

# on_toggle_btn = st.toggle(":red[See Session state]")
# if on_toggle_btn:
#     st.write(f"Now session state is: :red[{st.session_state}]")
