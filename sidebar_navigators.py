import streamlit as st
import time

def authenticated_nav_user(expanded):
    """
    已經登入後的 `使用者` 導航欄位顯示
    """
    with st.expander("Book Club User", expanded=expanded):
        st.page_link("./pages/UserMain.py", label="會員主頁")
        st.page_link("./pages/UserQuestions.py", label="我的提問")
        st.page_link("./pages/UserQuestionLobby.py", label="等你回答")
        st.page_link("./pages/UserJoinBookClub.py", label="加入讀書會")

def authenticated_nav_manager(expanded):
    """
    已經登入後的 `讀書會管理員` 導航欄位顯示
    """
    with st.expander("Book Club Manager", expanded=expanded):
        st.page_link("./pages/ManagerMain.py", label="讀書會管理員主頁")
        st.page_link("./pages/ManagerCreateBookClub.py", label="新建讀書會")

def login_btn():
    """登入頁面跳轉按鈕"""
    btn_to_login = st.button(
        ":red[登入]", 
        use_container_width=True, 
        help="還沒登入嗎? 登入才可以開啟更多功能喔~")
    
    if btn_to_login:
        st.switch_page("./pages/Login.py")
    
def logout_btn():
    """登出按鈕"""
    with st.expander("登出選項", expanded=False):
        logout_btn = st.button(
            ":green[登出]", 
            use_container_width=True)
        
        if logout_btn:
            st.session_state["user"] = False
            st.switch_page("./AIBookClub.py")


def navigators_generator(
    expanded_nav_user: bool = True,
    expanded_nav_manager: bool = True
):
    """生成導航欄 (與用戶狀態關聯的組件)

    Global Args:
        `st.session_state["user"]` (bool): 使用者登入狀態

    Args:
        `expanded_nav_user` (bool): 是否對 user 導航欄預先摺疊
        `expanded_nav_manager` (bool): 是否對 manager 導航欄預先摺疊
    
    Returns:
        顯示對應介面
    """

    if st.session_state["user"]:
        authenticated_nav_user(expanded_nav_user)
        authenticated_nav_manager(expanded_nav_manager)
    else:
        st.page_link("./pages/Register.py", label="會員註冊")
        login_btn()
    
def navigators_logout_generator():
    if st.session_state["user"]:
        logout_btn()

def navigators_openaikey_generator():
    """生成導航欄的 openai key 輸入用組件
    
    Change Global Args:
        `st.session_state["ai_usage"]` (bool): 使用者能否使用 AI 功能的狀態
        `st.session_state["ai_key"]` (str): 使用者調用 AI 功能時所使用的 OpenAI API key
        `st.session_state["ai_model"]` (str): 使用者調用 AI 功能時所使用的 OpenAI 模型型號
    """
    with st.expander("OpenAI key Setting", expanded=True):
        key = st.text_input("你的 OpenAI key", placeholder="請輸入你的 OpenAI key ，提供後續和 AI 功能的協作")
        model = st.selectbox("你想調用哪個模型?", ["GPT3.5", "GPT4"])
        key_submit_btn = st.button("確定", use_container_width=True)

        if key_submit_btn:
            st.session_state["ai_usage"] = True
            st.session_state["ai_key"] = key
            st.session_state["ai_model"] = model
            with st.empty():
                st.success("設置成功! 請稍等...")
                time.sleep(3)
            st.rerun()
    