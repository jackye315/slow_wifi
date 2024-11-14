import requests
import asyncio
import httpx
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scrape.read_webpage import text_from_html_llm, a_text_from_html_llm, text_from_html_langchain, get_gemini_model

def google_search(search_query:str, api_key:str, engine_id_cx:str, **kwargs):
    
    params = {
        "q": search_query,
        "key": api_key,
        "cx": engine_id_cx,
    }

    if "date_filter" in kwargs:
        params["dateRestrict"] = kwargs["date_filter"]
    if "num_results" in kwargs:
        params["num"] = kwargs["num_results"]
    if "country_code" in kwargs:
        params["gl"] = kwargs["country_code"]

    uri="https://www.googleapis.com/customsearch/v1"
    response = requests.get(uri, params=params)
    return response.json()

def clean_search_output(google_results):
    output = []
    for item in google_results['items']:
        output_dict = {}
        output_dict['link'] = item['link']
        output_dict['title'] = item['title']
        output_dict['snippet'] = item['snippet']
        output.append(output_dict)
    return output

def get_results_content_llm(output_list, model):
    for output in output_list:
        link = output['link']
        response = requests.get(link)
        output['extracted_content'] = text_from_html_llm(response.text, model=model)
    return output_list

async def a_get_results_content_llm(output_list, model):
    for output in output_list:
        link = output['link']
        async with httpx.AsyncClient() as client:
            response = await client.get(link)
            output['a_extracted_content'] = await a_text_from_html_llm(response.text, model=model)
    return output_list

def get_results_content_langchain(output_list):
    for output in output_list:
        link = output['link']
        output['extracted_content'] = text_from_html_langchain(url=link)
    return output_list

if __name__=="__main__":
    import google.generativeai as genai

    import os
    from dotenv import load_dotenv
    load_dotenv()
    google_api_key = os.environ['google_api_key']
    gemini_api_key = os.environ['gemini_api_key']
    reddit_engine_id_cx = os.environ['google_reddit_engine_id_cx']
    full_engine_id_cx = os.environ['google_all_engine_id_cx']

    search_query = "nfl week 11 results"
    results = google_search(search_query=search_query, api_key=google_api_key, engine_id_cx=full_engine_id_cx, num_results=5)
    output_list = clean_search_output(results)
    output_list = get_results_content_langchain(output_list=output_list)

    model = get_gemini_model(api_key=gemini_api_key)
    cleaned_question = model.generate_content([search_query, "Turn the above search query into a appropriate question. If the topic is time based, assume it is in the past unless specified"]).text
    gemini_params = genai.types.GenerationConfig(temperature=0.0)
    response = model.generate_content([*[f"Article {index+1}:\n{output['extracted_content']}" for index, output in enumerate(output_list)],cleaned_question], generation_config=gemini_params)
    response.text

    # import time

    # start_time = time.time()
    # output_list = get_results_content_llm(output_list=output_list, model=model)
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Regular Elapsed time: {elapsed_time} seconds")

    # a_start_time = time.time()
    # output_list = asyncio.run(a_get_results_content_llm(output_list=output_list, model=model))
    # a_end_time = time.time()
    # a_elapsed_time = a_end_time - a_start_time
    # print(f"Async Elapsed time: {a_elapsed_time} seconds")

    print("END")