import streamlit as st
from utils.google_map import google_directions, directions_output, google_map_autocomplete

import os
from dotenv import load_dotenv
load_dotenv()
google_api_key = os.environ['google_api_key']
google_engine_id_cx = os.environ['google_engine_id_cx']

def directions():
    st.title('Get Directions to Anywhere')

    if 'origin' not in st.session_state:
        st.session_state['origin'] = ""
    if 'destination' not in st.session_state:
        st.session_state['destination'] = ""
    if 'potential_origins' not in st.session_state:
        st.session_state['potential_origins'] = []
    if 'potential_destinations' not in st.session_state:
        st.session_state['potential_destinations'] = []
    if 'route_found' not in st.session_state:
        st.session_state['route_found'] = True
    if 'autocomplete_exist' not in st.session_state:
        st.session_state['autocomplete_exist'] = False

    origin = st.text_input("Enter Origin Here", value=st.session_state.origin)
    destination = st.text_input("Enter Destination Here", value=st.session_state.destination)

    mode = st.selectbox(
            label = "Transit Option",
            options = ("Walking", "Transit", "Bicycling", "Driving"), 
            index=0
        )
    if st.button("Get Directions"):
        st.session_state.potential_origins = []
        st.session_state.potential_destinations = []
        st.session_state.route_found = True
        st.session_state.autocomplete_exist = False
        st.session_state.origin = origin
        st.session_state.destination = destination
        directions, direction_origin, direction_destination = directions_output(google_directions(destination=st.session_state.destination, origin=st.session_state.origin, mode=mode.lower(), api_key=google_api_key))
        if len(directions) == 0:
            st.session_state.route_found = False
        else:
            st.write(f"{direction_origin} -> {direction_destination}")
            for index, direction in enumerate(directions):
                st.markdown(f"Step {index+1}: {direction['instructions']}",unsafe_allow_html=True)
                indent_text = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                st.markdown(f"{indent_text}Distance: {direction['distance']}, Duration: {direction['duration']}")
                if direction['step_mode'].lower() == "transit":
                    st.markdown(f"{indent_text}Vehicle: {direction['vehicle']}, {direction['line']}")
                    st.markdown(f"{indent_text}From {direction['departure_stop']} to {direction['arrival_stop']}, {direction['num_stops']} stops")
                if 'street_instructions' in direction:
                    more_indent_text = indent_text + indent_text
                    for street_instruction in direction['street_instructions']:
                        st.markdown(f"{more_indent_text}{street_instruction}", unsafe_allow_html=True)
    
    def update_origin():
        st.session_state.origin = st.session_state.selected_origin
    
    def update_destination():
        st.session_state.destination = st.session_state.selected_destination

    if not st.session_state.route_found:
        st.write("Route Not Found. Did you mean one of these?")
        if not st.session_state.autocomplete_exist:
            potential_origins = google_map_autocomplete(input_text=st.session_state.origin, api_key=google_api_key)
            potential_destinations = google_map_autocomplete(input_text=st.session_state.destination, api_key=google_api_key)
            st.session_state.potential_origins = potential_origins
            st.session_state.potential_destinations = potential_destinations
            st.session_state.autocomplete_exist = True

        col1, col2 = st.columns(2)
        with col1:
            autocomplete_origin = st.selectbox(
                label = "Found Origins",
                options = [x['description'] for x in st.session_state.potential_origins['predictions']],
                index = 0,
                key='selected_origin',
                on_change=update_origin
            )
        with col2:
            autocomplete_destination = st.selectbox(
                label = "Found Destinations",
                options = [x['description'] for x in st.session_state.potential_destinations['predictions']],
                index = 0,
                key='selected_destination',
                on_change=update_destination
            )