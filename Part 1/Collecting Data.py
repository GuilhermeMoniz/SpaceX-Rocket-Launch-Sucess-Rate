# Import Libraries
import pandas as pd
import numpy as np
import requests
import datetime

# Takes the dataset and uses the rocket column to call the API and append the data to the list
def getBoosterVersion(data):
    for x in data['rocket']:
        response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
        BoosterVersion.append(response['name'])


# Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(data):
    for x in data['launchpad']:
        response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
        Longitude.append(response['longitude'])
        Latitude.append(response['latitude'])
        LaunchSite.append(response['name'])


# Takes the dataset and uses the payloads column to call the API and append the data to the lists
def getPayloadData(data):
    for load in data['payloads']:
        response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])


# Takes the dataset and uses the cores column to call the API and append the data to the lists
def getCoreData(data):
    for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])



spacex_url = "https://api.spacexdata.com/v4/launches/past"

response = requests.get(spacex_url)
#print(response.content)

""""""

### TASK 1 - Request and parse the SpaceX launch data using the GET request

static_json_url = 'C://Users/guimo/datasets/API_call_spacex_api.json'
#print(response.status_code)

# Decode the response content as Json and turn it into a Pandas Dataframe
data = pd.json_normalize(response.json())

# Using the dataframe data print the first 5 rows
#print(data.head())

# A lot of data are IDs (ex. rocket column has no information about the rocket, just ID number)
# Use the API again to get information about the launches using the IDs given for each launch

# Take a subset of our dataframe keeping only the features we want and the flight number, and date_utc
data = data[["rocket", "payloads", "launchpad", "cores", "flight_number", "date_utc"]]

# Remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters
# Remove rows with multiple payloads in a single rocket
data = data[data["cores"].map(len) == 1]
data = data[data["payloads"].map(len) == 1]

# Since payloads and cores are lists of size 1, extract the single value in the list and replace the feature
data["cores"] = data["cores"].map(lambda x : x[0])
data["payloads"] = data["payloads"].map(lambda x : x[0])

# Convert teh data_utc to a datetime datatype and then extracting the date leaving the time
data["date"] = pd.to_datetime(data["date_utc"]).dt.date

# Using the date we will restrict the dates of the launches
data = data[data["date"] <= datetime.date(2020, 11, 13)]


# Data from the requests will be stored in lists and will be used to create a new dataframe
#Global variables 
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

# Look at the BoosterVersion variable
#print(BoosterVersion)

# Apply getBoosterVersion function method to get the booster version
getBoosterVersion(data)

# List is now updated
#print(BoosterVersion.head())

# Apply the rest of the functions:
getLaunchSite(data)
getPayloadData(data)
getCoreData(data)

# Construct the dataset using the data we obtained
# Combine the columns into a dictionary
launch_dict = {'FlightNumber': list(data['flight_number']),
'Date': list(data['date']),
'BoosterVersion':BoosterVersion,
'PayloadMass':PayloadMass,
'Orbit':Orbit,
'LaunchSite':LaunchSite,
'Outcome':Outcome,
'Flights':Flights,
'GridFins':GridFins,
'Reused':Reused,
'Legs':Legs,
'LandingPad':LandingPad,
'Block':Block,
'ReusedCount':ReusedCount,
'Serial':Serial,
'Longitude': Longitude,
'Latitude': Latitude}

# Create a dataframe from the dictionary launch_dict
df = pd.DataFrame.from_dict(launch_dict)

# SHow the summmary of the dataframe
#print(df.head())

""""""

### TASK 2 - Filter the dataframe to only include Falcon 9 launches

# Remove falcon 1 launches keeping only the falcon 9 launches
# Filter the dataframe using boosterversion column
# Save the filtered data to a new dataframe called data_falcon9
data_falcon9 = df[df["BoosterVersion"] != "Falcon 1"]

# Now that its removed, reset the flight number column
data_falcon9.loc[:, "FlightNumber"] = list(range(1, data_falcon9.shape[0] + 1))
#print(data_falcon9)

""""""

### DATA WRANGLING

# Some rows are missing values in our dataset
data_falcon9.isnull().sum()

""""""

### TASK 3 - Dealing with Missing Values

# 1. Calculate the mean for the PayloadMass
# 2. Use the mean and replace the nan values in the data with the mean calculated

# 1.
payloadmassavg = data_falcon9["PayloadMass"].mean()

# 2.
data_falcon9["PayloadMass"].replace(np.NaN, payloadmassavg, inplace = True)


# Now that the missing values are dealt with we can now export this into a CSV
data_falcon9.to_csv("dataset_part1.csv", index = False)