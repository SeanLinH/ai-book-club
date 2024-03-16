import streamlit as st
from sidebar_navigators import \
    navigators_generator, \
    navigators_openaikey_generator, \
    navigators_logout_generator

# TODO (Database API):
_test_bookclub_name = [
    "LLM 讀書會", "AI 醫療讀書會", "紅樓夢讀書會", "余光中精選讀書會"
]

#
## Session state
#

if "bookclub_name" not in st.session_state:
    st.session_state["bookclub_name"] = _test_bookclub_name


#
## Meta
#

st.set_page_config(
    page_title="智能讀書會-我的提問"
)

#
## Main
#

st.markdown("# 我的提問")

tabs = st.tabs(st.session_state["bookclub_name"])
for bookclub_order, tab in enumerate(tabs):
    with tab:
        bookclub_name = st.session_state["bookclub_name"][bookclub_order]
        
        st.markdown(f"## {bookclub_name} 空間")
        st.markdown("### 我要提問...")
        
        text = st.text_input("輸入問題:", key=f"{bookclub_name}-ask")
        if st.button("提交問題", key=f"{bookclub_name}-submit"):
            # 堆到我提問的最下方
            st.rerun()

        # 給定所有問題列表
        # (question_id, dialog)


#
## Sidebar
#

with st.sidebar:
    st.write("# 我的提問")
    st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator()
    navigators_openaikey_generator()
    navigators_logout_generator()


#
## TESTING COMPONENTS
#

on_toggle_btn = st.toggle(":red[See Session state]")
if on_toggle_btn:
    st.write(f"Now session state is: :red[{st.session_state}]")
