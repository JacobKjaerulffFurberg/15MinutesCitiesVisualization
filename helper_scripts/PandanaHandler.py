import pandana, time, os, pandas as pd, numpy as np
from pandana.loaders import osm
import pandas as pd
import time


def getAccessibilityMeasures(bbox = None, amenities = None, distance = None, num_pois = None):
    # configure search at a max distance of 1 km for up to the 10 nearest points-of-interest
    if not amenities:
        amenities = ['restaurant', 'bar', 'school', 'toilets', 'college', 'hospital']#, 'hospital']
    if not distance:
        distance = 1000
    if not num_pois:
        num_pois = 10
    num_categories = len(amenities) + 1 #one for each amenity, plus one extra for all of them combined

    # bounding box as a list of llcrnrlat, llcrnrlng, urcrnrlat, urcrnrlng
    if not bbox: 
        bbox = [55.6036813, 12.5202081, 55.6942218, 12.6150132]

    print(bbox)
    # configure filenames to save/load POI and network datasets
    bbox_string = '_'.join([str(x) for x in bbox])
    net_filename = '../data/network_{}.h5'.format(bbox_string)
    poi_filename = '../data/pois_{}_{}.csv'.format('_'.join(amenities), bbox_string)
    
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
        if len(pois[pois['amenity']==amenity].index) == 0:
            continue
        pois_subset = pois[pois['amenity']==amenity]
        network.set_pois(category=amenity, x_col=pois_subset['lon'], y_col=pois_subset['lat'])


    temp_df = network.nodes_df

    for ame in amenities:
        if len(pois[pois['amenity']==ame].index) == 0:
            continue
        temp_df[f'{ame}_distance'] = network.nearest_pois(distance=distance, category=f'{ame}', num_pois=num_pois)[1]
        
    return temp_df

