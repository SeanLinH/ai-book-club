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


if "user_info" not in st.session_state:
    st.session_state["user_info"] = {
        "user_name": st.session_state["user_id"],
        "domain": "智慧製造",
        "role": "AI工程師",
        "goal": "我希望可以增進自己的知識水平"
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
st.markdown("""# AI智能讀書會介紹

歡迎加入**AI智能讀書會**！這是一個專為跨領域人才設計的學習社群，旨在促進知識的自由流通與分享。無論您是AI領域的專家，還是對其他學科懷有濃厚興趣的學習者，這裡都是您不可多得的交流平台。

## 特色

- **跨領域學習**：涵蓋AI、數據科學、機器學習、深度學習等多個領域，讓知識無界限。
- **知識傳遞**：透過智能匹配系統，讓您能夠輕易地找到與您知識背景或興趣匹配的群組。
- **互助成長**：共同討論、學習，透過問題解決，實現個人與群體的共同進步。

## 如何加入

1. **點擊側邊欄的「建立讀書會群組」**：首先，請在本平台的側邊欄中找到並點擊「上傳教材/創建群組」按鈕。
2. **輸入使用者資訊**：根據引導，輸入您的相關資訊，包括但不限於您的興趣領域、專業背景等，以便我們為您匹配最適合的學習小組。
3. **開始探索**：完成上述步驟後，您將正式成為AI智能讀書會的一員，開啟您的跨領域學習之旅。

## 加入我們

立即行動，開拓您的學習視野，與來自世界各地的專家學者一同探索知識的海洋吧！

**讓我們攜手共創知識的未來。**
""")


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

