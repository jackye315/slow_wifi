import requests

def google_search(search_query:str, api_key:str, engine_id_cx:str, **kwargs):
    
    params = {
        "q": search_query,
        "key": api_key,
        "cx": engine_id_cx,
    }

    if "date_filter" in kwargs:
        params["dateRestrict"] = kwargs["date_filter"]

    uri="https://www.googleapis.com/customsearch/v1"
    response = requests.get(uri, params=params)
    return response.json()

def clean_search_output(google_results):
    output = []
    for item in google_results['items']:
        output.append(item['link'])
    return output


if __name__=="__main__":
    
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ['google_api_key']
    engine_id_cx = os.environ['google_reddit_engine_id_cx']

    search_query = "best pickleball paddle beginners"
    results = google_search(search_query=search_query, api_key=api_key, engine_id_cx=engine_id_cx)
    clean_search_output(results)