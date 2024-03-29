import streamlit as st
import openai
from dotenv import load_dotenv
import os 


# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# Define function to generate AI response
def generate_ai_response(message):
    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": message}],
        max_tokens=50,
        temperature=0.3
    )
    return response.choices[0].text.strip()

    # Define function to handle user input and generate AI response

def chatbot():
    st.title("AI Chatbot")
    message = st.chat_input("User Input")
    if st.button("Send"):
        ai_response = generate_ai_response([{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": message}])
        st.chat_message("AI Response", value=ai_response, height=200, max_chars=None)

# Run the chatbot function
if __name__ == "__main__":
    chatbot()