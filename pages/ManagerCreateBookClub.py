import streamlit as st

from sidebar_navigators import \
    navigators_generator, \
    navigators_logout_generator

#
## Session state
#


#
## Meta
#

st.set_page_config(
    page_title="智能讀書會-新建讀書會"
)

#
## Main
#



#
## Sidebar
#

with st.sidebar:
    st.write("# 新建讀書會")
    st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator(expanded_nav_user=False)
    navigators_logout_generator()