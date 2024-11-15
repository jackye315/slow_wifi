import streamlit as st
from st_directions import directions
from st_reddit import reddit_link, reddit_search
from st_web import one_web, web_search
from st_price import price_compare
from st_chatbot import chatbot

if __name__=="__main__":
    
    web_page = st.Page(one_web, title="Webpage", icon=":material/web:")
    web_search_page = st.Page(web_search, title="Web Search", icon=":material/search:")
    reddit_link_page = st.Page(reddit_link, title="Reddit", icon=":material/forum:")
    reddit_search_page = st.Page(reddit_search, title="Reddit Search", icon=":material/search_insights:")
    directions_page = st.Page(directions, title="Directions", icon=":material/map:")
    price_page = st.Page(price_compare, title="Compare Prices", icon=":material/money:")
    chatbot_page = st.Page(chatbot, title="Chatbot", icon=":material/smart_toy:")
    pg = st.navigation(
        {
            "Web": [web_page, web_search_page],
            "Reddit": [reddit_link_page, reddit_search_page],
            "Navigation":[directions_page],
            "Buying":[price_page],
            "Chat":[chatbot_page],
        }
    )
    pg.run()