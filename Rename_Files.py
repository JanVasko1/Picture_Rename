import os
from datetime import datetime, timedelta
from tqdm import tqdm
import logging
import windows_metadata
from Libs import Defaults

logging.basicConfig(level=logging.ERROR)

def Format_DateTime_All(Orifinal_Date_Time_str, Read_format, Export_format):
    Orifinal_Date_Time_str = Orifinal_Date_Time_str.replace("\u200e", "")
    Orifinal_Date_Time_str = Orifinal_Date_Time_str.replace("\u200f", "")
    Orifinal_Date_Time_dt = datetime.strptime(Orifinal_Date_Time_str, Read_format)
    Formated_Date_Time = Orifinal_Date_Time_dt.strftime(Export_format)
    return Formated_Date_Time

def Rename_File(actual_path, Formated_Date_Time, postfix, Export_format):
    add_second = 0  # Because of Take_Date duplicity and this parameter prevents that done for each file separatelly
    try:
        os.rename(file_path, os.path.join(actual_path, f"{Formated_Date_Time}{postfix}"))
    except:
        Formated_Date_Time_dt = datetime.strptime(Formated_Date_Time, Export_format)
        while True:
            Formated_Date_Time_dt = Formated_Date_Time_dt + timedelta(seconds=add_second)
            Formated_Date_Time = Formated_Date_Time_dt.strftime(Export_format)
            try:
                os.rename(file_path, os.path.join(actual_path, f"{Formated_Date_Time}{postfix}"))
                break
            except:
                add_second += 1
                continue

def Get_file_properties(file_path, atribute, Actual_Folder, filename):
    try:
        attributes = windows_metadata.windows_metadata.WindowsAttributes(file_path)
        return attributes[atribute]
    except Exception as error:
        Log_file.write(f"""Property Error;{Actual_Folder};{filename};Missing {atribute}\n""")
        return False

# Defaults
Export_format = "%Y%m%d_%H%M%S"
Attr_format = "%Y-%m-%d %H:%M"
Supported_photo_formats = Defaults.Supported_photo_formats()
Supported_video_formats = Defaults.Supported_video_formats()

print("""
#--------------------------------------------------------------#
# This program will take an metadata from pictures and viedeos # 
# from field "Date Taken" / "Media Created" and apply it as    #
# file name in format: %Y%m%d_%H%M%S"                          #
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
    Log_file = open("Logs\\Rename_Files_Log.csv", "w", encoding="UTF-8")
    Log_file.write(f"Type;Folder;File;Error\n")
    Log_file.close()
    Log_file = open("Logs\\Rename_Files_Log.csv", "a", encoding="UTF-8")
    
    # Get Date for each file
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Data_df_TQDM = tqdm(total=int(File_Count),desc=f"{now}>> File name change from Date Taken")
    for actual_path in Nested_Path:
        Actual_Folder_list = actual_path.split("\\")
        Actual_Folder = Actual_Folder_list[-1]

        for filename in os.listdir(actual_path):
            Nanem_split = os.path.splitext(filename)
            postfix = Nanem_split[1]
            file_path = os.path.join(actual_path, filename)

            if postfix == "":
                continue

            elif postfix in Supported_photo_formats:
                try:
                    Orifinal_Date_Time_str = Get_file_properties(file_path=file_path, atribute="Date taken", Actual_Folder=Actual_Folder, filename=filename)
                    if Orifinal_Date_Time_str != False:
                        Formated_Date_Time =  Format_DateTime_All(Orifinal_Date_Time_str=Orifinal_Date_Time_str, Read_format=Attr_format, Export_format=Export_format)
                    
                        # Rename File
                        Rename_File(actual_path=actual_path, Formated_Date_Time=Formated_Date_Time, postfix=postfix, Export_format=Export_format)
                    Data_df_TQDM.update(1) 

                except Exception as error:
                    Log_file.write(f"""Picture;{Actual_Folder};{filename};{error}\n""")
                    Data_df_TQDM.update(1) 
                    continue

            elif postfix in Supported_video_formats:
                try:
                    Orifinal_Date_Time_str = Get_file_properties(file_path=file_path, atribute="Media created", Actual_Folder=Actual_Folder, filename=filename)
                    if Orifinal_Date_Time_str != False:
                        Formated_Date_Time =  Format_DateTime_All(Orifinal_Date_Time_str=Orifinal_Date_Time_str, Read_format=Attr_format, Export_format=Export_format)

                        # Rename File
                        Rename_File(actual_path=actual_path, Formated_Date_Time=Formated_Date_Time, postfix=postfix, Export_format=Export_format)
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
    Log_file.close()

    Log_file = open("Logs\\Rename_Files_Log.csv", "r", encoding="UTF-8")
    file_contents = Log_file.read()
    print(file_contents)
    Log_file.close()

    