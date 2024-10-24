import streamlit as st
import requests
from scrape.read_webpage import get_gemini_model, text_from_html, text_from_html_llm, summarize_article, answer_question

import os
from dotenv import load_dotenv
load_dotenv()
gemini_api_key = os.environ['gemini_api_key']

def web():
    st.title('Scrape any web page')
    input_url = st.text_input("Url Link")

    model = get_gemini_model(model_name="gemini-1.5-flash", api_key=gemini_api_key)
    
    if st.button('Scrape'):
        response = requests.get(input_url)
        st.write(text_from_html_llm(response.text, model=model).replace("$", "\$"))

    if st.button('Summarize'):
        response = requests.get(input_url)
        st.write(summarize_article(text_from_html(response.text), model=model).replace("$", "\$"))

    question_box = st.text_input("Ask a question here!")
    if st.button('Answer') and question_box:
        response = requests.get(input_url)
        st.write(answer_question(text_from_html(response.text), question_box, model=model).replace("$", "\$"))