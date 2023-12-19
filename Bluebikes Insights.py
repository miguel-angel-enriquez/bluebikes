"""
Name:       Miguel Angel Enriquez Licea
CS230:      Section 5
Data:       Boston Blue Bikes
URL:        https://gist.github.com/miguel-angel-enriquez/01483e96419feb706cabca92f837b28a

Description: This program provides insightful queries and charts about the Bluebikes stations in the Boston area.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk
from PIL import Image

st.set_option('deprecation.showPyplotGlobalUse', False)

# Read in data
def read_data():
    path = "C:/Users/migue/OneDrive - Bentley University/Classes/FL 2023/CS 230 - Intro to Programming with Python/Final Project/"
    df = pd.read_csv(path + "current_bluebikes_stations.csv").set_index("Number")
    df = df.dropna() #Clear data
    return df


# Filter data

def filter_data(sel_districts, max_docks, min_years):
    df = read_data()
    df = df.loc[df['District'].isin(sel_districts)]
    df = df.loc[df['Total docks'] < max_docks]
    df = df.loc[df['Deployment Year'] > min_years]

    return df

# Count the frequency of Districts

def all_districts():
    df = read_data()
    lst = []
    for ind, row in df.iterrows():
        if row['District'] not in lst:
            lst.append(row['District'])

    return lst


def count_districts(districts, df):
    return [df.loc[df['District'].isin([district])].shape[0] for district in districts]


def district_docks(df):
    docks = [row['Total docks'] for ind, row in df.iterrows()]
    districts = [row['District'] for ind, row in df.iterrows()]

    dict = {}
    for district in districts:
        dict[district] = []

    for i in range(len(docks)):
        dict[districts[i]].append(docks[i])

    return dict


def district_averages(dict_docks):
    dict = {}
    for key in dict_docks.keys():
        dict[key] = np.mean(dict_docks[key])

    return (dict)

# Pie Chart
def generate_pie_chart(counts, sel_districts):
    plt.figure()

    explodes = [0 for i in range(len(counts))]
    maximum = counts.index(np.max(counts))
    explodes[maximum] = 0.20

    plt.pie(counts, labels=sel_districts, explode=explodes, autopct="%.2f%%")
    plt.title(f"Distribution of Docks per District: {', '.join(sel_districts)}")
    return plt

# Bar Chart
def generate_bar_chart(dict_averages):
    plt.figure()

    x = dict_averages.keys()
    y = dict_averages.values()
    plt.bar(x, y)
    plt.xticks(rotation=45)
    plt.ylabel("Number of Docks")
    plt.xlabel("Districts")
    plt.title(f"Average Number of Docks per District: {', '.join(dict_averages.keys())}")

    return plt

# Map
def generate_map(df):
    map_df = df.filter(['Name', 'Latitude', 'Longitude'])

    view_state = pdk.ViewState(latitude=map_df['Latitude'].mean(),
                               longitude=map_df['Longitude'].mean(),
                               zoom=12)
    layer = pdk.Layer('ScatterplotLayer',
                      data=map_df,
                      get_position='[Longitude, Latitude]',
                      get_radius=100,
                      get_color= [100, 150, 200], #[red,green,blue]
                      pickable=True)

    tool_tip = {'html': 'Name of station:<br><b>{Name}</b>', 'style': {'backgroundColor': 'steelblue', 'color': 'white'}}

    map = pdk.Deck(map_style='mapbox://styles/mapbox/outdoors-v11',
                   initial_view_state=view_state,
                   layers=[layer],
                   tooltip=tool_tip)

    st.pydeck_chart(map)

# Main Function
def main():
    st.title('Welcome to Bluebikes Insights')

    st_image = Image.open(
        "C:/Users/migue/OneDrive - Bentley University/Classes/FL 2023/CS 230 - Intro to Programming with Python/Final Project/Bluebikes_IMG.jpg")
    st.image(st_image, width=500, caption="Bluebikes")

    st.write("Welcome to Bluebikes Insights, your comprehensive analysis hub for Boston's renowned shared bike system. "
             "Dive into a wealth of information as we dissect the intricate details of Bluebikes stations, "
             "providing a data-driven exploration of their names, locations, installation years, and more. "
             "Our website is designed to empower users with valuable insights through queries and charts, "
             "allowing you to unravel patterns, trends, and key statistics related to the city's bike-sharing infrastructure. "
             "Whether you're a researcher, an urban planner, or simply curious about the evolution of Boston's transportation landscape, "
             "Bluebikes Insights is your gateway to understanding the dynamic and ever-growing network of bike stations that define the city's sustainable mobility initiatives. "
             "Explore, analyze, and uncover the fascinating story behind Boston's Bluebikes system right here.")

    st.divider()
    st.header('Want to know more?')
    st.write('Visit the "History" page to learn more about Bluebikes!')

    st.divider()
    st.header("Let's get started!")
    st.write('This website contains queries and charts that will help you gain insights about the Bluebikes system. '
             'To start exploring, find the options on the sidebar and make your selections.')

    st.divider()
    st.write('In case you are curious, below is the raw data of all the stations in the Boston area and beyond.')
    st.write(read_data())

    st.sidebar.write("Please select your options to visualize the data.")
    districts = st.sidebar.multiselect("Select a district: ", all_districts())
    max_docks = st.sidebar.slider("Maximum Number of Docks: ", 0, 53)
    min_years = st.sidebar.slider("Minimum Year of Deployment: ", 2011, 2013)

    data = filter_data(districts, max_docks, min_years)
    series = count_districts(districts,data)

    if len(districts) > 0 and max_docks >= 0 and min_years > 0:
        st.header("Explore the stations on the map")
        generate_map(data)
        st.divider()

        st.header("Visualize the data in a pie chart")
        st.pyplot(generate_pie_chart(series, districts))
        st.divider()

        st.header("Visualize the data in a bar chart")
        st.pyplot(generate_bar_chart(district_averages(district_docks(data))))

main()