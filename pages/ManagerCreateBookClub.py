import streamlit as st
import time
from sidebar_navigators import \
    navigators_generator, \
    navigators_logout_generator

import sql
#
## Session state
#

permissible_keys = {
    "user", 
    "user_id",
    "user_info",
    "group_list"
}

for key in st.session_state.keys():
    if key not in permissible_keys:
        st.session_state.pop(key)


#
## Meta
#

st.set_page_config(
    page_title="智能讀書會-新建讀書會"
)

#
## Main
#
st.markdown("#### 加入讀書會參考教材")
st.markdown("""
    支持以 pdf 、 txt 、 md 的格式文本傳入\n  
    (注意: 請確保課程教材的正確性、合理性以及可靠性)
    """)
bookclub_name = st.text_input("輸入讀書會名稱")



add_materials_cols = st.columns([1, 4])
with add_materials_cols[1]:
    files_key = f"{bookclub_name}-materials"
    files = st.file_uploader(
        "上傳本讀書會的教材文件", 
        key=files_key,
        accept_multiple_files=True, 
        label_visibility="collapsed")

with add_materials_cols[0]:
    button_key = f"{bookclub_name}-materials-btn"
    button_materials = st.button("確認上傳", key=button_key, use_container_width=True)
        
if button_materials:
    # 將 files 的內容做切分，然後合併到課程的 VectorDB 中
    empty = st.empty()
    with empty:
        st.success(
            "成功添加進課程教材，您可以和學員一同使用 :red[**智慧檢索問答**] ，提升學習效率"
        )
        time.sleep(3)
        empty.empty()

build_group = st.button("確認建立")



if build_group:
    print("", st.session_state['user_id'])
    sql.update_user_group(user_id=st.session_state['user_id'], group_id=bookclub_name)
    time.sleep(1)
    print("sql FETCH:", sql.fetch_user_group(st.session_state['user_id']))
    st.session_state['group_list'] = sql.fetch_user_group(st.session_state['user_id'])
    print(sql.fetch_user_group(st.session_state['user_id']))
    st.success("成功建立讀書會")
    time.sleep(2)
    st.rerun()
    # st.switch_page("./pages/UserMain.py")


#
## Sidebar
#

with st.sidebar:
    st.write    ("# 新建讀書會")
    st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator(expanded_nav_user=False)
    navigators_logout_generator()            