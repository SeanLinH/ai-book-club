import streamlit as st
import uuid
from typing import *
import openai
import os
import sql
import time
from api.ChatGPT import ans_question
from sidebar_navigators import \
    navigators_generator, \
    navigators_logout_generator
from api import Mail
import streamlit as st
from streamlit_chat import message


openai.api_key = os.environ.get("OPENAI_API_KEY")
## session state
permissible_keys = {
    "user", 
    "user_id",
    "user_info",
    "group_list",
    "group_id_list",
    "group_id",
    "user_email",
    "topic",
    "questions_list",
    "qst_text"
}

# for key in st.session_state.keys():
#     if key not in permissible_keys:
#         st.session_state.pop(key)

for key in permissible_keys:
    if key not in st.session_state.keys():
        st.session_state[key] = [""]
if st.session_state['user'] == [""]:
    st.session_state['user'] = False
    st.switch_page("./pages/Login.py")
    
st.set_page_config(
    page_title="AI智能讀書會-提問大廳",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

st.session_state['questions_list'] = []
for _,_,qst_text in sql.fetch_group_qst(st.session_state['group_id']):
    st.session_state['questions_list'].append(qst_text)

topic = st.session_state['topic']
if topic =="":
    st.switch_page("./pages/UserMain.py")


# Chatroom interface
# st.title("AI Chatroom")
# message("My message") 
# message("Hello bot!", is_user=True)  # align's the message to the right

import openai
import streamlit as st
from streamlit_chat import message


# Generating responses from the api

def generate_response(prompt):
    completions = openai.chat.completions.create(
        model = "gpt-4-1106-preview",
        messages = [{"role": "system", "content": "You are a helpful assistant."}, 
                    {"role": "user", "content": prompt}],
        max_tokens = 1024,
        temperature = 0.9,
        # stream=True
    )
    messages = completions.choices[0].message.content
    return messages

# Creating the chatbot interfaces

st.title("討論區")

# Storing the input

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Creating a function that returns the user's input from a text input field

def get_text():
    input_text = st.chat_input("your message", key = "input")
    return input_text

# We will generate response using the 'generate response' function and store into variable called output

user_input = get_text()

if user_input:
    output = generate_response(user_input)

    # Store the output
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)


# Finally we display the chat history
if st.session_state['generated']:
    
    for i in range(len(st.session_state['generated'])):
        message('sean:\n' +st.session_state["past"][i], is_user=True, allow_html=True, key=str(i) + '_user')
        message('SageLink:\n' + st.session_state["generated"][i],allow_html=True, key=str(i))
        



# User input

# user_input = st.chat_input("聊天窗") #st.text_input("Ask a question")

# if user_input:
#     st.write("AI is typing...")
#     time.sleep(1)
#     st.write(ans_question(topic, st.session_state['qst_text'], st.session_state['user_id']))

#
## Sidebar
#

with st.sidebar:
    st.write("# 聊天窗")
    # st.page_link("./AIBookClub.py", label="智能讀書會主頁")
    navigators_generator()
    navigators_logout_generator()

