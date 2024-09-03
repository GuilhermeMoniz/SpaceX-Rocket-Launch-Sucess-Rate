# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 

# Read the spaceX dataset into pandas dataframe
url = "C://Users/guimo/datasets/dataset_part_2.csv"
df = pd.read_csv(url)

# Print its summary
df.head()

# Plot out the FlightNumber vs. PayloadMassand overlay the outcome of the launch
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)

plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)

#plt.show()

""""""

### TASK 1: Visualize the relationship between Flight Number and Launch Site

# 1. Use the function catplot to plot FlightNumber vs LaunchSite, set the parameter x parameter to FlightNumber,set the y to Launch Site and set the parameter hue to 'class' 
sns.catplot(y = "LaunchSite", x = "FlightNumber", hue = "Class",  data = df, aspect = 5)

plt.xlabel("Flight Number", fontsize = 20)
plt.ylabel("Launch Site", fontsize = 20)

#plt.show()

""""""

### TASK 2: Visualize the relationship between Payload Mass and Launch Site

# 1. Observe if there is any relationship between launch sites and their payload mass
sns.catplot(y = "LaunchSite", x = "PayloadMass", hue = "Class",  data = df, aspect = 5)

plt.xlabel("Payload Mass (kg)", fontsize = 20)
plt.ylabel("Launch Site", fontsize = 20)

#plt.show()

""""""

### TASK 3: Visualize the relationship between success rate of each orbit type

# 1. Next, we want to visually check if there are any relationship between success rate and orbit type
# 1.1. Let's create a bar chart for the sucess rate of each orbit
df.groupby("Orbit").mean()["Class"].plot(kind = "bar")

plt.xlabel("Orbit Type", fontsize = 20)
plt.ylabel("Success Rate", fontsize = 20)

#plt.show()

""""""

### TASK  4: Visualize the relationship between FlightNumber and Orbit type

# 1. For each orbit, we want to see if there is any relationship between FlightNumber and Orbit type
sns.catplot(y = "Orbit", x = "FlightNumber", hue = "Class", data = df, aspect = 5)

plt.xlabel("Flight Number", fontsize = 20)
plt.ylabel("Orbit", fontsize = 20)

#plt.show()

""""""

### TASK 5: Visualize the relationship between Payload Mass and Orbit type

# 1. Plot the Payload Mass vs. Orbit scatter point charts to reveal the relationship between Payload Mass and Orbit type
sns.catplot(y = "Orbit", x = "PayloadMass", hue = "Class", data = df, aspect = 5)

plt.xlabel("Payload", fontsize = 20)
plt.ylabel("Orbit", fontsize = 20)

#plt.show()

""""""

### TASK 6: Visualize the launch success yearly trend

## The function will help you get the year from the date
# A function to Extract years from the date 
year=[]

def Extract_year():

    for i in df["Date"]:
        year.append(i.split("-")[0])

    return year

Extract_year()
df['Date'] = year

# 1. You can plot a line chart with x axis to be Year and y axis to be average success rate, to get the average launch success trend
df1 = pd.DataFrame(Extract_year(df["Date"], columns = ["year"]))
df1["Class"] = df["Class"]

sns.catplot(y = df1.groupby("year")["Class"].mean(), x = np.unique(Extract_year(df["Date"])), hue = "Class", data = df1)

plt.xlabel("Year", fontsize = 20)
plt.ylabel("Success Rate", fontsize = 20)

plt.show()


""""""


### FEATURES ENGINEERING ###
# Select the features that will be used in success prediction in the future module
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()

""""""

### TASK 7: Create dummy variables to categorical columns

# 1. Use the function get_dummies and features dataframe to apply OneHotEncoder to the column Orbits, LaunchSite, LandingPad, and Serial. 
# 1.1. Assign the value to the variable features_one_hot, display the results using the method head
# 1.2.Include all features including the encoded ones
features_one_hot = pd.get_dummies(features, columns = ["Orbit", "LaunchSite", "LandingPad", "Serial"])
features_one_hot.head()

""""""

### TASK 8: Cast all numeric columns to float64

# 1. Now that our features_one_hot dataframe only contains numbers, cast the entire dataframe to variable type float64
features_one_hot.astype("float64")

""""""

### TASK 9: Export it into CSV file
features_one_hot.to_csv("dataset_part3.csv", index = False)
