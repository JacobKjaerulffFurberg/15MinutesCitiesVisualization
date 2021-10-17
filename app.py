# # Run this app with `python app.py` and
# # visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pandana, time, os, pandas as pd, numpy as np
from pandana.loaders import osm
import plotly

app = dash.Dash(__name__)
server = app.server



# configure search at a max distance of 1 km for up to the 10 nearest points-of-interest
amenities = ['restaurant', 'bar', 'school', 'toilets', 'college', 'hospital']#, 'hospital']
distance = 1000
num_pois = 10
num_categories = len(amenities) + 1 #one for each amenity, plus one extra for all of them combined
holder = "naah"

# bounding box as a list of llcrnrlat, llcrnrlng, urcrnrlat, urcrnrlng
bbox = [55.6036813, 12.5202081, 55.6942218, 12.6150132]#[55.5036813, 12.4202081, 55.7442218, 12.6750132]
#[55.6036813, 12.5202081, 55.6942218, 12.6150132]

#[55.6636813, 12.5202081, 55.6942218, 12.5550132] #[55.6336813, 12.5402081, 55.6742218, 12.5950132]  #lat-long bounding box for berkeley/oakland

#[55.6036813, 12.5202081, 55.6942218, 12.6150132]#
#(53.2987342,-6.3870259,53.4105416,-6.1148829)
#[12.5795, 55.6775, 12.6081, 55.6688]

#bbox = [1.7752, 36.7799, 1.7889,36.7988 ]


#[y:37.76, x: -122.35, y:37.9, x:-122.17]


#[12.5842713, 55.6723028, 55.6741331,12.5985204]
#55.6723028,12.5842713

#55.6741331,12.5985204


# configure filenames to save/load POI and network datasets
bbox_string = '_'.join([str(x) for x in bbox])
net_filename = 'data/network_{}.h5'.format(bbox_string)
poi_filename = 'data/pois_{}_{}.csv'.format('_'.join(amenities), bbox_string)


start_time = time.time()
if os.path.isfile(poi_filename):
    # if a points-of-interest file already exists, just load the dataset from that
    pois = pd.read_csv(poi_filename)
    method = 'loaded from CSV'
else:   
    # otherwise, query the OSM API for the specified amenities within the bounding box 
    osm_tags = '"amenity"~"{}"'.format('|'.join(amenities))
    pois = osm.node_query(lat_min=bbox[0],lng_min=bbox[1], lat_max=bbox[2], lng_max=bbox[3], tags=osm_tags)
    
    # using the '"amenity"~"school"' returns preschools etc, so drop any that aren't just 'school' then save to CSV
    pois = pois[pois['amenity'].isin(amenities)]
    pois.to_csv(poi_filename, index=False, encoding='utf-8')
    method = 'downloaded from OSM'
    
print('{:,} POIs {} in {:,.2f} seconds'.format(len(pois), method, time.time()-start_time))
pois[['amenity', 'name', 'lat', 'lon']].head()


start_time = time.time()
if os.path.isfile(net_filename):
    # if a street network file already exists, just load the dataset from that
    network = pandana.network.Network.from_hdf5(net_filename)
    method = 'loaded from HDF5' 
else:
    #otherwise, query the OSM API for the street network within the specified bounding box
    network = osm.pdna_network_from_bbox(lat_min=bbox[0],lng_min=bbox[1], lat_max=bbox[2], lng_max=bbox[3])
    method = 'downloaded from OSM'

    # identify nodes that are connected to fewer than some threshold of other nodes within a given distance
    lcn = network.low_connectivity_nodes(impedance=1000, count=10, imp_name='distance')
    network.save_hdf5(net_filename, rm_nodes=lcn) #remove low-connectivity nodes and save to h5

print('Network with {:,} nodes {} in {:,.2f} secs'.format(len(network.node_ids), method, time.time()-start_time))
network.precompute(distance + 1)
# initialize the underlying C++ points-of-interest engine
network.init_pois(num_categories=num_categories, max_dist=distance, max_pois=num_pois)
# initialize a category for all amenities with the locations specified by the lon and lat columns
network.set_pois(category='all', x_col=pois['lon'], y_col=pois['lat'])
# initialize each amenity category with the locations specified by the lon and lat columns
for amenity in amenities:
    pois_subset = pois[pois['amenity']==amenity]
    network.set_pois(category=amenity, x_col=pois_subset['lon'], y_col=pois_subset['lat'])


temp_df = network.nodes_df

for ame in amenities:
    temp_df[f'{ame}_distance'] = network.nearest_pois(distance=distance, category=f'{ame}', num_pois=num_pois)[1]

# restaurant_access = network.nearest_pois(distance=distance, category='restaurant', num_pois=num_pois)
# school_access = network.nearest_pois(distance=distance, category='school', num_pois=num_pois)
# bar_access = network.nearest_pois(distance=distance, category='bar', num_pois=num_pois)


# temp_df["school_distance"] = school_access[1]
# temp_df["restaurant_distance"] = restaurant_access[1]
# temp_df["bar_distance"] = bar_access[1]

temp_df

import plotly.figure_factory as ff
import plotly.express as px
from dash.dependencies import Input, Output

px.set_mapbox_access_token(open(".mapbox_token").read())

amenity = "restaurant"

# @app.callback(Output('live-update-graph', 'figure'),
#               Input('interval-component', 'n_intervals'))
# def update_graph_live(a):
#     print("updating...")
#     #amenity = amenities[a % len(amenities)]
#     fig = ff.create_hexbin_mapbox(
#         data_frame=temp_df, lat="y", lon="x",
#         nx_hexagon=40, opacity=0.5, labels={f'{amenity}_distance': "school_distance"},
#         min_count=1, agg_func=np.mean, 
#         color=f'{amenity}_distance',  color_continuous_scale='viridis_r'
#     )

#     #fig.update_layout(mapbox_style="outdoors")
#     fig.update_layout(
#         autosize=False,
#         width=1400,
#         height=800,
#         mapbox_style="outdoors",
#         )

#     #print(fig)
#     return fig
#fig.data[0].hovertemplate = f'Point Count =%{z:,.1f}<extra>Average distance to a {amenity}</extra>'
#fig.show()

class Settings:
    custom_style = True


print("showing figure")
settings = Settings()
mapstyle = "mapbox://styles/anjulia/ck6212zuo0n7k1irz2cvd377i"


#import plotly.express as px
# px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])

figure = px.scatter_mapbox(data_frame=pd.DataFrame({'x': [12], 'y': [54]}), lat="y", lon="x",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

# ff.create_hexbin_mapbox(
#     data_frame=temp_df, lat="y", lon="x",
#     nx_hexagon=40, opacity=0.5, labels={f'{amenity}_distance': "school_distance"},
#     min_count=1, agg_func=np.mean, 
#     color=f'{amenity}_distance',  
#     color_continuous_scale='viridis_r',
# )


app.layout = html.Div(children=[
    html.H1(children='15 Minute Cities'),

    html.Div(children='''
        Interactive map of city accessibility
    '''),
    # html.Div(dcc.Input(id='input-on-submit', type='text')),
    # html.Button('Submit', id='submit-val', n_clicks=0),
    # html.Div(id='container-button-basic',
    #          children='Enter a value and press submit'),
    dcc.Dropdown(
        id='demo-dropdown',
        options= [{'label': amenity, 'value': amenity} for amenity in amenities],
        value=amenity[0]
    ),
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Div(id='container-button-basic'),
    html.Button('Submit', id='submit-val', n_clicks=0),
    dcc.Graph(id='live-update-graph'),
    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # )

    html.Div(id='dd-output-container')
    # dcc.Interval(
    #         id='interval-component',
    #         interval=1*10000, # in milliseconds
    #         n_intervals=0
    #     )
])

@app.callback(
dash.dependencies.Output('container-button-basic', 'children'),
[dash.dependencies.Input('submit-val', 'n_clicks')],
[dash.dependencies.State('input-on-submit', 'value')])
def update_out2(n_clicks, value):
    settings.custom_style = not settings.custom_style
    
    

@app.callback(
    Output('live-update-graph', 'figure'),
    Input('demo-dropdown', 'value'))
def update_output(value):
    print(value)
    print(amenities)
    for index, item in enumerate(amenities):
        if item == value:
            break
    else:
        index = -1
    
    mapstyle = "mapbox://styles/anjulia/ck6212zuo0n7k1irz2cvd377i"
    


    amenity = amenities[index]
    # figure = ff.create_hexbin_mapbox(
    #     data_frame=temp_df, lat="y", lon="x",
    #     nx_hexagon=40, opacity=0.5, labels={f'{amenity}_distance': "school_distance"},
    #     min_count=1, agg_func=np.mean, 
    #     color=f'{amenity}_distance',  
    #     color_continuous_scale='viridis_r',
    # )

    figure.update_mapboxes(
        bearing=0,
        pitch=45,
        style=mapstyle,
    )

    #figure.update(data_frame=temp_df) 

    # figure.bearing = 17.6
    # figure.pitch = 45
    

    # fig.update_layout(mapbox_style="outdoors")
    figure.update_layout(
        autosize=False,
        width=1400,
        height=800,
        mapbox_style= "mapbox://styles/goodgame/cku5oss0q0mv819nsp5hjydsx" #if settings.custom_style else "outdoors" #"stamen-watercolor",
    #     mapbox_layers=[
    #     {
    #         "sourcetype": "raster",
    #         "sourceattribution": "Government of Canada",
    #         "source": ["https://geo.weather.gc.ca/geomet/?"
    #                    "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX={bbox-epsg-3857}&CRS=EPSG:3857"
    #                    "&WIDTH=1000&HEIGHT=1000&LAYERS=RADAR_1KM_RDBR&TILED=true&FORMAT=image/png"],
    #     },
    #   ]
        )

    #print(fig)
    return figure
    

if __name__ == '__main__':
    app.run_server(debug=True)

