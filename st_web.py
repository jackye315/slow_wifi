import streamlit as st
import requests
from scrape.read_webpage import get_gemini_model, text_from_html, text_from_html_llm, summarize_article, answer_question, text_from_html_langchain
from utils.google_search import google_search, clean_search_output, get_results_content_langchain
import google.generativeai as genai

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
    if 'input_question' not in st.session_state:
        st.session_state.input_question = ""
    if 'search' not in st.session_state:
        st.session_state.search = False
    
    st.title('Bootleg Perplexity')
    input_question = st.text_input("Search Google", value=st.session_state.input_question)

    def get_answer(question):
        results = google_search(search_query=question, api_key=google_api_key, engine_id_cx=full_engine_id_cx, num_results=5)
        output_list = clean_search_output(results)
        output_list = get_results_content_langchain(output_list=output_list)
        cleaned_question = model.generate_content([question, "Turn the above search query into a appropriate question. If the topic is time based, assume it is in the past unless specified"]).text
        st.write(cleaned_question.replace("$", "\$"))
        gemini_params = genai.types.GenerationConfig(temperature=0.0)
        answer = model.generate_content([*[f"Article {index+1}:\n{output['extracted_content']}" for index, output in enumerate(output_list)],cleaned_question], generation_config=gemini_params).text
        st.write(answer.replace("$", "\$"))
        st.write("Sources:")
        for output in output_list:
            st.write(output['link'].replace("$", "\$"))
    
    if st.button('Search') and input_question:
        st.session_state.input_question = input_question
        get_answer(question=st.session_state['input_question'])
        st.session_state.search = True
    else:
        st.write('Enter a question and find your answer - powered by Gemini')
    
    if st.session_state.search:
        if st.button("Regenerate"):
            different_question = model.generate_content([input_question, "Modify the above search query. Keep it about the same length. Only return the new search query."]).text
            st.session_state.input_question = different_question
            st.rerun()


    