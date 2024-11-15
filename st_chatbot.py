import streamlit as st

import google.generativeai as genai
from typing import Union, List

import os
from dotenv import load_dotenv
load_dotenv()
gemini_api_key = os.environ['gemini_api_key']

def get_gemini_model(model_name:str="gemini-1.5-flash", safety_settings:dict={}, api_key:str=gemini_api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name, safety_settings=safety_settings)

def gemini_chat(model, query:Union[str, List[str]], chat=None):
    if not chat:
        chat = model.start_chat()
    response = chat.send_message(query)
    return chat, response.text

def chatbot():
    st.title("Bootleg ChatGPT")

    # Initialize session state for storing the conversation
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    if 'gemini_model' not in st.session_state:
        st.session_state.gemini_model = "gemini-1.5-flash"
    if 'gemini_history' not in st.session_state:
        st.session_state.gemini_history = None

    model = get_gemini_model(model_name=st.session_state.gemini_model, api_key=gemini_api_key)

    # Define your list of options
    options = ["gemini-1.5-flash", "gemini-1.5-pro"]
    with st.sidebar:
        selected_option = st.radio('Gemini Model:', options, index=0)
        st.session_state.gemini_model = selected_option

    # Function to simulate a chatbot response
    def chatbot_response(user_input):
        st.session_state.gemini_history, chat_resonse = gemini_chat(model=model, query=user_input, chat=st.session_state.gemini_history)
        return chat_resonse
    
    def chatbot_action():
        user_input = st.session_state.user_input
        if user_input:
            # Append user message to the conversation history
            st.session_state.messages.append(f"You: {user_input}")
            
            # Generate chatbot response and append it to the conversation history
            bot_reply = chatbot_response(user_input)
            st.session_state.messages.append(bot_reply)
            
            st.session_state.user_input = ""

    # Custom CSS for message styling to allow right-align for user
    st.markdown(
        """
    <style>
        .st-emotion-cache-janbn0 {
            flex-direction: row-reverse;
            text-align: right;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Display conversation in a chat-like layout
    for i, message in enumerate(st.session_state.messages):
        role = "user" if i % 2 == 0 else "bot"  # Alternate between user and bot messages
        with st.chat_message(role):
            st.write(message)
        
    # Clear button
    if st.button("Clear", key="clear_button"):
        st.session_state.messages = []
        st.session_state.gemini_history = None
        st.rerun()

    # User input
    st.divider()  # Optional divider for a cleaner separation
    user_input = st.text_input("You:", key="user_input", on_change=chatbot_action)
