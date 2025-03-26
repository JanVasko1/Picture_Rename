import os
import logging
import windows_metadata
from pandas import DataFrame
from datetime import datetime
import lat_lon_parser
import json

from PIL import Image

import Libs.Data_Functions as Data_Functions
from customtkinter import CTkProgressBar, CTk

logging.basicConfig(level=logging.ERROR)

# -------------------------------------------------------------------------------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def convert_to_degrees(value: tuple) -> float:
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)

def Format_DateTime_All(Original_Date_Time_str: str, DateTime_Format: str) -> datetime:
    Original_Date_Time_dt = datetime.strptime(Original_Date_Time_str, DateTime_Format)
    return Original_Date_Time_dt

def Get_Picture_Main_Att(Settings: dict, file_path: str, Actual_Folder: str, filename: str, Log_file) -> list|bool:
    Exif_ID = Settings["MetaData"]["Exif_ID"]
    GPS_ID = Settings["MetaData"]["GPS_ID"]
    Date_Taken_ID = Settings["MetaData"]["Date_Taken_ID"]

    try:
        # Open the image file
        image = Image.open(file_path)
        exif1 = image.getexif()
        GPS_Coordinate = exif1.get_ifd(tag=GPS_ID)
        Date_Taken = exif1.get_ifd(tag=Exif_ID)[Date_Taken_ID]
        image.close()

        # Convert latitude and longitude to degrees
        Latitude = lat_lon_parser.to_dec_deg(d=GPS_Coordinate[2][0], m=GPS_Coordinate[2][1], s=GPS_Coordinate[2][2])
        Longitude = lat_lon_parser.to_dec_deg(d=GPS_Coordinate[4][0], m=GPS_Coordinate[4][1], s=GPS_Coordinate[4][2])

        # Latitude Update -> to be on below Ecuador
        if GPS_Coordinate[1] == "N":
            pass
        elif GPS_Coordinate[1] == "S":
            Latitude *= -1

        # Longitude Update -> to be on Wester Hemisphere
        if GPS_Coordinate[3] == "W":
            Longitude *= -1
        elif GPS_Coordinate[3] == "E":
            pass

        # Format the GPS coordinates -> list
        geo_coordinate = [Latitude, Longitude]
        return geo_coordinate, Date_Taken

    except Exception as error:
        Log_file.write(f"""Property Error;{Actual_Folder};{filename};{error}\n""")
        return False

def Get_Video_GEO(file_path, Actual_Folder, filename) -> list|bool:
    # TODO --> Finish
    return True

def Get_DateTime_properties(file_path, attribute, Actual_Folder, filename, Log_file):
    try:
        attributes = windows_metadata.windows_metadata.WindowsAttributes(file_path)
        return attributes[attribute]
    except Exception as error:
        Log_file.write(f"""Property Error;{Actual_Folder};{filename};Missing {attribute} in file.\n""")
        return False

def Add_to_Dataframe(GEO_df: DataFrame, GEO_attributes: list, Date: datetime, Album: str, Album2: str, Name: str) -> None:
    GEO_df.loc[len(GEO_df.index)] = [Date, GEO_attributes[0], GEO_attributes[1], str(Album), str(Album2), str(Name)] 

def Create_geojson(GEO_df: DataFrame, Export_File_Name: str) -> None:
    geojson = {"type": "FeatureCollection", "features": []}

    for _, row in GEO_df.iterrows():
        feature = {
            "type": "Feature", 
            "geometry": {
                "type": "Point", 
                "coordinates": [
                    row["Longitude"], 
                    row["Latitude"]
                ]
                }, 
            "properties": {
                "Album": row["Album"],
                "Album2": row["Album2"],
                "Name": row["Name"],
                "Date": str(row["Date"])
            }
        }
        geojson["features"].append(feature)

    with open(Data_Functions.Absolute_path(relative_path=f"Exports\\{Export_File_Name}.geojson"), "w") as fp:
        json.dump(geojson, fp)   

def Progress_Bar_step(window: CTk, Progress_Bar: CTkProgressBar) -> None:
    Progress_Bar.step()
    window.update_idletasks()

def Progress_Bar_set(window: CTk, Progress_Bar: CTkProgressBar, value: int) -> None:
    Progress_Bar.set(value=value)
    window.update_idletasks()

# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def GEO_Json(Settings: dict, Nested_Path: list, window: CTk, Progress_Bar: CTkProgressBar, Export_File_Name: str) -> None:
    GEO_df = DataFrame(columns=["Date", "Latitude", "Longitude", "Album" ,"Album2", "Name"])
    PIL_DateTime_Format = Settings["GEOJson"]["PIL_DateTime_Format"]
    Supported_photo_formats = Settings["General"]["Supported_postfix"]["Photos"]
    Supported_video_formats = Settings["General"]["Supported_postfix"]["Videos"]

    # Create Log file
    Log_file = open(Data_Functions.Absolute_path(relative_path=f"Libs\\Logs\\GEO_JSON_Log.csv"), "w", encoding="UTF-8")
    Log_file.write(f"Type;Folder;File;Error\n")
    Log_file.close()
    Log_file = open(Data_Functions.Absolute_path(relative_path=f"Libs\\Logs\\GEO_JSON_Log.csv"), "a", encoding="UTF-8")
    
    # Get Date for each file
    for actual_path in Nested_Path:
        Actual_Folder_list = actual_path.split("\\")
        Actual_Folder = Actual_Folder_list[-1]
        Higher_Actual_Folder = Actual_Folder_list[-2]

        for filename in os.listdir(actual_path):
            Name_split = os.path.splitext(filename)
            postfix = Name_split[1]
            file_path = os.path.join(actual_path, filename)

            if postfix == "":
                continue

            elif postfix in Supported_photo_formats:
                try:
                    GEO_Attributes, Date_Taken = Get_Picture_Main_Att(file_path=file_path, Actual_Folder=Actual_Folder, filename=filename, Log_file=Log_file)
                    if GEO_Attributes != False:
                        Formatted_Date_Time =  Format_DateTime_All(Original_Date_Time_str=Date_Taken, DateTime_Format=PIL_DateTime_Format)
                        Add_to_Dataframe(GEO_df=GEO_df, GEO_attributes=GEO_Attributes, Date=Formatted_Date_Time, Album=Higher_Actual_Folder, Album2=Actual_Folder, Name=filename)
                    Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)

                except Exception as error:
                    Log_file.write(f"""Picture;{Actual_Folder};{filename};{error}\n""")
                    Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
                    continue

            elif postfix in Supported_video_formats:
                try:
                    GEO_Attributes = Get_Video_GEO(file_path=file_path, Actual_Folder=Actual_Folder, filename=filename)
                    if GEO_Attributes != False:
                        DateTime_Attributes = Get_DateTime_properties(file_path=file_path, attribute="Media created", Actual_Folder=Actual_Folder, filename=filename, Log_file=Log_file)
                        Formatted_Date_Time =  Format_DateTime_All(Original_Date_Time_str=DateTime_Attributes, DateTime_Format=PIL_DateTime_Format)
                        Add_to_Dataframe(GEO_df=GEO_df, GEO_attributes=GEO_Attributes, Date=Formatted_Date_Time, Album=Higher_Actual_Folder, Album2=Actual_Folder, Name=filename)

                    Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)

                except:
                    Log_file.write(f"""Video;{Actual_Folder};{filename};{error}\n""")
                    Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
                    continue

            else:
                Log_file.write(f"""Postfix;{Actual_Folder};{filename};Not supported file type\n""")
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
                continue

    # Create GEOJson file
    Create_geojson(GEO_df=GEO_df, Export_File_Name=Export_File_Name)

    Log_file.close()
    Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, value=1) 