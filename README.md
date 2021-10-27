# 15MinutesCitiesVisualization
Research project for visualizing accessibility measures for cities.


## Tools
Created with Python3 using Pandana and data from OSM.


## Authors
Anne Havmøller Fellows-Jensen, Sumin Lee & Jacob Kjærulff Furberg

### Supervisor
Maria Sinziiana Astefanoaei



## How to use the project to generate data

Follow the steps below to use this project:

### Step 1: Download .TIF images from WorldPop

Go to https://www.worldpop.org/methods/populations to browse different population density datasets. The lower the resolution the longer the scripts will take to run.

This link https://www.worldpop.org/geodata/listing?id=78 is useful for downloading .TIF images for different countries at an approx 100m*100m resolution.

#### explanation of .TIF format

.TIFF images is a picture that contains pixel with a single value associated with each pixel. In the case of WorldPop, each pixel holds a value which is the calculated population density of that area. 

### Step 2: open the project as a jupyter lab
Do the following steps
1. download the github project, we suggest you run `git clone <LINK_TO_THIS_GITHUB_REPO>`
2. open a cmd prompt/terminal and navigate to the folder
3. run: `jupyter lab`

Now you can see all the different scripts files.

### Step 3: Generate a .geojson from the .TIF image file

1. When you are in the project folder, then navigate to `notebooks/Generate_GeoJson_With_Points_From_TIFF.ipynb` 
2. Update the filename to match the name of your .tif file and move your .tif file to the `tif_images/` folder found in the main directory.
3. Starting from the first cell, run all the cells to generate a .geojson from the .tif image.
4. After all cells have ran you will be able to find the generated .geojson file in the folder `geojson_files/`, found in the main directory.

### Step 4: Generate a .geojson file of polygons from the points .geojson file

1. When you are in the project folder, then navigate to `notebooks/ConvertGeoPointsToGeoPolygons.ipynb`.
2. Change the filename to match your .geojson file containing the points.
3. Run all the cells.
4. Now you have generated a .geojson file with polygons instead of points.

### Step 5: 

1. When you are in the project folder, then navigate to `notebooks/GetAccessibilityDataAndJoinWithGrid.ipynb`.
2. Change the filename to match your .geojson file with polygons.
3. Run all the cells.
4. Your final result file can be seen in the folder `csv_files/`.