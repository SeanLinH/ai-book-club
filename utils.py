import streamlit as st
import re


def change_user_state(state):
    state["user"] = not state["user"]

# 確認電子郵件地址是否有效
def is_email_valid(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False
    

def generate_html(key, default_value=""):
    return f"""
    <html>
    <body>
        <script>
        // 尝试从 Local Storage 读取数据
        var savedData = localStorage.getItem("{key}");
        if (savedData) {{
            // 如果成功读取，发送数据到 Streamlit
            parent.postMessage({{event: 'streamlit:setComponentValue', data: savedData}}, '*');
        }} else {{
            // 如果没有读取到数据，使用默认值
            localStorage.setItem("{key}", "{default_value}");
            parent.postMessage({{event: 'streamlit:setComponentValue', data: "{default_value}"}}, '*');
        }}
        </script>
    </body>
    </html>
    """

