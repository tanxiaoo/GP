# Geospatial Processing Course Project Repository

This repository contains the project for the **Geospatial Processing** course held in 2024 at Polimi.

The project objective is to design and implement a Python-based library for geospatial data analysis and processing. The library will include functionalities for working with vector, raster, or datacube data types, enabling specific geospatial tasks. This repository includes the code, documentation, and testing materials needed to publish a complete and functional geospatial library on GitHub.

## Project Name: Buildable Area Analysis library

#### Project Overview
This project leverages Python to analyze multispectral imagery (Sentinel-2) and DEM data to identify areas suitable for construction. Identifying buildable areas supports regional planning and provides effective guidance for infrastructure implementation and construction projects. The analysis results are presented via interactive maps and output files, offering an intuitive way to view the findings. This project is suitable for both professional users and non-professional users through simplified operation modes.

---

### User Guide

#### If you want to conduct a professional analysis:
1. **Open the file:**
   - Use Jupyter Lab or upload the file to Google Drive, then open `building_area.ipynb` with Google Colab.

2. **Prepare data:**
   - Ensure the multispectral imagery (B3, B4, B8, etc.), DEM files, and ROI region files are downloaded and placed in an appropriate directory (recommended: create a `data` folder in the current directory).
   - Recommended data sources:
     - Multispectral imagery: [Copernicus Open Access Hub](https://browser.dataspace.copernicus.eu/)
     - DEM data: [USGS Earth Explorer](https://earthexplorer.usgs.gov/)
     - ROI region: Custom-defined or generated from GIS tools.

3. **Run the analysis:**
   - In the `Data Import and Parameter Settings` code section:
     - Modify input and output file paths.
     - Adjust analysis parameters (e.g., region of interest size) as needed.
   - Execute all code cells sequentially.

4. **View the results:**
   - View the interactive map in the dashboard.
   - Or navigate to the `output/` folder to check the generated result files (`building_area.geojson`).

---

#### If you just want to quickly view buildable areas:
1. **Register with Google Earth Engine:**
   - Sign up for [Google Earth Engine](https://earthengine.google.com/) and create a project.

2. **Open the file:**
   - Open `building_area_quickview.ipynb` using Jupyter Lab or Google Colab.

3. **Run the analysis:**
   - In the initial code section:
     - Replace the GEE ID with your project ID.
     - Set the output path.
     - Adjust analysis parameters (e.g., region of interest size) as needed.
   - Follow the prompts to select the region of interest on the map.
   - Run all code cells sequentially.

4. **View the results:**
   - Interactively view the analysis results on the map.
   - Or navigate to the `output/` folder to check the generated result files (`building_area.geojson`).

---

### Project Directory Structure

GP_Project/  
├── `building_area.ipynb`           # Main analysis file for users with prepared data  
├── `data_processing.py`            # Core data preprocessing script  
├── `building_area_quickview.ipynb` # Simplified operation file, no data preparation required  
│  
├── `test_data/`                    # Test data (multispectral imagery, DEM, ROI, etc.)  
├── `output/`                       # Folder for output results  

---

###  Main Analysis File Workflow `building_area.ipynb`

**STEP 1: Data Import and Parameter Settings**
- **File path settings:** Includes paths for multispectral imagery (B3, B4, B8, etc.), DEM files, and ROI region files.
- **Parameter settings:**
  - NDVI (Normalized Difference Vegetation Index) threshold: 0.3
  - NDWI (Normalized Difference Water Index) threshold: 0.1
  - Elevation range: 0-2500 meters
  - Maximum slope: 15°
  - Minimum buildable area: 10,000 square meters
- **Output path definition:** Specifies the location to save result files.

**STEP 2: Data Processing**
- **Reprojection:** Standardize the projection and coordinate system of the data.
- **Clipping:** Clip imagery and DEM data based on the ROI to reduce processing scope.
- **Resampling:** Adjust resolution to meet analysis requirements.
- **Raster alignment:** Ensure all input data are perfectly aligned on the raster grid.

**STEP 3: Data Analysis**
- **NDVI Calculation:** Generate a vegetation index layer using B4 and B8 bands, filtering out non-vegetation areas.
- **NDWI Calculation:** Generate a water index layer using B3 and B8 bands, excluding water bodies.
- **Elevation Analysis:** Use DEM data to filter areas that meet elevation thresholds.
- **Slope Analysis:** Calculate slope layers and exclude areas with excessive slopes.

**STEP 4: Buildable Area Selection**
- **Mask generation:** Combine NDVI, NDWI, elevation, and slope analysis results to create a buildable area mask.
- **Vectorization:** Convert the filtered raster data to vector format.
- **Save files:** Output vector files (GeoJSON or Shapefile) and raster files (GeoTIFF).

**STEP 5: Results Display and Interaction**
- **Map layer preparation:** Integrate analysis results and load them into map layers.
- **Interactive map display:** Use tools like Folium to display buildable areas with user interaction support.

---

### Project Limitations
1. **Limited factors considered:** The project only considers elevation, slope, water bodies, and vegetation, neglecting other potential factors such as soil type, land use, and socioeconomic factors.
2. **Dependency on thresholds:** The analysis relies on manually set thresholds (e.g., slope, NDVI, NDWI), which may affect the results.
3. **Data quality and timeliness:** Satellite imagery and DEM data may have resolution differences or missing data and might not always be up-to-date.
4. **Complex terrain challenges:** Complex terrains (e.g., canyons, mountains) may not be accurately represented, and elevation data might face occlusion issues.
5. **Dynamic changes:** Due to the time-sensitive nature of satellite data, the analysis might not reflect the latest land changes, especially in rapidly developing areas.
