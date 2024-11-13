from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import asyncio
from langchain_community.document_loaders import WebBaseLoader
from typing import Union, List

import google.generativeai as genai

def get_gemini_model(api_key:str, model_name:str="gemini-1.5-flash"):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def text_from_html_llm(body, model):
    clean_html_prompt = "Remove all html elements and keep only the text in the article. If there are any images or videos, also remove those."
    return model.generate_content([body, clean_html_prompt]).text

async def a_text_from_html_llm(body, model):
    clean_html_prompt = "Remove all html elements and keep only the text in the article. If there are any images or videos, also remove those."
    a_response = await model.generate_content_async([body, clean_html_prompt])
    return a_response.text

def text_from_html_langchain(url:str) -> str:
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs[0].page_content

def summarize_article(article_text:str, model):
    response = model.generate_content([article_text, "Can you summarize the key points in this article?"])
    return response.text

def answer_question(article_text:str, question:str, model):
    response = model.generate_content([article_text, f"Answer the question with the above information: {question}"])
    return response.text

if __name__=="__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    gemini_api_key = os.environ['gemini_api_key']
    
    models = ["gemini-1.5-pro","gemini-1.5-flash"]
    model = get_gemini_model(model_name=models[1],api_key=gemini_api_key)
    
    url = 'https://www.pickleheads.com/pickleball-gear/best-pickleball-paddle-for-beginners'
    response = requests.get(url)
    extracted_web = text_from_html_llm(response.text, model=model)
    print(extracted_web)

    extracted_langchain = text_from_html_langchain(url)
    extracted_langchain