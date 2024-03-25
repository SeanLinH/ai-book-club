import streamlit as st
import time
from sidebar_navigators import navigators_generator
import sql
import re

#
## Session state
#


#
## Meta
#

st.set_page_config(
    page_title="智能讀書會-會員註冊"
)



def is_email_valid(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False

#
## Main
#

st.markdown("# 會員註冊")

with st.form(key="register_form"):
    account = st.text_input("帳號(名稱)",placeholder="John123" ,help="請輸入您的用戶名稱")

    email = st.text_input("Email")
    
    password = st.text_input(
        "密碼", 
        placeholder="此為測試應用，請勿與其他平台密碼共用",
        type="password", 
        help="密碼應為: 長 8 到 20 個英文字母大小寫或數字混和的字符串"
    )
    password_rep = st.text_input("確認密碼", type="password")

    submit_btn = st.form_submit_button("加入智能讀書會會員", use_container_width=True)
    if submit_btn:
        if password != password_rep:
            submit_btn = False
            st.warning("請確認用戶密碼是否輸入一致")
        elif not is_email_valid(email):
            submit_btn = False
            st.warning("請輸入有效的電子郵件地址")
        else:
            # TODO: 這邊需要將用戶的輸入數據提交到數據庫中
            regist_done, regist_msg = sql.insert_user(account, password, email, account)
            if regist_done:
                st.success("註冊成功!")
                time.sleep(2)
                st.switch_page("./pages/Login.py") 
            else:
                if regist_msg == "UNIQUE constraint failed: user.email":
                    st.error("email 已經被註冊過了")
                elif regist_msg == "UNIQUE constraint failed: user.user_id":
                    st.error("用戶名已經被註冊過了")
                else:
                    st.error(f"註冊失敗，請稍後再試, {regist_msg}")
                

                
            
            
            

        # sql.insert_user()


#
## Sidebar
#

with st.sidebar:
    st.write("# 會員註冊")
    st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator()


