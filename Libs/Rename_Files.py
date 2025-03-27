import os
from datetime import datetime, timedelta
import logging
import windows_metadata

import Libs.Data_Functions as Data_Functions
import Libs.GUI.Elements as Elements

from customtkinter import CTkProgressBar, CTk

logging.basicConfig(level=logging.ERROR)

# -------------------------------------------------------------------------------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Format_DateTime_All(Original_Date_Time_str, Read_format, Export_format):
    Original_Date_Time_str = Original_Date_Time_str.replace("\u200e", "")
    Original_Date_Time_str = Original_Date_Time_str.replace("\u200f", "")
    Original_Date_Time_dt = datetime.strptime(Original_Date_Time_str, Read_format)
    Formatted_Date_Time = Original_Date_Time_dt.strftime(Export_format)
    return Formatted_Date_Time

def Rename_File(file_path, actual_path, Formatted_Date_Time, postfix, Export_format):
    add_second = 0  # Because of Take_Date duplicity and this parameter prevents that done for each file separately
    try:
        os.rename(file_path, os.path.join(actual_path, f"{Formatted_Date_Time}{postfix}"))
    except:
        Formatted_Date_Time_dt = datetime.strptime(Formatted_Date_Time, Export_format)
        while True:
            Formatted_Date_Time_dt = Formatted_Date_Time_dt + timedelta(seconds=add_second)
            Formatted_Date_Time = Formatted_Date_Time_dt.strftime(Export_format)
            try:
                os.rename(file_path, os.path.join(actual_path, f"{Formatted_Date_Time}{postfix}"))
                break
            except:
                add_second += 1
                continue

def Get_file_properties(file_path, attribute, Actual_Folder, filename, Log_file):
    try:
        attributes = windows_metadata.windows_metadata.WindowsAttributes(file_path)
        return attributes[attribute]
    except Exception as error:
        Log_file.write(f"""Property Error;{Actual_Folder};{filename};Missing {attribute}\n""")
        return False

def Progress_Bar_step(window: CTk, Progress_Bar: CTkProgressBar) -> None:
    Progress_Bar.step()
    window.update_idletasks()

def Progress_Bar_set(window: CTk, Progress_Bar: CTkProgressBar, value: int) -> None:
    Progress_Bar.set(value=value)
    window.update_idletasks()

# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Rename_Files(Settings: dict, Configuration: dict, Nested_Path: list, window: CTk, Progress_Bar: CTkProgressBar) -> None:
    Export_format = Settings["General"]["File_Format"]
    Attr_format = Settings["Rename"]["Attr_format"]
    Supported_photo_formats = Settings["General"]["Supported_postfix"]["Photos"]
    Supported_video_formats = Settings["General"]["Supported_postfix"]["Videos"]

    # Create Log file
    Log_file = open(Data_Functions.Absolute_path(relative_path=f"Libs\\Logs\\Rename_Files_Log.csv"), "w", encoding="UTF-8")
    Log_file.write(f"Type;Folder;File;Error\n")
    Log_file.close()
    Log_file = open(Data_Functions.Absolute_path(relative_path=f"Libs\\Logs\\Rename_Files_Log.csv"), "a", encoding="UTF-8")
    
    # Get Date for each file
    for actual_path in Nested_Path:
        Actual_Folder_list = actual_path.split("\\")
        Actual_Folder = Actual_Folder_list[-1]

        for filename in os.listdir(actual_path):
            Name_split = os.path.splitext(filename)
            postfix = Name_split[1]
            file_path = os.path.join(actual_path, filename)

            if postfix == "":
                continue

            elif postfix in Supported_photo_formats:
                try:
                    Original_Date_Time_str = Get_file_properties(file_path=file_path, attribute="Date taken", Actual_Folder=Actual_Folder, filename=filename, Log_file=Log_file)
                    if Original_Date_Time_str != False:
                        Formatted_Date_Time =  Format_DateTime_All(Original_Date_Time_str=Original_Date_Time_str, Read_format=Attr_format, Export_format=Export_format)
                    
                        # Rename File
                        Rename_File(file_path=file_path, actual_path=actual_path, Formatted_Date_Time=Formatted_Date_Time, postfix=postfix, Export_format=Export_format)
                    Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)

                except Exception as error:
                    Log_file.write(f"""Picture;{Actual_Folder};{filename};{error}\n""")
                    Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
                    continue

            elif postfix in Supported_video_formats:
                try:
                    Original_Date_Time_str = Get_file_properties(file_path=file_path, attribute="Media created", Actual_Folder=Actual_Folder, filename=filename)
                    if Original_Date_Time_str != False:
                        Formatted_Date_Time =  Format_DateTime_All(Original_Date_Time_str=Original_Date_Time_str, Read_format=Attr_format, Export_format=Export_format)

                        # Rename File
                        Rename_File(file_path=file_path, actual_path=actual_path, Formatted_Date_Time=Formatted_Date_Time, postfix=postfix, Export_format=Export_format)
                    Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)

                except Exception as error:
                    Log_file.write(f"""Video;{Actual_Folder};{filename};{error}\n""")
                    Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
                    continue

            else:
                Log_file.write(f"""Postfix;{Actual_Folder};{filename};Not supported file type\n""")
                Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
                continue

    Log_file.close()
    Progress_Bar_set(window=window, Progress_Bar=Progress_Bar, value=1) 
    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Files successfully renamed.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
