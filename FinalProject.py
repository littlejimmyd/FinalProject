"""
Name:       James Haddad
CS230:      Section SN5
Data:       skyscrapers.csv
URL:        Link to your web application online (see extra credit)

Description:

This programs utilizes streamlit and its functions to create a user interface to analyze skyscraper data from the
skyscraper.csv file. The first major element of my project is a filtered dataset and map based upon a max height (in
feet) slider. The second major part of my project displays a bar chart which displays the height of the skyscrapers,
of a certain country, based upon the sidebar selection). The next chart is another bar chart which displays the count of
skyscrappers from each country. Both the colors of these charts can be changed by the user on the sidebar. The final
major element of my project involves a sidebar multiselect which displays the dataset for skyscrapers within the selected
countries, as well as a stastical analysis from the selections (including: the number of skyscrapers, the average year
built, the average height, the max height, and the minimum height).

"""

from pandas import DataFrame, read_csv
import os
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import matplotlib
import dateutil
import pydeck as pdk

#Reading in CSV File
def read_file(datafile= "skyscrapers.csv"):
    df= pd.read_csv(datafile)
    df["Feet"]=df["Feet"].str.replace(',','')
    df["Feet"]=df["Feet"].astype(float)
    return df

#Bar Chart 1 Function
def bar_chart1(selectedcountrydata, country, color):
    plt.figure()
    plt.title(f"Heights of Skyscrapers in {country}")
    plt.ylabel("Height (In Feet)",fontsize=16,fontweight="bold")
    plt.xlabel("Skyscraper Name",fontsize=16,fontweight="bold")
    plt.xticks(rotation='vertical')
    plt.bar(selectedcountrydata["Name"],selectedcountrydata["Feet"],color=color, edgecolor="black")
    return plt

#Bar Chart 2 Function
def bar_chart2(fd, color2):
    plt.figure()
    plt.title(f"Number of Skyscrappers (Per Country)")
    plt.ylabel("Number of Skyscrappers",fontsize=16,fontweight="bold")
    plt.xlabel("Country Name",fontsize=16,fontweight="bold")
    plt.xticks(rotation='vertical')
    plt.bar(fd["Country"],fd["Counts"],color=color2, edgecolor="black")
    return plt

#Frequency Function for Countries
def freq_data(df, countries):
    freq_dict = {}
    for country in countries:
        freq=0
        for i in range(len(df)):
            if df[i][5] == country:
                freq+=1
        freq_dict[country] = freq
    return freq_dict

def main():
    #Page Formatting
    st.header("Welcome to A World Skyscrapers Analysis!")
    st.sidebar.header("World Skyscrapers Filters")
    df= read_file()

    # Max Height Slider (For Map)
    feet = df["Feet"]
    print(feet)
    min_slider = int(df['Feet'].min())
    max_slider = int(df['Feet'].max())
    maxheight= st.sidebar.slider("Slide for Max Height of Skyscraper",min_value=min_slider,max_value=max_slider)

    #Map Cration
    df_filtered = df[df['Feet'] <= maxheight]
    st.write("Data Set Based Upon Max Height Filter:")
    st.write(df_filtered)
    df_filtered["lon"]=df_filtered["Lon"]
    df_filtered["lat"]=df_filtered["Lat"]
    map_data= df_filtered[["lon","lat"]]
    st.map(map_data)

    #Country Selection Drop Down Box (For Bar Chart)
    countries = df['Country'].unique()
    country = st.sidebar.selectbox('Country (For Bar Charts)', countries)
    selectedcountrydata= df[df['Country'] == country]
    color= st.sidebar.color_picker('Pick A Color (For Bar Charts)', '#7AD8D8')
    st.sidebar.write('The current selected color is',color)
    st.pyplot(bar_chart1(selectedcountrydata=selectedcountrydata,country=country, color=color))
    st.set_option('deprecation.showPyplotGlobalUse', False)

    #Country Selection (For Statistics)
    countries2 = df['Country'].unique()
    country2 = st.sidebar.multiselect('Countries Selection (For Statistics)', countries2)
    fd = df['Country'].value_counts().rename_axis("Country").reset_index(name="Counts")
    print(fd)
    selectedcountrydata2= df['Country'].isin(country2)
    selectedcountrydata2=df[selectedcountrydata2]
    selectedcountrydata2_count= selectedcountrydata2["Country"].count()

    #Bar Chart2 Creation
    st.pyplot(bar_chart2(fd=fd,color2=color))

    #Selected Countries Statistics
    st.write("Statistics/Data for Selected Countries:")
    st.write(selectedcountrydata2)
    st.write("Number of Skyscrapers in Selected Countries:",selectedcountrydata2_count)
    yearmean= selectedcountrydata2["Year"].mean()
    st.write("Average Year Built: ",yearmean)
    heightmean= selectedcountrydata2["Feet"].mean()
    heightmax= selectedcountrydata2["Feet"].max()
    heightmin=selectedcountrydata2["Feet"].min()
    st.write("Average Height (Feet): ",heightmean)
    st.write("Max Height (Feet): ",heightmax)
    st.write("Minimum Height (Feet): ",heightmin)

main()

