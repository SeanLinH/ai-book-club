import streamlit as st
import time
from sidebar_navigators import navigators_generator


#
## Session state
#


#
## Meta
#

st.set_page_config(
    page_title="智能讀書會-會員註冊"
)

#
## Main
#

st.markdown("# 會員註冊")

with st.form(key="register_form"):
    account = st.text_input("帳號(名稱)")
    email = st.text_input("Email")
    password = st.text_input(
        "密碼", 
        type="password", 
        help="密碼應為: 長 8 到 20 個英文字母大小寫或數字混和的字符串"
    )
    password_rep = st.text_input("確認密碼", type="password")

    submit_btn = st.form_submit_button("加入智能讀書會會員", use_container_width=True)
    if submit_btn:
        if password != password_rep:
            submit_btn = False
            st.warning("請確認用戶密碼是否輸入一致")
        else:
            # TODO: 這邊需要將用戶的輸入數據提交到數據庫中

            st.success("註冊成功! 3 秒後為您導到登入介面!")
            time.sleep(3)
            st.switch_page("./pages/Login.py") 


#
## Sidebar
#

with st.sidebar:
    st.write("# 會員註冊")
    st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator()


