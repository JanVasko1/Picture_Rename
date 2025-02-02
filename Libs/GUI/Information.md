# Photo Rename / change metadata
These tiny programs were developed because of media library handling. To make it easier and to update data in batches (even for whole media library).

# Setup
### <span style="color:blue;">Installation</span>
1. Install [Python 3.11.2](https://www.python.org/downloads/release/python-3112/) - recommended or higher
    - install it as "Run as Administrator"
    - on pop-up page mark "Add Python 3.8 to PATH" and un-mark "Instal launcher for all users" (if possible)
2. Run `Installation_libs.ps1` code (reflect correct path to your python installation)
3. Update:
    1. `Photo_Rename_Files.bat` to reflect correct path to your python installation
    2. `Photo_Change_metadata.bat` to reflect correct path to your python installation
    3. `Photo_Generate_GEO_json.bat` to reflect correct path to your python installation

### <span style="color:blue;">Process</span></span>
![Process](Libs\\Readme\\Whole_process.png)

- red --> manual steps
- green --> automatic steps

# <span style="color:blue;">Photo Rename</span>
This program was build to harmonize media names into one format `YYYYMMDD_hhmmss`, because of Windows sorting and Photo gallery app sorting.
- Also works with `Nested Folders`
- list of allowed postfix is in [`Defaults.py`](https://github.com/JanVasko1/Picture_Rename/blob/main/Libs/Defaults.py)

> [!TIP]
> ![Media Rename](Libs\\Readme\\Photo_rename.png)

- red --> manual steps
- green --> automatic steps

# <span style="color:blue;">Photo Meta Data Change</span>
This program was build to update media MetaData `Date Taken`(Photos) and `Media Create`(Video) from filename in format `YYYYMMDD_hhmmss`, because of Windows sorting and Photo gallery app sorting.
- Also works with `Nested Folders`
- list of allowed postfix is in [`Defaults.py`](https://github.com/JanVasko1/Picture_Rename/blob/main/Libs/Defaults.py)

> [!TIP]
> ![Media Dates Change](Libs\\Readme\\Photo_MetaData_Change.png)
- red --> manual steps
- green --> automatic steps

> [!CAUTION]
> Video file types --> Under Development

# <span style="color:blue;">Photo Create GEOJSON</span>
This program was build to create .geojson from media files (Photos and Videos) 
- Also works with `Nested Folders`

> [!TIP]
> ![GEOJSON creation process](Libs\\Readme\\Photo_Geojson.png)

- red --> manual steps
- green --> automatic steps

> [!CAUTION]
> Video file types --> Under Development

![Kepler example](Libs\\Readme\\MyTimeLine.gif)
