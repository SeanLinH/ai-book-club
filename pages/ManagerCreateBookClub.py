import streamlit as st
import time
from sidebar_navigators import \
    navigators_generator, \
    navigators_logout_generator
import sql
import random
import string
from io import StringIO
import pandas as pd
import os


## config

st.set_page_config(
    page_title="AI智能讀書會-建立群組",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

#
## Session state
#

def folder_path(bookclub_id):
    target_folder = f'src/data/{bookclub_id}-materials'
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    return target_folder

def show_materials(path):
    return ', '.join(os.listdir(path))

permissible_keys = {
    "user", 
    "user_id",
    "user_info",
    "group_list",
    "group_id_list",
    "group_id",
    "user_email",
    "topic"
}

for key in st.session_state.keys():
    if key not in permissible_keys:
        st.session_state.pop(key)

for key in permissible_keys:
    if key not in st.session_state.keys():
        st.session_state[key] = [""]
if st.session_state['user'] == [""]:
    st.session_state['user'] = False
    st.switch_page("./pages/Login.py")


#
## Meta
#


bookclub_name = st.session_state['topic']
bookclub_id = st.session_state['group_id']
#
## Main
#

st.markdown(f"""#### 加入[{bookclub_name}]參考教材
    支持以 pdf 、 txt 、 md 的格式文本傳入\n  
    (注意: 請確保課程教材的正確性、合理性以及可靠性)
    
    群組檔案列表:
    {show_materials(folder_path(bookclub_id))}
    """)


add_materials_cols = st.columns([1, 4])
with add_materials_cols[1]:
    files_key = f"{bookclub_id}-materials"
    files = st.file_uploader(
        "上傳本讀書會的教材文件", 
        # key=files_key,
        accept_multiple_files=True, 
        label_visibility="collapsed")
    

with add_materials_cols[0]:
    button_key = f"{bookclub_id}-materials-btn"
    button_materials = st.button("確認上傳", 
                                #  key=button_key, 
                                 use_container_width=True)
    remove_materials = st.button(":red[刪除所有教材]", use_container_width=True)
        

if remove_materials:
    target_folder = folder_path(bookclub_id)
    for file in os.listdir(target_folder):
        os.remove(os.path.join(target_folder, file))
    st.success("成功刪除所有教材")
    time.sleep(3)
    st.rerun()

if button_materials:
    st.write('upload!')
    path = folder_path(bookclub_id)
    
    if files is not []:
        for uploaded_file in files:
            bytes_data = uploaded_file.read()
            filename = uploaded_file.name
            file_path = os.path.join(path, filename)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"成功添加 :red[{uploaded_file.name}] 到 {bookclub_name} 的教材")

    empty = st.empty()
    with empty:
        time.sleep(3)
        empty.empty()
        st.rerun()
    

with st.expander("創建讀書會群組", expanded=True):        
    col1, col2 = st.columns([1, 1])
    with col1:
        new_bookclub_name = st.text_input("輸入讀書會的名稱", placeholder="ex.大型語言模型研究, 產品開發知識")
        build_group = st.button("確認建立")

        if build_group:
            if new_bookclub_name == "":
                st.warning("請輸入讀書會名稱")
            else:
                random_code = ''.join(random.choices(string.ascii_letters, k=8))
                msg = sql.update_user_group(user_id=st.session_state['user_id'], group_name=new_bookclub_name, group_id=random_code)
                st.session_state['group_list'], st.session_state['group_id_list'] = sql.fetch_user_group(st.session_state['user_id'])
                st.success("成功建立讀書會")
                time.sleep(2)
                # st.rerun()
                # st.switch_page("./pages/UserMain.py")
    with col2:
        join_group = st.text_input("輸入邀請群組碼", placeholder="NiAimKmy")
        join = st.button("加入群組")

        if join:
            if join_group == "":
                st.warning("請輸入群組碼")
            else:
                msg = sql.join_user_group(user_id=st.session_state['user_id'], group_id=join_group)
                st.session_state['group_list'], st.session_state['group_id_list'] = sql.fetch_user_group(st.session_state['user_id'])
                if msg == "成功加入群組":
                    st.success(msg)
                else:
                    st.warning(msg)
                time.sleep(2)
                st.rerun()
                # st.switch_page("./pages/UserMain.py")
            
    


with st.expander("退出群組"):
    build_group = st.button(f"退出當前群組: :red[{bookclub_name}]")
    if build_group:
        # group_list = st.session_state['group_list']
        # group_id_lst = st.session_state['group_id_list']
        # idx = group_list.index(bookclub_name)
        # group_list.pop(idx)
        # group_id_lst.pop(idx)
        group_id = st.session_state['group_id']
        group_name = st.session_state['topic']
        msg = sql.drop_user_group(user_id=st.session_state['user_id'], group_name=group_name, group_id=group_id)
        st.session_state['group_list'], st.session_state['group_id_list'] = sql.fetch_user_group(st.session_state['user_id'])
        if msg == "已退出群組!":
            st.success(msg)
        else:   
            st.warning(msg)
        time.sleep(2)
        st.rerun()


#
## Sidebar
#

with st.sidebar:
    st.write    ("# 新建讀書會")
    # st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator(expanded_nav_user=False)
    navigators_logout_generator()       
