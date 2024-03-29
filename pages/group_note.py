import streamlit as st
import uuid
from typing import *
import os
import sql
import time
from api.ChatGPT import ans_question
from sidebar_navigators import \
    navigators_generator, \
    navigators_logout_generator


def folder_path(bookclub_id):
    target_folder = f'src/data/{bookclub_id}-materials'
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    return target_folder

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

if "edit" not in st.session_state:
    st.session_state['edit'] = False
    st.session_state['content'] = "" 

st.set_page_config(
    page_title="AI智能讀書會-群組筆記",
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



st.write(f'## {topic}')

col1, col2, col3 = st.columns([7, 1, 1])
if col2.button("編輯"):
    st.session_state['edit'] = True
    st.rerun()

if st.session_state['edit']:
    content = st.text_area("MarkDown 筆記編輯...", value=st.session_state['content'], height=700)
else:
    bookclub_id = st.session_state['group_id']
    path = folder_path(bookclub_id)
    content = open(f'{path}/note.md').read()
    st.markdown(content)

if col3.button("保存"):
    st.session_state['edit'] = False
    bookclub_id = st.session_state['group_id']
    path = folder_path(bookclub_id)
    with open(f'{path}/note.md', 'w') as f:
        f.write(content)
    st.rerun()





        

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
