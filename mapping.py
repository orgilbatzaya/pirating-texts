'''
Created on Jun 12, 2018

@author: orgil
'''
import folium, pandas, requests

url = 'http://maps.googleapis.com/maps/api/geocode/json'
d = {'address': 'Seattle', 'sensor':'false'}
r = requests.get(url, params = d)








'''folium_map = folium.Map(location=[40.738, -73.98],
                        zoom_start=13,
                        tiles="CartoDB dark_matter")
marker = folium.CircleMarker(location=[40.738, -73.98])
marker.add_to(folium_map)
folium_map.save("my_map.html")'''
