# Photo Rename / change metadata
This program was developed to make TimeSheet administration easier and harmonize it over all fo Konica Minolta employee.

# Setup
### <span style="color:blue;">Installation</span>
1. Install [Python 3.11.2](https://www.python.org/downloads/release/python-3112/) - recomended or higher
2. Run `Installation_libs.ps1` code (reflect correct path to your python installation)
3. Update:
    1. `Photo_Rename_Files.bat` to reflect correct path to your python installation
    2. `Photo_Chage_metadata.bat` to reflect correct path to your python installation
    3. `Photo_Generate_GEO_json.bat` to reflect correct path to your python installation

### <span style="color:blue;">Process</span></span>
![Process](https://github.com/JanVasko1/Picture_Rename/blob/main/Libs/Icons/Whole_process.png?raw=true
 "Overal process")

- red --> manual steps
- green --> automatic steps

# <span style="color:blue;">Photo Rename</span>
This program was build to harmonize media names into one format `YYYYMMDD_hhmmss`, because of Windows sorting and Photo galerry app sorting.
- Also works with `Nested Folders`
- list of allowed postfix is in [`Defaults.py`](https://github.com/JanVasko1/Picture_Rename/blob/main/Libs/Defaults.py)

> [!TIP]
> ![Media Rename](https://github.com/JanVasko1/Picture_Rename/blob/main/Libs/Icons/Photo_rename.png?raw=true
 "Media Rename")

- red --> manual steps
- green --> automatic steps

# <span style="color:blue;">Photo Meta Data Change</span>
This program was build to update media MetaData `Date Taken`(Photos) and `Media Create`(Video) from filename in format `YYYYMMDD_hhmmss`, because of Windows sorting and Photo galerry app sorting.
- Also works with `Nested Folders`
- list of allowed postfix is in [`Defaults.py`](https://github.com/JanVasko1/Picture_Rename/blob/main/Libs/Defaults.py)

> [!TIP]
> ![Media Dates Change](https://github.com/JanVasko1/Picture_Rename/blob/main/Libs/Icons/Photo_MetaData_Change.png?raw=true
 "Media Dates Change")

- red --> manual steps
- green --> automatic steps

> [!CAUTION]
> Video file types --> Under Developemnt

# <span style="color:blue;">Photo Create GEOJSON</span>
This program was build to create .geojson from media files (Photos and Videos) 
- Also works with `Nested Folders`

> [!TIP]
> ![GEOJSON creation process](https://github.com/JanVasko1/Picture_Rename/blob/main/Libs/Icons/Photo_Geojson.png?raw=true
 "GEOJSON creation process")

- red --> manual steps
- green --> automatic steps

> [!CAUTION]
> Video file types --> Under Developemnt

> [!TIP]
> ![Kepler example](https://github.com/JanVasko1/Picture_Rename/blob/main/Libs/Exports/Kepler_example.html
 "Kepler example")

<video autoplay loop style="width:50%; height: auto; position:absolute; z-index: -1;">
  <source src="http://syddev.com/jquery.videoBG/assets/tunnel_animation.mp4" type="video/mp4" />
  <img src="http://syddev.com/jquery.videoBG/assets/tunnel_animation.jpg">
</video>