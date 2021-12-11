import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

st.set_page_config(
    page_title="15 Minutes City - Copenhagen",
    page_icon="🗺️",
    layout="wide",
    menu_items={
        'About':"Research project for visualizing accessibility measures for cities. Created with Python3 using Pandana (Foti & Waddell, 2012) and data from OSM (© OpenStreetMap contributors). \n Authors: Anne Havmøller Fellows-Jensen, Sumin Lee & Jacob Kjærulff Furberg"
    },
    initial_sidebar_state="expanded"
)

@st.cache(allow_output_mutation=True)
def load_data():
    data = pd.read_csv("cph_pop_and_access_100m.csv")
    return data


st.title('🗺️ 15 Minute City - Copenhagen')
col1, col2 = st.columns([3,1])

with col1:
    description1 = '<p style="color:black; font-size: 20px;">This webpage is developed as part of a research project at the IT University of Copenhagen. The project attempts to address the problem of how to simultaneously visualize population density and accessibility measures of a city. This webpage works as a prototype and consists of an interactive map which allows you to explore the amenities and the density in various areas of the city of Copenhagen. The map is developed utilising the Pandana (source) and Mapbox (source) frameworks, and builds upon data on amenities from OpenStreetMap (source) and population data from WorldPop (source).</p>'
    st.markdown(description1, unsafe_allow_html = True)
    description2 = '<p style="color:black; font-size: 20px;">The interactive map is divided into areas of a size 100m X 100m. For each area the average distance to the selected amenities in relation to the number of people is visualised as a color combination. The color represents the relation between the density and average distance and can be interpreted utilising the matrix to the right.</p>'
    st.markdown(description2, unsafe_allow_html = True)
    st.subheader('Instructions')
    instruction = '<p style="color:black; font-size: 20px;">To interact with the map of Copenhagen see the input options in the sidebar. By default the map will showcase the average distance to all amenities in relation to the size of the population. Initially the longest distance and the highest population count in the dataset are considered as the farthest distance and highest density on the map. This can be toglled by the sliders to your left. The number of amenities disblayed can be changed utilising the multiselect box. </p>'
    st.markdown(instruction, unsafe_allow_html = True)

# Create a text element and let the reader know the data is loading.
#data_load_state = st.text('Loading data...')
# Load csv data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
#data_load_state.success("Done! (using st.cache)")


#if st.checkbox('Show raw data'):
#    st.subheader('Raw data')
#    st.write(data)

#st.subheader('Map')
#column = "population_density"
#filtered_data = data[data[column]]
#st.map(data)


st.sidebar.header("Inputs")
st.sidebar.write("Filter what is shown on the map based on your input below.")

st.sidebar.subheader('Select Amenities')
st.sidebar.write("Below you can select the amenities you wish to see the average distances for.")

#user selection
#streamlit multiselect widget
data.rename({'avg_restaurant_dist': 'Restaurants', 'avg_bar_dist': 'Bars', 'avg_school_dist': 'Schools', 'avg_toilets_dist': 'Toilets', 'avg_college_dist': 'Colleges', 'avg_hospital_dist': 'Hospitals'}, axis=1, inplace=True)


container = st.sidebar.container()
choices = data.columns[5:11]
#user_choice = st.multiselect('Select your ammenities:', choices, defaul =)

all_options = st.sidebar.checkbox("Select all", value=True)

if all_options:
    user_choice = container.multiselect("Select one or more options:",
         list(choices),list(choices))
else:
    user_choice = container.multiselect("Select one or more options:",
        list(choices))

#if all_options:
#    user_choice = list(choices)
#st.write("You selected:", user_choice)

st.sidebar.subheader('Select Max Values')
st.sidebar.write("Below you can select what is categorised as high distance and high density. The colourmap will be updated accordingly.")

data["avg_user_selection"] = data[user_choice].mean(axis=1)

max_dist = st.sidebar.slider("Pick a max distance",0, 5000, value = 5000)

data["max_dist"] = data["avg_user_selection"].mask(data["avg_user_selection"]>max_dist, max_dist)

max_pop = st.sidebar.slider("Pick a max density",0, int(data["population_density"].max()), value = int(data["population_density"].max()))

data["max_pop"] = data["population_density"].mask(data["population_density"]>max_pop, max_pop)

#user_selected_amenities = ["avg_restaurant_dist", "avg_bar_dist", "avg_toilets_dist"]
#data["avg_user_selection"] = (data[user_selected_amenities[0]] + data[user_selected_amenities[1]] + data[user_selected_amenities[2]])/len(user_choice)


#PCA color
sample = data[["population_density", "avg_user_selection", "max_dist", "max_pop"]]

# Scale(normalize) the data attributes between 0-1

from sklearn import preprocessing
import pandas as pd
scaler = preprocessing.MinMaxScaler()
names = sample.columns
d = scaler.fit_transform(sample)
scaled_df = pd.DataFrame(d, columns=names)

# Adding scaled data rows in the original data frame 

data['scaled_acc'] = abs(scaled_df['avg_user_selection']-1)
data['scaled_pop'] = scaled_df['population_density']
data['scaled_max_acc'] = abs(scaled_df['max_dist']-1)
data['scaled_max_pop'] = scaled_df['max_pop']

pca_df = data[['scaled_max_pop', 'scaled_max_acc']]

eig_vals, eig_vecs = np.linalg.eig(np.cov(pca_df.T))

# Choosing bigger Eigen value
def chooseEigenVal(eig_vals):
    if eig_vals[0] >= eig_vals[1]:
        return 0
    else:
        return 1

projected_X = pca_df.dot(eig_vecs.T[chooseEigenVal(eig_vals)])

data['PCA'] = projected_X
data['modifiedPCA'] = projected_X + 1
data['y_axis'] = 0.0


#st.subheader('Plotly')

with col2:
    legend = px.scatter(data, x='scaled_pop', y='scaled_acc', color='PCA', width=400, height=400, title='Color Scheme')
    legend.update_layout(
        font = dict(
            size=18
        ),
        autosize=True,
        xaxis=dict(
            title_text="Population Density",
            #visible=False,
            ticktext = ['low', 'medium', 'high'],
            tickvals = [0, 0.5, 1],
            titlefont=dict(size=20)
        ),
        yaxis=dict(
            title_text="Accessibility",
            #visible=False,
            ticktext = ['far', ' ', ' ', ' ', ' ', 'close'],
            tickvals = [0, 0.2, 0.4, 0.6, 0.8, 1],
            titlefont=dict(size=20),
        )
    )

    legend.update(layout_coloraxis_showscale=False)
    legend.update_layout(
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        paper_bgcolor="LightGrey",
    )
    st.plotly_chart(legend)


px.set_mapbox_access_token(open(".mapbox_token").read())
fig = px.scatter_mapbox(
        data, 
        lon="lon", lat="lat", 
        hover_data=["population_density"] + user_choice + ["avg_user_selection"],
        size="population_density",
        color="PCA",
        #color_continuous_scale="Viridis_r", #viridis reversed
        mapbox_style="outdoors",
        width=1500,
        height=800
    )
fig.update(layout_coloraxis_showscale=False)
st.plotly_chart(fig)

st.header("15 Minute Cities")
context = '<p style="color:black; font-size: 20px;">The continuous rise in urbanisation has made cities’ ability to be inclusive and sustainable a global focus (Moreno et al., 2021; Graells-Garrido et al., 2021). Carlos Moreno introduced the concept of The 15-minute City to describe the idea of an urban city where inhabitants have immediate access to essential services (Moreno et al., 2021). Rather than humans adapting to the urban space, he argues that urban spaces should be designed (or re-designed) to adapt to human needs (Moreno et al., 2021). The 15-minute initiative and others like it are an attempt to rethink our way of structuring cities to best accommodate as many citizens as possible, and to minimise transportation pollution. However, a redesign of our cities requires an understanding of the current arrangement. How is accessibility measures currently distributed?</p>'
st.markdown(context, unsafe_allow_html = True)


HtmlFile = open("javascript_test.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height=800)