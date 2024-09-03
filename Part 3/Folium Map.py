# Import Libraries
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon

""""""

### TASK 1 - Mark all launch sites on a map
url = 'C://Users/guimo/datasets/spacex_launch_geo.csv'
spacex_df = pd.read_csv(url)
print(spacex_df.head())

""""""

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]

launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()

launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]

""""""

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]

site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

""""""

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))

# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,

    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )

site_map.add_child(circle)
site_map.add_child(marker)

""""""

# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label
vafb_coordinates = [34.750144,-120.521294]
ksc_coordinates = [28.573255,-80.646895]
ccafs_coordinates = [28.562302,-80.577356]
ccafs_slc_coordinates = [28.563197,-80.576820]

vafb_circle = folium.Circle(vafb_coordinates, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('Vandenberg Space Force Base'))
vafb_marker = folium.map.Marker(vafb_coordinates, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0),html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'VAFB SLE 4E'))
site_map.add_child(vafb_circle)
site_map.add_child(vafb_marker)

ksc_circle = folium.Circle(ksc_coordinates, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('Kennedy Space Center'))
ksc_marker = folium.map.Marker(ksc_coordinates, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0),html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'KSC LC-39A'))
site_map.add_child(ksc_circle)
site_map.add_child(ksc_marker)

ccafs_circle = folium.Circle(ccafs_coordinates, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('Cape Canaveral LC'))
ccafs_marker = folium.map.Marker(ccafs_coordinates, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0),html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'CCAFS LC-40'))
site_map.add_child(ccafs_circle)
site_map.add_child(ccafs_marker)

ccafs_slc_circle = folium.Circle(ccafs_slc_coordinates, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('Cape Canaveral SLC'))
ccafs_slc_marker = folium.map.Marker(ccafs_slc_coordinates, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0),html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'CCAFS SLC-40'))
site_map.add_child(ccafs_slc_circle)
site_map.add_child(ccafs_slc_marker)

""""""

### TASK 2 - Mark the success/failed launches for each site on the map

# Create a MarkerCluster object
marker_cluster = MarkerCluster()

# Create a new column in spacex_df dataframe called marker_color to store the marker colors based on the class value
# Apply a function to check the value of `class` column

# If class=1, marker_color value will be green
# If class=0, marker_color value will be red

# Function to assign color to launch outcome
def assign_marker_color(launch_outcome):
    if launch_outcome == 1:
        return 'green'
    else:
        return 'red'
    
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)
spacex_df.tail(10)

""""""

# For each launch result in spacex_df data frame, add a folium.Marker to marker_cluster
# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)

# for each row in spacex_df data frame
# create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed, 
# e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']
for index, record in spacex_df.iterrows():
    marker = folium.Marker([record['Lat'], record['Long']], 
                  icon=folium.Icon(color='white', icon_color=record['marker_color']))
    marker_cluster.add_child(marker)

site_map

""""""

### TASK 3 - Calculate the distances between a launch site to its proximities

# Add a MousePosition on the map to get coordinate for a mouse over a point on the map
# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)
site_map

# Zoom in to a launch site and explore its proximity to see if you can easily find any railway, highway, coastline, etc
# Move your mouse to these points and mark down their coordinates (shown on the top-left) in order to the distance to the launch site
from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

""""""

# Mark down a point on the closest coastline using MousePosition and calculate the distance between the coastline point and the launch site

# find coordinate of the closet coastline
# e.g.,: Lat: 28.56367  Lon: -80.57163
# distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)

#Work out distance to coastline
coordinates = [
    [28.56342, -80.57674],
    [28.56342, -80.56756]]

lines=folium.PolyLine(locations=coordinates, weight=1)
site_map.add_child(lines)
distance = calculate_distance(coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1])
distance_circle = folium.Marker(
    [28.56342, -80.56794],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
        )
    )
site_map.add_child(distance_circle)
site_map

""""""

# Draw a PolyLine between a launch site to the selected coastline point
#Distance to Florida City 

coordinates = [
    [28.56342, -80.57674],
    [28.5383, -81.3792]]

lines=folium.PolyLine(locations=coordinates, weight=1)
site_map.add_child(lines)
distance = calculate_distance(coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1])
distance_circle = folium.Marker(
    [28.5383, -81.3792],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#252526;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
        )
    )
site_map.add_child(distance_circle)
site_map

""""""

# Create a marker with distance to a closest city, railway, highway, etc.
# Draw a line between the marker to the launch site

#Distance to Highway
coordinates = [
    [28.56342, -80.57674],
    [28.411780, -80.820630]]

lines=folium.PolyLine(locations=coordinates, weight=1)
site_map.add_child(lines)
distance = calculate_distance(coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1])
distance_circle = folium.Marker(
    [28.411780, -80.820630],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#252526;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
        )
    )
site_map.add_child(distance_circle)
site_map
