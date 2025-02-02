import os
import logging
from datetime import datetime
from PIL import Image
import subprocess
import piexif

import Libs.Defaults_Lists as Defaults_Lists
from customtkinter import CTkProgressBar, CTk

logging.basicConfig(level=logging.ERROR)

# -------------------------------------------------------------------------------------------------------------------------------------------------- Set Defaults -------------------------------------------------------------------------------------------------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Date_dt_Format = Settings["MetaData"]["Date_dt_Format"]
Exif_ID = Settings["MetaData"]["Exif_ID"]
GPS_ID = Settings["MetaData"]["GPS_ID"]
DateTime_ID = Settings["MetaData"]["DateTime_ID"]
Date_Taken_ID = Settings["MetaData"]["Date_Taken_ID"]
DateTimeDigitized_ID = Settings["MetaData"]["DateTimeDigitized_ID"]
PreviewDateTime_ID = Settings["MetaData"]["PreviewDateTime_ID"]
Name_format = Settings["General"]["File_Format"]
Property_format = Settings["MetaData"]["Property_format"]

Supported_photo_formats = Settings["General"]["Supported_postfix"]["Photos"]
Supported_video_formats = Settings["General"]["Supported_postfix"]["Videos"]

# -------------------------------------------------------------------------------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Init_Picture_Exif(File_Name: str, file_path: str, postfix: str, DateTime_import:str) -> None:
    # Read the image data using PIL
    image = Image.open(f"{file_path}\\{File_Name}{postfix}")

    exif_dict = {
        "0th": {
            piexif.ImageIFD.DateTime: DateTime_import ,
            piexif.ImageIFD.PreviewDateTime: DateTime_import
        },
        "Exif": {
            piexif.ExifIFD.DateTimeOriginal: DateTime_import,
            piexif.ExifIFD.DateTimeDigitized: DateTime_import
        }
    }

    # Convert the dictionary to bytes
    exif_bytes = piexif.dump(exif_dict)

    image.save(fp=f"{file_path}\\{File_Name}{postfix}", exif=exif_bytes)
    image.close()

def Change_Property_picture(File_Name_dt: datetime, File_Name: str, file_path: str, postfix: str) -> None:
    # Read the image data using PIL
    image = Image.open(f"{file_path}\\{File_Name}{postfix}")
    DateTime_import = File_Name_dt.strftime(Date_dt_Format)

    # Extract EXIF data
    exif1 = image.getexif()
    try:
        Date_Taken = exif1.get_ifd(tag=Exif_ID)[36867]
    except:
        Date_Taken = ""

    # Create exif information to be then updated
    if Date_Taken == "":
        image.close()
        Init_Picture_Exif(File_Name=File_Name, file_path=file_path, postfix=postfix, DateTime_import=DateTime_import)
        image = Image.open(f"{file_path}\\{File_Name}{postfix}")
        DateTime_import = File_Name_dt.strftime(Date_dt_Format)

        # Extract EXIF data
        exif1 = image.getexif()
    else:
        pass

    # Update Dates information --> change define key/values pairs
    exif1.get_ifd(tag=Exif_ID)[DateTime_ID] = DateTime_import
    exif1.get_ifd(tag=Exif_ID)[Date_Taken_ID] = DateTime_import
    exif1.get_ifd(tag=Exif_ID)[DateTimeDigitized_ID] = DateTime_import
    exif1.get_ifd(tag=Exif_ID)[PreviewDateTime_ID] = DateTime_import

    # Update GPS information --> change delete not used keys/values was wrong for CANON EOS-550
    gpsinfo = exif1.get_ifd(tag=GPS_ID)
    GPS_Keep_Keys = [1, 2, 3, 4 ]
    GPS_Delete_Keys = []

    for key, value in gpsinfo.items():
        if key not in GPS_Keep_Keys:
            GPS_Delete_Keys.append(key)

    for key in GPS_Delete_Keys:
        exif1.get_ifd(tag=GPS_ID).pop(key)

    # Save
    image.save(fp=f"{file_path}\\{File_Name}{postfix}", exif=exif1)
    creation_time = File_Name_dt.timestamp()
    modification_time = File_Name_dt.timestamp()
    os.utime(f"{file_path}\\{File_Name}{postfix}", (creation_time, modification_time))

def Change_Property_video(File_Name_dt: datetime, File_Name: str, file_path: str, postfix: str, Property_format:str):
    input_video = f"{file_path}\\{File_Name}{postfix}"
    output_video = f"{file_path}\\{File_Name}A{postfix}"
    Date_Formatted = File_Name_dt.strftime("%Y-%m-%dT%H:%M:%S")

    # TODO --> Zkontrolovat: tenhle zápis přemaže všechna jiná metadata (pokud existujou, jako je GPS ...), musím je zkopírovat a přenést

    # Change MetaData
    metadata_dict = {
        "creation_time": Date_Formatted,
        "date": Date_Formatted}
    
    metadata_args = []
    for key, value in metadata_dict.items():
        metadata_args.extend(['-metadata', f'{key}={value}'])
    
    command = ['ffmpeg','-loglevel', 'quiet', '-i', input_video, '-c', 'copy', *metadata_args, output_video]
    subprocess.run(command, check=True)

    # Save
    creation_time = File_Name_dt.timestamp()
    modification_time = File_Name_dt.timestamp()
    os.utime(path=output_video, times=(creation_time, modification_time))

    # Delete Input file
    os.remove(input_video)

    # Rename Output File
    os.rename(src=output_video, dst=input_video)


def File_Name_Format_Check(File_Name, Name_format):
    try:
        File_Name_dt = datetime.strptime(File_Name, Name_format)
        return File_Name_dt, True
    except:
        return False
    
def Progress_Bar_step(window: CTk, Progress_Bar: CTkProgressBar) -> None:
    Progress_Bar.step()
    window.update_idletasks()

def Progress_Bar_set(window: CTk, Progress_Bar: CTkProgressBar, value: int) -> None:
    Progress_Bar.set(value=value)
    window.update_idletasks()

# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Change_Metadata(Nested_Path: list, window: CTk, Progress_Bar: CTkProgressBar) -> None:
    # Create Log file
    Log_file = open("Libs\\Logs\\Change_Metadata_Log.csv", "w", encoding="UTF-8")
    Log_file.write(f"Type;Folder;File;Error\n")
    Log_file.close()
    Log_file = open("Libs\\Logs\\Change_Metadata_Log.csv", "a", encoding="UTF-8")

    # Get Date for each file
    for actual_path in Nested_Path:
        Actual_Folder_list = actual_path.split("\\")
        Actual_Folder = Actual_Folder_list[-1]

        for filename in os.listdir(actual_path):
            Name_split = os.path.splitext(filename)
            File_Name = Name_split[0]
            postfix = Name_split[1]
            file_path = os.path.join(actual_path, filename)

            if postfix == "":
                continue

            elif postfix in Supported_photo_formats:
                try:
                    File_Name_dt, Correct_Name = File_Name_Format_Check(File_Name=File_Name, Name_format=Name_format)
                    if Correct_Name == True:
                        Change_Property_picture(File_Name_dt=File_Name_dt, File_Name=File_Name, file_path=actual_path, postfix=postfix)
                        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
                    else:
                        Log_file.write(f"""Picture;{Actual_Folder};{filename};File name is not in proper format\n""")
                        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
                        continue
                    
                except Exception as error:
                    Log_file.write(f"""Picture;{Actual_Folder};{filename};{error}\n""")
                    Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
                    continue

            elif postfix in Supported_video_formats:
                try:
                    File_Name_dt, Correct_Name = File_Name_Format_Check(File_Name=File_Name, Name_format=Name_format)
                    if Correct_Name == True:
                        Change_Property_video(File_Name_dt=File_Name_dt, File_Name=File_Name, file_path=actual_path, postfix=postfix, Property_format=Property_format)
                        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
                    else:
                        Log_file.write(f"""Video;{Actual_Folder};{filename};File name is not in proper format\n""")
                        Progress_Bar_step(window=window, Progress_Bar=Progress_Bar)
                        continue
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