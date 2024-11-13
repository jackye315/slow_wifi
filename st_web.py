import streamlit as st
import requests
from scrape.read_webpage import get_gemini_model, text_from_html, text_from_html_llm, summarize_article, answer_question, text_from_html_langchain
from utils.google_search import google_search, clean_search_output, get_results_content_langchain

import os
from dotenv import load_dotenv
load_dotenv()
google_api_key = os.environ['google_api_key']
full_engine_id_cx = os.environ['google_all_engine_id_cx']
gemini_api_key = os.environ['gemini_api_key']
model = get_gemini_model(model_name="gemini-1.5-flash", api_key=gemini_api_key)

def one_web():
    st.title('Scrape any web page')
    input_url = st.text_input("Url Link")

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

def web_search():
    st.title('Bootleg Perplexity')
    input_question = st.text_input("Search Google")

    if st.button('Search') and input_question:
        results = google_search(search_query=input_question, api_key=google_api_key, engine_id_cx=full_engine_id_cx, num_results=5)
        output_list = clean_search_output(results)
        output_list = get_results_content_langchain(output_list=output_list)
        answer = model.generate_content([*[output['extracted_content'] for output in output_list],input_question]).text
        st.write(answer.replace("$", "\$"))
        st.write("Sources:")
        for output in output_list:
            st.write(output['link'].replace("$", "\$"))
    else:
        st.write('Enter a question and find your answer - powered by Gemini')

    