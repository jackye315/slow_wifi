import streamlit as st
from scrape.read_reddit import get_post_and_comments, reddit_setup
from utils.google_search import google_search, clean_search_output

import os
from dotenv import load_dotenv
load_dotenv()
reddit_client_id = os.environ['reddit_client_id']
reddit_client_secret = os.environ['reddit_client_secret']
reddit_user = os.environ['user']
google_api_key = os.environ['google_api_key']
google_engine_id_cx = os.environ['google_reddit_engine_id_cx']

def _reddit_st_post(post_data):
    st.write(post_data['title'].replace("$", "\$"))
    st.write(post_data['link'].replace("$", "\$"))
    st.write((f"Author: {post_data['author']}, Upvotes: {post_data['score']}").replace("$", "\$"))
    st.write(post_data['body_text'].replace("$", "\$"))

def _reddit_st_conversation(comment_conversations):
    for conversation in comment_conversations:
        st.write("-------")
        for comment in conversation:
            st.write((f"{comment.author}, {comment.score}: {comment.body}").replace("$", "\$"))

def reddit_link():
    st.title('Scrape Reddit Link')
    input_url = st.text_input("Reddit Url Link")

    if st.button('Scrape'):
        reddit = reddit_setup(client_id=reddit_client_id,client_secret=reddit_client_secret,user=reddit_user)
        post_data, comment_conversations = get_post_and_comments(reddit, input_url)
        _reddit_st_post(post_data)
        _reddit_st_conversation(comment_conversations)

def reddit_search():
    st.title('Search & Scrape Reddit')

    search_query = st.text_input("Enter Search Query Here")
    
    col1,col2,col3 = st.columns([1,1,2])
    with col1:
        date_unit = st.selectbox(
            label = "Date Range for Search",
            options = ("Any Time", "Days", "Weeks", "Months", "Years"), 
            index=0
        )
        st.session_state.date_unit = date_unit
    with col2:
        default_amount = None if st.session_state.date_unit == "Any Time" else 5
        date_amount = st.number_input(
            label = "Date Amount for Search",
            step = 1,
            value = default_amount
        )
        st.session_state.date_amount = date_amount
    if st.button('Search & Scrape'):
        st.session_state.search_query = search_query
        if "date_unit" in st.session_state and st.session_state.date_unit != "Any Time":
            google_date_dict = {"Days":"d", "Weeks":"w", "Months":"m", "Years":"y"}
            date_filter = f"{google_date_dict[st.session_state.date_unit]}[{st.session_state.date_amount}]"
            results = google_search(search_query=search_query, date_filter=date_filter, api_key=google_api_key, engine_id_cx=google_engine_id_cx)
        else:
            results = google_search(search_query=search_query, api_key=google_api_key, engine_id_cx=google_engine_id_cx)
        reddit_links = clean_search_output(results)

        reddit = reddit_setup(client_id=reddit_client_id,client_secret=reddit_client_secret,user=reddit_user)
        st.session_state.posts = []
        st.session_state.comments = []
        for link in reddit_links:
            post_data, comment_conversations = get_post_and_comments(reddit, link)
            st.session_state.posts.append(post_data)
            st.session_state.comments.append(comment_conversations)

    if 'search_query' in st.session_state:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            button_a = st.button('Result 1')
        with col_b:
            button_b = st.button('Result 2')
        with col_c:
            button_c = st.button('Result 3')
        if button_a:
            _reddit_st_post(st.session_state.posts[0])
            _reddit_st_conversation(st.session_state.comments[0])
        if button_b:
            _reddit_st_post(st.session_state.posts[1])
            _reddit_st_conversation(st.session_state.comments[1])
        if button_c:
            _reddit_st_post(st.session_state.posts[2])
            _reddit_st_conversation(st.session_state.comments[2])