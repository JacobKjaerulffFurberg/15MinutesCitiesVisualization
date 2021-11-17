search_dist = 5000 # in meters
amenities = ['restaurant', 'bar', 'school', 'toilets', 'college', 'hospital']
num_pois = 10


bbox_min_lon = 12.3080 
bbox_max_lon = 12.7096
bbox_min_lat = 55.5416
bbox_max_lat = 55.7761
search_bbox = [bbox_min_lon, bbox_min_lat, bbox_max_lon, bbox_max_lat]

settings = {"bbox": search_bbox, "num_pois": num_pois, "amenities": amenities, "search_dist": search_dist}
