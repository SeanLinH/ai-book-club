import time
import streamlit as st
from typing import *
from sidebar_navigators import navigators_generator
import sql
import re

# 確認電子郵件地址是否有效
def is_email_valid(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False
    
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
        if is_email_valid(account):
            login, msg = sql.check_username(email=account, pwd=password)
        else:
            login, msg = sql.check_username(user_id=account, pwd=password)

        if login:
            st.success(msg)
            time.sleep(2)
            st.session_state["user"] = True
            st.switch_page("./pages/UserMain.py")
        else:
            st.error(msg)
        

#
## Sidebar
#

with st.sidebar:
    st.write("# 會員登入")
    st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator()

