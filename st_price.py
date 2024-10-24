import streamlit as st
from utils.google_shopping import google_price, clean_price_output, max_min_avg_price, filter_searches

import os
from dotenv import load_dotenv
load_dotenv()
serpapi_api_key = os.environ['serpapi_api_key']

def price_compare():
    st.title('Check Online Prices')
    
    if 'search_item' not in st.session_state:
        st.session_state['search_item'] = ""
    
    search_item = st.text_input("Enter Search Item", value=st.session_state.search_item)

    if st.button("Get Prices"):
        search_results = google_price(item_query=search_item, api_key=serpapi_api_key)
        results_df = clean_price_output(price_results=search_results)
        filtered_results_df = filter_searches(price_df=results_df)
        max_price, min_price, avg_price = max_min_avg_price(price_df=results_df)
        st.write((f"Max: ${int(max_price)}, Min: ${int(min_price)}, Average: ${int(avg_price)}").replace("$", "\$"))
        st.dataframe(data=filtered_results_df[['title','source', 'price', 'rating', 'reviews', 'old_price']])