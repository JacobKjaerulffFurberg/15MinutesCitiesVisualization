import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import streamlit.components.v1 as components

st.title('15 Minutes City')

@st.cache
def load_data():
    data = pd.read_csv("cph_pop_and_access_1k.csv")
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Map')
#column = "population_density"
#filtered_data = data[data[column]]
st.map(data)




st.subheader('Plotly')

#user selection:
user_selected_amenities = ["avg_restaurant_dist", "avg_bar_dist", "avg_toilets_dist"]

# streamlit multiselect widget
px.set_mapbox_access_token(open(".mapbox_token").read())
fig = px.scatter_mapbox(
        data, 
        lon="lon", lat="lat", 
        hover_data=["population_density"] + user_selected_amenities,
        size="population_density",
        color="avg_bar_dist",
        color_continuous_scale="Viridis_r", #viridis reversed
        mapbox_style="outdoors",
    )


st.plotly_chart(fig)

HtmlFile = open("javascript_test.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height=800)