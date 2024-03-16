import streamlit as st


def change_user_state(state):
    state["user"] = not state["user"]
