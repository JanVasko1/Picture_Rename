import os
import logging
import windows_metadata
from pandas import DataFrame
from datetime import datetime
from tqdm import tqdm
import Defaults
import lat_lon_parser
import json


from PIL import Image
from PIL.ExifTags import TAGS

logging.basicConfig(level=logging.ERROR)

def convert_to_degrees(value: tuple) -> float:
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)

def Format_DateTime_All(Original_Date_Time_str: str, DateTime_Format: str) -> datetime:
    Orifinal_Date_Time_dt = datetime.strptime(Original_Date_Time_str, DateTime_Format)
    return Orifinal_Date_Time_dt

def Get_Pictrue_Main_Att(file_path: str, Actual_Folder: str, filename: str) -> list|bool:
    try:
        # Open the image file
        image = Image.open(file_path)
        exif1 = image.getexif()
        GPS_Coordinance = exif1.get_ifd(tag=34853)
        Date_Taken = exif1.get_ifd(tag=34665)[36867]
        image.close()

        # Convert latitude and longitude to degrees
        Latitude = lat_lon_parser.to_dec_deg(d=GPS_Coordinance[2][0], m=GPS_Coordinance[2][1], s=GPS_Coordinance[2][2])
        Longitude = lat_lon_parser.to_dec_deg(d=GPS_Coordinance[4][0], m=GPS_Coordinance[4][1], s=GPS_Coordinance[4][2])

        # Latitude Update -> to be on below Equador
        if GPS_Coordinance[1] == "N":
            pass
        elif GPS_Coordinance[1] == "S":
            Latitude *= -1

        # Longitude Update -> to be on Wester Hemisphear
        if GPS_Coordinance[3] == "W":
            Longitude *= -1
        elif GPS_Coordinance[3] == "E":
            pass

        # Format the GPS coordinates -> list
        geo_coordinate = [Latitude, Longitude]
        return geo_coordinate, Date_Taken

    except Exception as error:
        Log_file.write(f"""Property Error;{Actual_Folder};{filename};{error}\n""")
        return False

def Get_Video_GEO(file_path, Actual_Folder, filename) -> list|bool:
    #! Dodělat 
    return False

def Get_DateTime_properties(file_path, atribute, Actual_Folder, filename):
    try:
        attributes = windows_metadata.windows_metadata.WindowsAttributes(file_path)
        return attributes[atribute]
    except Exception as error:
        Log_file.write(f"""Property Error;{Actual_Folder};{filename};Missing {atribute} in file.\n""")
        return False

def Add_to_Dataframe(GEO_df: DataFrame, GEO_attributes: list, Date: datetime, Album: str, Album2: str, Name: str) -> None:
    GEO_df.loc[len(GEO_df.index)] = [Date, GEO_attributes[0], GEO_attributes[1], str(Album), str(Album2), str(Name)] 

def Create_geojson(GEO_df: DataFrame) -> None:
    Export_File_Name = input("\nGive me file name: ")

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

    with open(f"Exports\\{Export_File_Name}.geojson", "w") as fp:
        json.dump(geojson, fp)   

# Defaults
GEO_df = DataFrame(columns=["Date", "Latitude", "Longitude", "Album" ,"Album2", "Name"])
PIL_DateTime_Format = "%Y:%m:%d %H:%M:%S"
Supported_photo_formats = Defaults.Supported_photo_formats()
Supported_video_formats = Defaults.Supported_video_formats()

print("""
#--------------------------------------------------------------#
# This program will take an metadata from pictures and viedeos # 
# from field "Date Taken" GPS Coordinance create .geojson file.#
# - program worsk also with nested folders                     #
# - folders name cannot contain dots .                         #
#--------------------------------------------------------------#""")

# List of files in folder
while True:
    Selected_path = input("Give me file path to pictures: ")
    Nested_Folder = input("Do you want also check nested Folders? [Y/N]")
    Nested_Folder = Nested_Folder.upper()

    # Create Path list 
    if Nested_Folder == "Y":
        # Read actual folder and folders inside
        Nested_Path = [x[0] for x in os.walk(Selected_path)]
        File_Count = sum([len(files) for r, d, files in os.walk(Selected_path)])
    else:
        Nested_Path = [Selected_path]
        File_Count = [len(files) for r, d, files in os.walk(Selected_path)]
        File_Count = File_Count[0]

    # Create Log file
    Log_file = open("Logs\\GEO_JSON_Log.csv", "w", encoding="UTF-8")
    Log_file.write(f"Type;Folder;File;Error\n")
    Log_file.close()
    Log_file = open("Logs\\GEO_JSON_Log.csv", "a", encoding="UTF-8")
    
    # Get Date for each file
    now = datetime.now()
    Data_df_TQDM = tqdm(total=int(File_Count),desc=f"{now}>> Getting GEO data from media.")
    for actual_path in Nested_Path:
        Actual_Folder_list = actual_path.split("\\")
        Actual_Folder = Actual_Folder_list[-1]
        Higher_Actual_Folder = Actual_Folder_list[-2]

        for filename in os.listdir(actual_path):
            Nanem_split = os.path.splitext(filename)
            postfix = Nanem_split[1]
            file_path = os.path.join(actual_path, filename)

            if postfix == "":
                continue

            elif postfix in Supported_photo_formats:
                try:
                    GEO_Attributes, Date_Taken = Get_Pictrue_Main_Att(file_path=file_path, Actual_Folder=Actual_Folder, filename=filename)
                    if GEO_Attributes != False:
                        Formated_Date_Time =  Format_DateTime_All(Original_Date_Time_str=Date_Taken, DateTime_Format=PIL_DateTime_Format)
                        Add_to_Dataframe(GEO_df=GEO_df, GEO_attributes=GEO_Attributes, Date=Formated_Date_Time, Album=Higher_Actual_Folder, Album2=Actual_Folder, Name=filename)
                    Data_df_TQDM.update(1) 

                except Exception as error:
                    Log_file.write(f"""Picture;{Actual_Folder};{filename};{error}\n""")
                    Data_df_TQDM.update(1) 
                    continue

            elif postfix in Supported_video_formats:
                try:
                    GEO_Attributes = Get_Video_GEO(file_path=file_path, Actual_Folder=Actual_Folder, filename=filename)
                    if GEO_Attributes != False:
                        DateTime_Attributes = Get_DateTime_properties(file_path=file_path, atribute="Media created", Actual_Folder=Actual_Folder, filename=filename)
                        Formated_Date_Time =  Format_DateTime_All(Original_Date_Time_str=DateTime_Attributes, DateTime_Format=PIL_DateTime_Format)
                        Add_to_Dataframe(GEO_df=GEO_df, GEO_attributes=GEO_Attributes, Date=Formated_Date_Time, Album=Higher_Actual_Folder, Album2=Actual_Folder, Name=filename)

                    Data_df_TQDM.update(1) 

                except:
                    Log_file.write(f"""Video;{Actual_Folder};{filename};{error}\n""")
                    Data_df_TQDM.update(1) 
                    continue

            else:
                Log_file.write(f"""Postfix;{Actual_Folder};{filename};Not suported file type\n""")
                Data_df_TQDM.update(1) 
                continue

    Data_df_TQDM.close()

    # Create GEOJson file
    Create_geojson(GEO_df=GEO_df)

    Log_file.close()
    Log_file = open("Logs\\GEO_JSON_Log.csv", "r", encoding="UTF-8")
    file_contents = Log_file.read()
    print(file_contents)
    Log_file.close()