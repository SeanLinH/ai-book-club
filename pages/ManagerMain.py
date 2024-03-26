import streamlit as st
import time
from sidebar_navigators import \
    navigators_generator, \
    navigators_logout_generator



## session state
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

# TODO (Database API)
_test_host_bookclub_name = [
    "LLM 讀書會", "AI 醫療讀書會", "紅樓夢讀書會", "余光中精選讀書會"
]


# Session state


if "host_bookclub_name" not in st.session_state:
    st.session_state["host_bookclub_name"] = _test_host_bookclub_name


#
## Meta
#

st.set_page_config(
    page_title="智能讀書會-讀書會管理員主頁"
)

#
## Main
#

st.markdown("# 由您所管理的讀書會")

tabs = st.tabs(st.session_state["host_bookclub_name"])
for bookclub_order, tab in enumerate(tabs):
    with tab:
        bookclub_name = st.session_state["host_bookclub_name"][bookclub_order]
        st.markdown(f"### {bookclub_name}空間")

        st.markdown("#### 讀書會管理員名單")
        # 目前這部分先亂填一些文字
        st.markdown("""Lorem ipsum dolor sit amet consectetur adipisicing 
                    elit. Illum numquam voluptates, tempora unde inventore
                        autem dolores libero ab voluptate nam, odio totam min
                    ima voluptatibus beatae alias modi ut ipsum voluptas e
                    ius et cum. Exercitationem reiciendis suscipit totam d
                    electus magnam, facere vel laboriosam adipisci nostrum 
                    ab atque repudiandae modi. Repudiandae fugiat incidunt
                        adipisci officiis, vero, hic est veniam dicta, molest
                    ias distinctio asperiores eligendi non maxime nulla se
                    qui voluptatem quisquam natus quas exercitationem, 
                    blanditiis consequatur dolorem eveniet qui!""")

        add_member_cols = st.columns([1, 4])
        with add_member_cols[1]:
            text_key = f"{bookclub_name}-add-member"
            id_text = st.text_input(
                "輸入使用者 id", 
                key=text_key, 
                label_visibility="collapsed",
                placeholder="請輸入使用者 id"
            )

        with add_member_cols[0]:
            button_key = f"{bookclub_name}-add-btn"
            button_add = st.button("新增管理人員", key=button_key, use_container_width=True)

        if button_add:
            # 將 id_text 的 id 作為輸入，
            # 增加此讀書會的 bookclub_id 到那個用戶的 
            # host_bookclub_name 中
            empty = st.empty()
            with empty:
                st.success("成功邀請對方，對方可以一起管理讀書會了")
                time.sleep(3)
                empty.empty()

        st.markdown("#### 加入讀書會參考教材")
        st.markdown("""
            支持以 pdf 、 txt 、 md 的格式文本傳入\n  
            (注意: 請確保課程教材的正確性、合理性以及可靠性)
            """)

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





#
## Sidebar
#

with st.sidebar:
    st.write("# 讀書會管理員主頁")
    st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator(expanded_nav_user=False)
    navigators_logout_generator()

