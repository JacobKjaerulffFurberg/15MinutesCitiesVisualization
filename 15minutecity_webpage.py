import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn import preprocessing

def main():
    st.set_page_config(
    page_title="15 Minute City",
    page_icon="🗺️",
    layout="wide",
    menu_items={
        'About':"Research project for visualizing accessibility measures for cities. Created with Python3 using Pandana (Foti & Waddell, 2012) and data from OSM (© OpenStreetMap contributors). \n Authors: Anne Havmøller Fellows-Jensen, Sumin Lee & Jacob Kjærulff Furberg"
    },
    initial_sidebar_state="expanded"
    )
    st.title("Research Project - The IT University of Copenhagen Autumn 2021")

    page = st.selectbox("", ["Front Page", "Map of Copenhagen", "Map of Denmark"])
    select_page(page)

# Create a page dropdown
def select_page(page):
    if page == "Front Page":
        front_page()
    elif page == "Map of Copenhagen":
        map_of_copenhagen()
    elif page == "Map of Denmark":
        map_of_denmark()

# Create content of pages

# Build front page
def front_page():
    st.header('🗺️ The 15 Minute City')
    context = '<p style="color:black; font-size: 20px;">The continuous rise in urbanisation has made cities’ ability to be inclusive and sustainable a global focus (Moreno et al., 2021; Graells-Garrido et al., 2021). Carlos Moreno introduced the concept of The 15-minute City to describe the idea of an urban city where inhabitants have immediate access to essential services (Moreno et al., 2021). Rather than humans adapting to the urban space, he argues that urban spaces should be designed (or re-designed) to adapt to human needs (Moreno et al., 2021). The 15-minute initiative and others like it are an attempt to rethink our way of structuring cities to best accommodate as many citizens as possible, and to minimise transportation pollution. However, a redesign of our cities requires an understanding of the current arrangement. How is accessibility measures currently distributed?</p>'
    st.markdown(context, unsafe_allow_html = True)
    introduction = '<p style="color:black; font-size: 20px;">This webpage is developed as part of a research project at the IT University of Copenhagen. The project attempts to address the problem of how to simultaneously visualize population density and accessibility measures of a city. The webpage works as a prototype and consists of two interactive maps. One of Copenhagen and one of the entirety of Denmark. Both allow you to explore areas and their distance to various amenities and population density. The maps are developed utilising the Pandana (source) and Mapbox (source) frameworks, and build upon data on amenities from OpenStreetMap (source) and population data from WorldPop (source).</p>'
    st.markdown(introduction, unsafe_allow_html = True)
    

    st.image("cph_with_bivariate_map_color.png", caption="Accessibility Measures and Population Density Plottet on a Map of Copenhagen")

# Build map of Denmark page
def map_of_denmark():
    # Display details of page 2
    st.header('Map of Denmark')

    description_dk = '<p style="color:black; font-size: 20px;">This page presents an interactive map of the relation between various amenities and population density in Denmark. The interactive map is divided into areas of a size 100m X 100m. For each area the relation between the avarage distance to amenities and the population density is showcased, either through a combination of colour and form (height) or solely as a color combination</p>'
    st.markdown(description_dk, unsafe_allow_html = True)
    instruction_header_dk = '<p style="color:black; font-size: 22px;">Instructions</p>'
    st.markdown(instruction_header_dk, unsafe_allow_html = True)
    instruction_dk = '<p style="color:black; font-size: 20px;">To interact with the map of Denmark see the input options in the left hand corner of the map. You can select which amenities you wish to see represented on the map and by using the \'Search distance\' slider you can set what distance should be considered as far. Initially the average distance to amenities is represented on the map as the color of an area and the density as the height. By clickling the button \'Swap color mode\', you can represent the relation between distance to amenities and population density as a color combination. The top right hand corner of the \'Color grid\' represents areas with high density but high distance and the left hand corner represents a low density and low distance.</p>'
    st.markdown(instruction_dk, unsafe_allow_html = True)


    HtmlFile = open("javascript_test.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height=800)

# Build map of Copenhagen page
def map_of_copenhagen():
    # Display details of page 1
    st.header('Map of Copenhagen')
    @st.cache(allow_output_mutation=True)
    def load_data():
        data = pd.read_csv("cph_pop_and_access_100m.csv")
        return data

    col1, col2 = st.columns([3,1])

    with col1:
        description_cph = '<p style="color:black; font-size: 20px;">This page presents an interactive map of the relation between various amenities and population density in Copenhagen.</p>'
        st.markdown(description_cph, unsafe_allow_html = True)
        description_cph2 = '<p style="color:black; font-size: 20px;">The interactive map is divided into areas of a size 100m X 100m (each dot representing the centrum of an area). For each area the average distance to the selected amenities in relation to the number of people is visualised as a color combination. The color represents the relation between the density and average distance and can be interpreted utilising the matrix to the right.</p>'
        st.markdown(description_cph2, unsafe_allow_html = True)
        instruction_header_cph = '<p style="color:black; font-size: 22px;">Instructions</p>'
        st.markdown(instruction_header_cph, unsafe_allow_html = True)
        instruction_cph = '<p style="color:black; font-size: 20px;">To interact with the map of Copenhagen see the input options in the sidebar. By default the map will showcase the average distance to all amenities in relation to the size of the population. Initially the longest distance and the highest population count in the dataset are considered as the farthest distance and highest density on the map. This can be toglled by the sliders to your left. The number of amenities disblayed can be changed utilising the multiselect box. </p>'
        st.markdown(instruction_cph, unsafe_allow_html = True)

        # Create a text element and let the reader know the data is loading.
        #data_load_state = st.text('Loading data...')
        # Load csv data into the dataframe.
        data = load_data()
        # Notify the reader that the data was successfully loaded.
        #data_load_state.success("Done! (using st.cache)")

        # Create sidebar for interacting with the map data
        st.sidebar.header("Inputs")
        st.sidebar.write("Filter what is shown on the map based on your input below.")

        st.sidebar.subheader('Select Amenities')
        st.sidebar.write("Below you can select the amenities you wish to see the average distances for.")

        #user selection
        #streamlit multiselect widget
        data.rename({'avg_restaurant_dist': 'Restaurants', 'avg_bar_dist': 'Bars', 'avg_school_dist': 'Schools', 'avg_toilets_dist': 'Toilets', 'avg_college_dist': 'Colleges', 'avg_hospital_dist': 'Hospitals'}, axis=1, inplace=True)


        container = st.sidebar.container()
        choices = data.columns[5:11]


        all_options = st.sidebar.checkbox("Select all", value=True)

        if all_options:
            user_choice = container.multiselect("Select one or more options:",
                list(choices),list(choices))
        else:
            user_choice = container.multiselect("Select one or more options:",
                list(choices))

        st.sidebar.subheader('Select Max Values')
        st.sidebar.write("Below you can select what is categorised as high distance and high density. The colourmap will be updated accordingly.")

        data["avg_user_selection"] = data[user_choice].mean(axis=1)

        max_dist = st.sidebar.slider("Pick a max distance",0, 5000, value = 5000)

        data["max_dist"] = data["avg_user_selection"].mask(data["avg_user_selection"]>max_dist, max_dist)

        max_pop = st.sidebar.slider("Pick a max density",0, int(data["population_density"].max()), value = int(data["population_density"].max()))

        data["max_pop"] = data["population_density"].mask(data["population_density"]>max_pop, max_pop)


        #PCA color
        sample = data[["max_dist", "max_pop"]]
        
        # Scale(normalize) the data attributes between 0-1
        scaler = preprocessing.MinMaxScaler()
        names = sample.columns
        d = scaler.fit_transform(sample)
        scaled_df = pd.DataFrame(d, columns=names)

        scaled_df['max_dist'] = abs(scaled_df['max_dist']-1)

        scaled_df.loc[len(scaled_df.index)] = [1, 1] 
        scaled_df.loc[len(scaled_df.index)] = [0, 1] 
        scaled_df.loc[len(scaled_df.index)] = [1, 0] 
        scaled_df.loc[len(scaled_df.index)] = [0, 0] 

        scaled_df.rename(columns = {'max_pop':'scaled_pop', 'max_dist':'scaled_acc'}, inplace = True)

        eig_vals, eig_vecs = np.linalg.eig(np.cov(scaled_df.T))

        def chooseEigenVal(eig_vals):
            return 0 if eig_vals[0] >= eig_vals[1] else 1

        projected_X = scaled_df.dot(eig_vecs.T[chooseEigenVal(eig_vals)])
        scaled_df['PCA'] = projected_X


        data = pd.concat([data, scaled_df], axis=1) 

        data = data.fillna(0)
        data.iloc[-4:, data.columns.get_loc('lon')] = 12.611250
        data.iloc[-4:, data.columns.get_loc('lat')] = 55.60375




        
    # Create map of Copenhagen
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
            #size="population_density",
            color="PCA",
            mapbox_style="outdoors",
            width=1800,
            height=1100
        )
    fig.update(layout_coloraxis_showscale=False)
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
