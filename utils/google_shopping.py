from serpapi import GoogleSearch
import pandas as pd

def google_price(item_query:str, api_key:str):
    
    params = {
    "engine": "google_shopping",
    "q": item_query,
    "api_key": api_key,
    }

    search = GoogleSearch(params)
    return search.get_dict()

def clean_price_output(price_results):
    return pd.DataFrame(results['shopping_results'])

def max_min_avg_price(price_df:pd.DataFrame):
    price_df['price_float'] = price_df['price'].replace('[^\d.]', '', regex=True).astype(float)
    return price_df['price_float'].max(), price_df['price_float'].min(), price_df['price_float'].mean()

def filter_searches(price_df:pd.DataFrame, filter_amount:int = 10, second_hand: bool=False) -> pd.DataFrame:
    if not second_hand:
        price_df = price_df[price_df['second_hand_condition'].isna()]
    top_by_rating = price_df.sort_values(by=['rating']).head(filter_amount)
    top_by_reviews = price_df.sort_values(by=['reviews']).head(filter_amount)
    return price_df[price_df['position'].isin(top_by_rating['position']) & price_df['position'].isin(top_by_reviews['position'])]



if __name__=="__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ['serpapi_api_key']

    results = google_price(item_query="Macbook M3", api_key=api_key)
    shopping_results = results["shopping_results"]
    price_df = clean_price_output(results)
    print(max_min_avg_price(price_df))
    filtered_df = filter_searches(price_df)