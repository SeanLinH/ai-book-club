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