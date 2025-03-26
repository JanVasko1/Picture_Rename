# Import Libraries
import os
import json
from glob import glob
from shutil import rmtree, copy
from pandas import DataFrame

import Libs.GUI.Elements as Elements

from customtkinter import CTk

# --------------------------------------------- Folders / Files --------------------------------------------- #
def Create_Folder(Configuration: dict|None, window: CTk|None, file_path: str) -> None:
    # Create Folder
    try: 
        os.makedirs(f"{file_path}")
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title=f"Not possible to create folder int {file_path}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Copy_File(Configuration: dict|None, window: CTk|None, Source_Path: str, Destination_Path: str) -> None:
    try:
        copy(src=Source_Path, dst=Destination_Path)
    except Exception as Error:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title=f"Not possible to copy file:\n From: {Source_Path}\n To: {Destination_Path} ", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Copy_All_File(Configuration: dict|None, window: CTk|None, Source_Path: str, Destination_Path: str, include_hidden: bool) -> None:
    files = glob(pathname=os.path.join(Source_Path, "*"), include_hidden=include_hidden)
    for source_file in files:
        dest_file = source_file.replace(Source_Path, Destination_Path)
        try:
            copy(src=source_file, dst=dest_file)
        except Exception as Error:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title=f"Not possible to copy file:\n From: {Source_Path}\n To: {Destination_Path} ", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

def Delete_Folder(file_path: str) -> None:
    # Create Folder
    try: 
        os.rmdir(path=f"{file_path}")
    except Exception as Error:
        print(Error)

def Delete_Folders(file_path: str) -> None:
    try:
        rmtree(file_path)
    except Exception as Error:
        print(Error)

def Delete_File(file_path: str) -> None:
    # Delete File
    try: 
        os.remove(path=f"{file_path}")
    except Exception as Error:
        print(Error)

def Delete_All_Files(file_path: str, include_hidden: bool) -> None:
    # Delete File
    try:
        files = glob(pathname=os.path.join(file_path, "*"), include_hidden=include_hidden)
        for file in files:
            os.remove(file)
    except Exception as Error:
        print(Error)

def Get_Downloads_File_Path(File_Name: str, File_postfix: str):
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    Destination_File = os.path.join(downloads_folder, os.path.basename(f"{File_Name}.{File_postfix}"))
    return Destination_File
