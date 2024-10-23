import requests
import folium
import os

# Your API Key
api_key = "5b3ce3597851110001cf6248dbbfd26f49dd4c58b840fa14e75d49fd"




# Make the API request
locations =[] 

def get_coordinates(town_name):
    # Parameters for the geocoding request
    params = {
        "api_key": api_key,
        "text": town_name,
        "focus.point.lon": 37.5,  
        "focus.point.lat": -0.5,  
        "boundary.country": "KE",  # Focus on Kenya
        "sources": "osm,oa,gn,wof",  # Data sources
        "layers": "region,county"  # Only return region and county
    }
    # Endpoint URL
    url = f"https://api.openrouteservice.org/geocode/autocomplete?api_key={api_key}&text={params['text']}&focus.point.lon={params['focus.point.lon']}&focus.point.lat={params['focus.point.lat']}&boundary.country={params['boundary.country']}"  

    try:
        response = requests.get(url)

        # Check for HTTP errors
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.text}")
        else:

            try:
                data = response.json()  # Parse JSON response
                # print("Response JSON:", data)  # Print the entire JSON response
                
                # Check if there are any features
                if 'features' in data and data['features']:
                    location = data['features'][0]['geometry']['coordinates']
                    # location = location[::-1]
                    locations.append(location)
                    



                   
                else:
                    print("No features found in the response.")
                    
            except requests.exceptions.JSONDecodeError:
                print("Error: Unable to parse JSON. Response might be empty or not valid JSON.")
                print(f"Response content: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


town1 = str(input("Enter start point: "))
town2 = str(input("Enter End point: "))
coords = get_coordinates(town1)
coords = get_coordinates(town2)

def get_driving_route(api_key, start, end):
    """
    Fetch driving route data from OpenRouteService API.
    
    Parameters:
        api_key (str): Your OpenRouteService API key.
        start (str): Starting coordinates in the format "longitude,latitude".
        end (str): Ending coordinates in the format "longitude,latitude".
        
    Returns:
        dict: Route data from the API or None if there was an error.
    """


   # Construct the URL for the OpenRouteService API
    url = 'https://api.openrouteservice.org/v2/directions/driving-car'
    
    # Define parameters
    params = {
        'api_key': api_key,
        'start': f"{start[0]},{start[1]}", 
        'end': f"{end[0]},{end[1]}",         
        "focus.point.lon": 37.5,             
        "focus.point.lat": -0.5,             
    }
    
    # Send GET request to the API
    response = requests.get(url, params=params)
    
    # Check for a successful response
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        return data
    else:
        print(f"Error with the API request: {response.status_code} - {response.text}")
        return None


api_key = '5b3ce3597851110001cf6248dbbfd26f49dd4c58b840fa14e75d49fd'

# Coordinates for the start and end points
start = locations[0] 
end = locations[1]    

def get_route(start_coords, end_coords):
    # This function should return route data as a list of coordinates (lat, lng)
    # Example response: [{'lat': lat1, 'lng': lng1}, {'lat': lat2, 'lng': lng2}, ...]
    # Replace this with your actual API call to get route data
    route_data = [
        [start_coords[0], start_coords[1]],  # Start coordinates
        [end_coords[0], end_coords[1]]       # End coordinates
    ]
    # In practice, the route data will have more intermediate points for the road/path
    return route_data

route_coords = get_route(start,end) 
print(route_coords)

# Get driving route
route_data = get_driving_route(api_key, start, end)


  

# Check if route_data exists and extract the summary
if route_data and 'features' in route_data and route_data['features']:
    print("Route Data:")
    
    # Extract the first feature from features
    feature = route_data['features'][0]
    summary = feature['properties']['summary']
    distance = summary['distance'] / 1000  # Convert meters to kilometers
    duration = summary['duration'] / 60    # Convert seconds to minutes

    print(f"Distance: {distance:.2f} km")
    print(f"Duration: {duration:.2f} minutes")

    

    reversed_locations = [location[::-1] for location in locations]
    # print(reversed_locations)
    coords = reversed_locations[0] # Latitude, Longitude for Nyeri, Kenya

    # Create the map centered around Nyeri
    map = folium.Map(location=coords, zoom_start=7)

    for location in reversed_locations:
        folium.Marker(
            location=location,
            popup=f"Location: {location}",
            icon=folium.Icon(color="blue")
        ).add_to(map)

    # Highlight the road (line) connecting the two towns
    road = folium.PolyLine(route_coords, color='red', weight=5, opacity=0.8)
    map.add_child(road)    

    # Output path for the map
    output_path = os.path.join(os.getcwd(), "map.html")

    # Save the map to an HTML file
    map.save(output_path)
    print(f"Map saved to: {output_path}")

    # For environments like Jupyter Notebooks, you can display the map
    # In other environments, you'd need to open the saved file manually
    map

else:
    print("No routes found.")