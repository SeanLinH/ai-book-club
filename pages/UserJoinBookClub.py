import streamlit as st
import uuid
from typing import *
from sidebar_navigators import \
    navigators_generator, \
    navigators_logout_generator

# TODO (Database Initialize API):
_test_bookclub_display = {
    "bookclub_name": None,
    "bookclub_key": None
}

# TODO (Database Initialize API):
_test_bookclub_btn_name_list = [
    "LLM 讀書會", "AI 醫療讀書會", "紅樓夢讀書會", "余光中精選讀書會"
]

# TODO (Database Update API): 加載智能讀書會資訊
def get_bookclub_info(bookclub_key: str) -> str:
    info = """## 智能讀書會資訊 (測試)  \n\
這個部分是用於測試的一段 Markdown 文字，具體需要從數據庫或檔案中\
讀取指定讀書會的宣傳資訊、基本資訊、入會條件等。以字符串的這種形式\
做載入"""
    return info

#
## Session state
#

permissible_keys = {
    "user", 
    "user_id", 
    "bookclub_display", 
    "bookclub_btn_name_list"
}

for key in st.session_state.keys():
    if key not in permissible_keys:
        st.session_state.pop(key)

if "bookclub_display" not in st.session_state:
    st.session_state["bookclub_display"] = _test_bookclub_display

if "bookclub_btn_name_list" not in st.session_state:
    # TODO: 加載所有已建立的讀書會數據，並做成標籤 (API)
    st.session_state["bookclub_btn_name_list"] = _test_bookclub_btn_name_list


#
## Meta
#

st.set_page_config(
    page_title="智能讀書會-加入讀書會"
)

#
## Main
#

st.markdown("# 我要參加...")

# TODO: 加載所有已建立的讀書會數據，並做成標籤

bookclub_info_col, bookclub_select_col = st.columns([4, 1])

with bookclub_select_col.container(height=750):
    for i, bookclub_btn_name in enumerate(
            st.session_state["bookclub_btn_name_list"]
        ):
        if st.button(bookclub_btn_name):
            st.session_state["bookclub_display"]["bookclub_name"] = \
                st.session_state["bookclub_btn_name_list"][i]
            st.session_state["bookclub_display"]["bookclub_key"] = \
                st.session_state["bookclub_btn_name_list"][i]
            st.rerun()  

    if st.button(":red[更多讀書會]"):
        # TODO: 加載更多的讀書會 (再增加 5 個) (API)
        val = str(uuid.uuid4())
        st.session_state["bookclub_btn_name_list"].append(val)
        st.rerun()

# 動態顯示加入填寫表單
with bookclub_info_col.container(height=750, border=True):

    if st.session_state["bookclub_display"]["bookclub_name"] is not None:
        title_name = st.session_state["bookclub_display"]["bookclub_name"]
    else:
        title_name = None

    if title_name is None:
        title = st.markdown(f"## 請點選一個讀書會按鈕")

    if title_name is not None:

        # bookclub title
        title = st.markdown(f"## {title_name}")

        # bookclub information
        with st.expander("讀書會資訊",  expanded=True):
            bookclub_info = get_bookclub_info(st.session_state["bookclub_display"]["bookclub_key"])
            st.markdown(bookclub_info)

        # bookclub submit form
        form_key = st.session_state["bookclub_display"]["bookclub_key"]
        
        with st.expander("用戶資料表單", expanded=False):
            with st.form(key=form_key):
                username = st.text_input("你的名字", placeholder='王大強')
                domain = st.text_input("你的專業領域是什麼？", placeholder='智慧製造工程師')
                role = st.selectbox("你在這個讀書會擔任什麼角色?", ['學習者', '領域專家/導師', '群組幹部/組長'])
                goal = st.text_area("你的學習目標?", placeholder='我希望可以成為領域專家...')
                st.form_submit_button(use_container_width=True)


#
## Sidebar
#

with st.sidebar:
    st.write("# 加入讀書會")
    st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator()
    navigators_logout_generator()


#
## TESTING COMPONENTS
#

on_toggle_btn = st.toggle(":red[See Session state]")
if on_toggle_btn:
    st.write(f"Now session state is: :red[{st.session_state}]")