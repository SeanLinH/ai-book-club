import streamlit as st
import time
import sql


def authenticated_nav_user(expanded):
    """
    已經登入後的 `使用者` 導航欄位顯示
    """

    group_list = st.session_state['group_list']
    
    topic = st.selectbox(f"選擇群組", group_list)
    group_id = group_list.index(topic)
    if topic != st.session_state['topic']:
        st.session_state['topic'] = topic
        st.session_state['group_id'] = st.session_state['group_id_list'][group_id]
        st.rerun()
    if topic == "":
        if st.button(":red[新建群組]"):
            st.switch_page("./pages/ManagerCreateBookClub.py")
    users = sql.fetch_group_users(st.session_state['group_id'])
    st.info(f'群組編號: :red[{st.session_state["group_id"]}]')
    st.write(f"目前有 :red[{len(users)}]位成員")
    st.page_link("./pages/UserMain.py", label="💎會員說明")
    st.page_link("./pages/UserQuestionLobby.py", label="🙋提問大廳")
    st.page_link("./pages/ChatRoom.py", label="💬討論區")
    st.page_link("./pages/group_note.py", label="📝群組筆記")

    # with st.expander("Book Club User", expanded=expanded):
    #     st.page_link("./pages/UserQuestions.py", label="我的提問")
    #     st.page_link("./pages/UserQuestionLobby.py", label="等你回答")
    #     st.page_link("./pages/UserJoinBookClub.py", label="加入讀書會")

def authenticated_nav_info():
    """
    已經登入後顯示用戶的屬性設定
    """

    st.session_state['show_user_form'] = True
    if st.session_state.get('show_user_form', False):
        with st.sidebar.form(key='user_info_form'):
            st.write("個人化回應表單")
            username = st.text_input("你的名字", value=st.session_state['user_info'].get('user_name'),placeholder='王大強')
            domain = st.text_input("你的專業領域是什麼？", value=st.session_state['user_info'].get('domain') ,placeholder='智慧製造')
            role = st.selectbox(f"你在這個讀書會擔任什麼角色?\n\n你目前是 :red[{st.session_state['user_info'].get('role')}]", ['UI/UX設計師','前端工程師', '後端工程師', 'Data Scientist', 'AI工程師'])
            goal = st.text_area("你的學習目標?",value=st.session_state['user_info'].get('goal'), placeholder='我希望可以成為領域專家...')
            submit_button = st.form_submit_button('提交')
            
            if submit_button:
                if username == '':
                    username=st.session_state['user_id']
                if domain == '':
                    domain = '知識水平在大學的一般大眾'
                if role == '':
                    role = 'AI工程師'
                if goal == '':
                    goal = '增進自己的知識水平'


                st.session_state["user_info"] = {
                "user_name": username,
                "domain": domain,
                "role": role,
                "goal": goal
                }
                sql.update_user_info(user_id=st.session_state['user_id'], name=username, domain=domain, role=role, goal=goal, tag="")
                st.success('資料已提交')
                time.sleep(2)
                st.rerun()


def authenticated_nav_manager(expanded):
    """
    已經登入後的 `讀書會管理員` 導航欄位顯示
    """
    # with st.expander("資料上傳", expanded=expanded):
    #     st.page_link("./pages/ManagerMain.py", label="更新讀書會教材")
    st.page_link("./pages/ManagerCreateBookClub.py", label=":orange[☁️上傳教材/創建群組]")

def login_btn():
    """登入頁面跳轉按鈕"""
    btn_to_login = st.button(
        ":red[登入]", 
        use_container_width=True, 
        help="還沒登入嗎? 登入才可以開啟更多功能喔~")
    
    if btn_to_login:
        st.switch_page("./pages/Login.py")

def register_btn():
    """登入頁面跳轉按鈕"""
    btn_to_login = st.button(
        "註冊", 
        use_container_width=True, 
        help="還沒註冊嗎？")
    
    if btn_to_login:
        st.switch_page("./pages/Register.py")
    
def logout_btn():
    """登出按鈕"""
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
        authenticated_nav_info()
    else:
        col1, col2 = st.columns([1, 1])
        with col1:
            register_btn()
        with col2:
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
