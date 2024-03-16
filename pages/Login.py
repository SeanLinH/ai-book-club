import time
import streamlit as st
from typing import *
from sidebar_navigators import navigators_generator

# TODO (Database API): 這邊需要確認帳號密碼匹配的方法
def login_checking(account: str, password: str) -> bool:
    return True

#
## Session state
#


#
## Meta
#

st.set_page_config(
    page_title="智能讀書會-會員登入"
)

#
## Main
#

st.markdown("# 登入智能讀書會")

with st.container(border=True):
    account = st.text_input("帳號")
    password = st.text_input(
        "密碼",
        type="password"
    )

    login_check = st.button("登入", use_container_width=True)
    if login_check:
        if login_checking(account, password):
            st.success("登入成功， 3 秒後導到您的主頁")
            time.sleep(3)
            st.session_state["user"] = True
            st.switch_page("./pages/UserMain.py")
        else:
            st.error("帳號或密碼輸入不正確")
        

#
## Sidebar
#

with st.sidebar:
    st.write("# 會員登入")
    st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator()

