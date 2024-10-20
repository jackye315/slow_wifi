import streamlit as st
from st_directions import directions
from st_reddit import reddit_link, reddit_search
from st_web import web

if __name__=="__main__":
    
    web_page = st.Page(web, title="Webpage", icon=":material/web:")
    reddit_link_page = st.Page(reddit_link, title="Reddit", icon=":material/forum:")
    reddit_search_page = st.Page(reddit_search, title="Reddit Search", icon=":material/search:")
    directions_page = st.Page(directions, title="Directions", icon=":material/map:")
    pg = st.navigation(
        {
            "Web": [web_page],
            "Reddit": [reddit_link_page, reddit_search_page],
            "Navigation":[directions_page]
        }
    )
    pg.run()