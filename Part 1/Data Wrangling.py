# Import libraries
import pandas as pd
import numpy as np

""""""

### DATA ANALYSIS
df = pd.read_csv("C://Users/guimo/datasets/dataset_part_1.csv")
print(df.head())

# Identify and calculate the percentage of the missing values in each attribute
df.isnull().sum() / len(df) * 100

# Identify which columns are numerical and categorical
df.dtypes

""""""

### TASK 1 - Calculate the number of launches on each site
# Use value_counts() on the column LaunchSite to determine the number of launches on each site
df["LaunchSite"].value_counts()

""""""

### TASK 2 - Calculate the number and occurrence of each orbit
# Use value_counts() to determine the number and occurrence of each orbit
df["Orbit"].value_counts()

""""""

### TASK 3 - Calculate the number and occurrence of mission outcome per orbit type
# Use value_counts() on the column Outcome to determine the number of landing_outcomes
# Assign it to a variable called landing_outcomes
landing_outcomes = df["Outcome"].value_counts()

"""
Important information:

    - True Ocean means the mission outcome was successfully landed to a specific region of the ocean while False Ocean means the mission outcome was unsuccessfully landed to a specific region of the ocean
    - True RTLS means the mission outcome was successfully landed to a ground pad False RTLS means the mission outcome was unsuccessfully landed to a ground pad
    - True ASDS means the mission outcome was successfully landed to a drone ship False ASDS means the mission outcome was unsuccessfully landed to a drone ship

    - None ASDS and None None these represent a failure to land
"""

for i, outcome in enumerate(landing_outcomes.keys()):
    print(i, outcome)

# Create a set of outcomes where the second stage did not land successfully
bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])

""""""

### TASK 4 - Create a landing outcome label from Outcome column
# Using the Outcome, create a list where the element is zero if the corresponding row in Outcome is in the set bad_outcome; otherwise, it's one. 
# Then assign it to the variable landing_class

# landing_class = 0 if bad_outcome
# landing_class = 0 otherwise
landing_class = []

for outcome in df["Outcome"]:
    if outcome in bad_outcomes:
        landing_class.append(0)
    else:
        landing_class.append(1)
        
# This variable will represent the classification variable that represents the outcome of each launch. If the value is zero, the first stage did not land successfully; one means the first stage landed Successfully
df['Class'] = landing_class
#print(df.head())

# We can use the following line of code to determine the success rate
df["Class"].mean()

""""""

### TASK 5 - Export into a CSV file
df.to_csv("dataset_part_2.csv", index = False)
