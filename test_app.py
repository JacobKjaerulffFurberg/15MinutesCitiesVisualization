import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import streamlit.components.v1 as components

st.set_page_config(
    page_title="15 Minutes City - Copenhagen",
    page_icon="🗺️",
    layout="wide",
    menu_items={
        'About':"Here we can put our info and contact information etc."
    }
)

st.header('15 Minute City - Copenhagen')

@st.cache(allow_output_mutation=True)
def load_data():
    data = pd.read_csv("cph_pop_and_access_100m.csv")
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.success("Done! (using st.cache)")


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

#st.subheader('Map')
#column = "population_density"
#filtered_data = data[data[column]]
#st.map(data)


st.subheader('Select Amenities')

#user selection
#streamlit multiselect widget
container = st.container()
choices = data.columns[4:]
#user_choice = st.multiselect('Select your ammenities:', choices, defaul =)

all_options = st.checkbox("Select all", value=True)

if all_options:
    user_choice = container.multiselect("Select one or more options:",
         list(choices),list(choices))
else:
    user_choice = container.multiselect("Select one or more options:",
        list(choices))

#if all_options:
#    user_choice = list(choices)
#st.write("You selected:", user_choice)

data["avg_user_selection"] = data[user_choice].mean(axis=1)

#user_selected_amenities = ["avg_restaurant_dist", "avg_bar_dist", "avg_toilets_dist"]
#data["avg_user_selection"] = (data[user_selected_amenities[0]] + data[user_selected_amenities[1]] + data[user_selected_amenities[2]])/len(user_choice)

#st.subheader('Plotly')
px.set_mapbox_access_token(open(".mapbox_token").read())
fig = px.scatter_mapbox(
        data, 
        lon="lon", lat="lat", 
        hover_data=["population_density"] + user_choice,
        size="population_density",
        color="avg_user_selection",
        color_continuous_scale="Viridis_r", #viridis reversed
        mapbox_style="outdoors",
        width=2000,
        height=1000
    )


st.plotly_chart(fig)

HtmlFile = open("javascript_test.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height=800)