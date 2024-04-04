import streamlit as st
from sidebar_navigators import \
    navigators_generator, \
    navigators_logout_generator




## config
st.set_page_config(
    page_title="AI 智能讀書會",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
    
)


permissible_keys = {"user", "user_id"}

if "user" not in st.session_state:
    st.session_state["user"] = False
    st.session_state['group_list'] = []

# for key in st.session_state.keys():
#     if key not in permissible_keys:
#         st.session_state.pop(key)


for key in st.session_state.keys():
    if key not in permissible_keys:
        st.session_state.pop(key)
#
## Main
#
#markdown 匯入圖片


st.markdown(f"""## AI智能讀書會平台介紹""")
st.image("src/images/logo.png", width=400, clamp=True)
st.markdown(f"""
### 簡介
AI智能讀書會是一個創新的學習共享平台，旨在促進知識的深度交流與協作學習。透過這個平台，用戶可以加入特定的學習群組，共同研究和討論學術論文或其他學習材料。本平台特色在於引入AI技術，以智能方式支持問題解答和內容理解，使學習過程更加高效、互動。

### 情境
- **學術研究**：學者和研究生可以上傳並討論最新的學術論文，深入探討研究方法和結果。
- **技術學習**：IT專業人士和學生可以分享技術文檔或教程，共同解決技術難題。
- **專業發展**：對特定領域感興趣的專業人士可以進行深入討論，擴展專業知識。

### 使用方法
1. **註冊並加入群組**：用戶首先需要註冊賬號，然後根據興趣或專業領域加入相應的學習群組。
2. **上傳學習材料**：用戶可以上傳學習材料，如學術論文或技術文檔，供群組成員共同學習。
3. **提問與回答**：針對材料，用戶可以提出問題，這些問題會被列入問題清單。用戶可以根據自己的知識和興趣回答問題，也可以使用AI輔助回答。

### 使用對象
- 學者、研究生和其他學術研究人員。
- IT專業人士、開發者和技術愛好者。
- 對特定領域有深入學習需求的專業人士。

### 應用技術
- **自然語言處理（NLP）**：用於理解和生成對學習材料的問題和回答。
- **機器學習與深度學習**：分析用戶行為，根據用戶的專業領域和興趣對問題和材料進行個性化排序。
- **知識圖譜**：構建專業領域內的知識關聯，幫助更準確地匹配問題和回答，並提供深入的學習資源。

AI智能讀書會平台致力於打造一個智能化、互動性強的學習社群，通過技術創新促進知識的交流與共享，為用戶提供一個全新的學習體驗。
""")


#
## Sidebar
#

with st.sidebar:
    st.write("# Welcome")
    st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    # st.page_link("./app.py", label="知識問答")
    
    # dropdown_value = st.selectbox("Select an option", ["Option 1", "Option 2", "Option 3"])
    navigators_generator()
    navigators_logout_generator()


#
## TESTING COMPONENTS
#

### test use modules and functions
from utils import change_user_state

if st.button(":green[change user state]"):
    change_user_state(st.session_state)
    st.rerun()

on_toggle_btn = st.toggle(":red[See Session state]")
if on_toggle_btn:
    st.write(f"Now session state is: :red[{st.session_state}]")

