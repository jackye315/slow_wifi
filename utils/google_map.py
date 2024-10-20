import requests

def google_directions(destination:str, origin:str, mode:str, api_key:str, **kwargs):
    params = {
        "destination": destination,
        "origin": origin,
        "mode": mode,
        "key": api_key,
    }

    uri = "https://maps.googleapis.com/maps/api/directions/json"
    response = requests.get(uri, params=params)
    return response.json()

def directions_output(response) -> tuple[list, str, str]:
    direction_list = []
    for route in response["routes"]:
        for leg in route["legs"]:
            for step in leg["steps"]:
                word_instructions = step['html_instructions']
                distance = step["distance"]["text"]
                duration = step["duration"]["text"]
                step_mode = step["travel_mode"]
                step_dict = {
                        "instructions":word_instructions,
                        "distance":distance,
                        "duration":duration,
                        "step_mode":step_mode,
                }
                if step_mode == "WALKING" and 'steps' in step:
                    street_instructions = []
                    for street_steps in step["steps"]:
                        street_instructions.append(street_steps['html_instructions'])
                    step_dict['street_instructions'] = street_instructions

                if step_mode == "TRANSIT":
                    step_dict['line'] = step['transit_details']['line']['short_name']
                    step_dict['vehicle'] = step['transit_details']['line']['vehicle']['name']
                    step_dict['departure_stop'] = step['transit_details']['departure_stop']['name']
                    step_dict['arrival_stop'] = step['transit_details']['arrival_stop']['name']
                    step_dict['num_stops'] = step['transit_details']['num_stops']

                direction_list.append(step_dict)
    
    if len(response['routes']) != 0:
        origin = response['routes'][0]['legs'][0]['start_address']
        destination = response['routes'][0]['legs'][0]['end_address']
    else:
        origin = ""
        destination = ""
    return direction_list, origin, destination

def google_map_autocomplete(input_text, api_key, **kwargs):
    params = {
        "input":input_text,
        "types":"geocode",
        "key": api_key,
    }

    uri = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
    response = requests.get(uri, params=params)
    return response.json()

if __name__=="__main__":

    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ['google_api_key']

    destination = "30 Rock"
    origin = "120 Ridge Street, New York"
    mode = "walking"
    response = google_directions(destination=destination, origin=origin, mode=mode, api_key=api_key)
    directions = directions_output(response)

    response = google_map_autocomplete(input_text="30 Rockefeller Plaza", api_key=api_key)
    print(response)