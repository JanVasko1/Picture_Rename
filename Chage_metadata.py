import os
from datetime import datetime
from tqdm import tqdm
import windows_metadata
from PIL import Image
from PIL.ExifTags import TAGS
from Libs import Defaults

Date_dt_Format = "%Y:%m:%d %H:%M:%S"
Exif_ID = 34665
GPS_ID = 34853

def Change_Property_picture(File_Name_dt: datetime, File_Name: str, file_path: str, postfix: str) -> None:
    # Read the image data using PIL
    image = Image.open(f"{file_path}\\{File_Name}{postfix}")
    DateTime_import = File_Name_dt.strftime(Date_dt_Format)

    # Extract EXIF data
    exif1 = image.getexif()

    # Update Dates information --> change define key/values pairs
    exif1.get_ifd(tag=Exif_ID)[306] = DateTime_import
    exif1.get_ifd(tag=Exif_ID)[36867] = DateTime_import
    exif1.get_ifd(tag=Exif_ID)[36868] = DateTime_import
    exif1.get_ifd(tag=Exif_ID)[50971] = DateTime_import

    # Udpate GPS information --> change delete not used keys/values was wrong for CANON EOS-550
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

def Change_Property_video(File_Name_dt: datetime, File_Name: str, file_path: str, Property_format:str):
    Date_Formated = File_Name_dt.strftime(Property_format)
    with open(file=file_path, mode="a+b") as file:
        
        attributes = windows_metadata.windows_metadata.WindowsAttributes(file_path)
        
        # Date taken 
        try:
            attributes["Date taken"] = Date_Formated
        except:
            # Create Property
            pass
        
        # Media created
        try:
            attributes["Media created"] = Date_Formated
        except:
            # Create Property
            pass
            
        # Date created 
        try:
            attributes["Date created"] = Date_Formated
        except:
            # Create Property
            pass
            
        # Date modified
        try:
            attributes["Date modified"] = Date_Formated
        except:
            # Create Property 
            pass


def File_Name_Format_Check(File_Name, Name_format):
    try:
        File_Name_dt = datetime.strptime(File_Name, Name_format)
        return File_Name_dt, True
    except:
        return False

print("""
#--------------------------------------------------------------#
# This program will apply media file name from format          #
# "%Y%m%d_%H%M%S" and apply it into these metadata:            #
# 1) Date taken                                                #
# 2) Media created                                             #
# 3) Date created                                              #
# 4) Date modified                                             #
#--------------------------------------------------------------#""")

# Defaults
Name_format = "%Y%m%d_%H%M%S"
Property_format = "%Y-%m-%d %H:%M:%S"
Supported_photo_formats = Defaults.Supported_photo_formats()
Supported_video_formats = Defaults.Supported_video_formats()
# List of files in folder
while True:
    Selected_path = input("Give me file path to pictures: ")
    Nested_Folder = input("Do you want also check nested Folders? [Y/N]: ")
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
    Log_file = open("Logs\\Change_Metadata_Log.csv", "w", encoding="UTF-8")
    Log_file.write(f"Type;Folder;File;Error\n")
    Log_file.close()
    Log_file = open("Logs\\Change_Metadata_Log.csv", "a", encoding="UTF-8")

    # Get Date for each file
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Data_df_TQDM = tqdm(total=int(File_Count),desc=f"{now}>> File name change from Date Taken")
    for actual_path in Nested_Path:
        Actual_Folder_list = actual_path.split("\\")
        Actual_Folder = Actual_Folder_list[-1]

        for filename in os.listdir(actual_path):
            Nanem_split = os.path.splitext(filename)
            File_Name = Nanem_split[0]
            postfix = Nanem_split[1]
            file_path = os.path.join(actual_path, filename)

            if postfix == "":
                continue

            elif postfix in Supported_photo_formats:
                try:
                    File_Name_dt, Corret_Name = File_Name_Format_Check(File_Name=File_Name, Name_format=Name_format)
                    if Corret_Name == True:
                        Change_Property_picture(File_Name_dt=File_Name_dt, File_Name=File_Name, file_path=actual_path, postfix=postfix)
                        Data_df_TQDM.update(1) 
                    else:
                        Log_file.write(f"""Picture;{Actual_Folder};{filename};File name is not in proper format\n""")
                        Data_df_TQDM.update(1) 
                        continue
                    
                except Exception as error:
                    Log_file.write(f"""Picture;{Actual_Folder};{filename};{error}\n""")
                    Data_df_TQDM.update(1) 
                    continue

            elif postfix in Supported_video_formats:
                try:
                    File_Name_dt, Corret_Name = File_Name_Format_Check(File_Name=File_Name, Name_format=Name_format)
                    if Corret_Name == True:
                        Change_Property_video(File_Name_dt=File_Name_dt, File_Name=File_Name, file_path=file_path, Property_format=Property_format)
                        Data_df_TQDM.update(1) 
                    else:
                        Log_file.write(f"""Video;{Actual_Folder};{filename};File name is not in proper format\n""")
                        Data_df_TQDM.update(1) 
                        continue
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

    Log_file = open("Logs\\Change_Metadata_Log.csv", "r", encoding="UTF-8")
    file_contents = Log_file.read()
    print(file_contents)
    Log_file.close()

    