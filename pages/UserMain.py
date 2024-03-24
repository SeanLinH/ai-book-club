import streamlit as st
from sidebar_navigators import \
    navigators_generator, \
    navigators_logout_generator

#
## Session state
#

permissible_keys = {
    "user", 
    "user_id",
    "user_info"
}

for key in st.session_state.keys():
    if key not in permissible_keys:
        st.session_state.pop(key)

if "user_info" not in st.session_state:
    st.session_state["user_info"] = {
        "user_name": "Jack (Default)",
        "user_club_join": ["預設1讀書會", "預設2讀書會"]
    }

#
## Meta
#

st.set_page_config(
    page_title="智能讀書會-會員主頁"
)

#
## Main
#

# 頁面標題開頭
# st.markdown(f'# Hi! {st.session_state["user_info"]["user_name"]}')

# 我的學習歷程
st.markdown("## 我的學習歷程")

st.markdown("這邊的設計不知道要填什麼...這邊的設計不知道要填什麼...\
這邊的設計不知道要填什麼...這邊的設計不知道要填什麼...\
這邊的設計不知道要填什麼...這邊的設計不知道要填什麼...\
這邊的設計不知道要填什麼...這邊的設計不知道要填什麼...")

# 我參加的讀書會
st.markdown("## 我參加的讀書會")
club_group = st.session_state["user_info"]["user_club_join"]
club_tabs = st.tabs(club_group + ["參加其他讀書會"])
for club, tab in zip(club_group, club_tabs[:-1]):
    with tab:
        st.markdown(f"### {club}")
        st.markdown("這邊的設計不知道要填什麼...這邊的設計不知道要填什麼...\
這邊的設計不知道要填什麼...這邊的設計不知道要填什麼...\
這邊的設計不知道要填什麼...這邊的設計不知道要填什麼...\
這邊的設計不知道要填什麼...這邊的設計不知道要填什麼...")

with club_tabs[-1]:
    st.markdown("### 想參加? 想看看其他讀書會嗎?")

    btn_to_login = st.button(
        ":red[去看看]",
        use_container_width=True, 
        help="還沒加入讀書會的朋友，可在這裡參加一個喔~"
    )
    
    if btn_to_login:
        st.switch_page("./pages/UserJoinBookClub.py")

#
## Sidebar
#

with st.sidebar:
    st.write("# 你的主頁")
    st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator()
    navigators_logout_generator()


#
## TESTING COMPONENTS
#

on_toggle_btn = st.toggle(":red[See Session state]")
if on_toggle_btn:
    st.write(f"Now session state is: :red[{st.session_state}]")
