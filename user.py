import streamlit as st

# 假設的用戶數據庫
# 在實際應用中，應該使用安全的方式來存儲和管理用戶信息
users_db = {
    "user1": {"password": "password1", "interest": None, "profession": None, "role": None},
    "user2": {"password": "password2", "interest": None, "profession": None, "role": None},
}

def login(user, password):
    """簡單的登入驗證"""
    return user in users_db and users_db[user]['password'] == password

def user_form(user):
    """顯示用戶資料表單"""
    with st.form("user_info"):
        st.write(f"歡迎, {user}! 請填寫以下資訊:")
        interest = st.text_input("你的興趣是什麼？", key="interest")
        profession = st.text_input("你的職業是什麼？", key="profession")
        role = st.selectbox("你在學習中扮演的角色是什麼？", ["學生", "教師", "研究者", "業餘愛好者"], key="role")
        
        # 當用戶提交表單時，更新用戶資料
        submitted = st.form_submit_button("提交")
        if submitted:
            users_db[user].update({"interest": interest, "profession": profession, "role": role})
            st.success("資料已更新")

# 用戶登入介面
with st.sidebar:
    st.title("用戶登入")
    user = st.text_input("用戶名稱", key="user")
    password = st.text_input("密碼", type="password", key="password")
    if st.button("登入"):
        if login(user, password):
            st.session_state['user'] = user
            st.success(f"歡迎回來, {user}!")
        else:
            st.error("登入失敗，請檢查用戶名稱和密碼")

# 如果用戶已登入，顯示資料表單
if 'user' in st.session_state:
    user_form(st.session_state['user'])