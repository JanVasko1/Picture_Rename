# Import Libraries
import os
import threading

from Libs.GUI.Widgets.Widgets_Class import WidgetFrame, WidgetRow_CheckBox, WidgetRow_Input_Entry, Widget_Buttons_Row
import Libs.GUI.Elements as Elements

from customtkinter import CTk, CTkFrame, BooleanVar, CTkProgressBar

# -----------------------------------------------------------------------------------------Local Functions ----------------------------------------------------------------------------------------- #
def Nested_Folders(Nested_Folder: bool, Selected_path: str) -> list[list, int]:
    if Nested_Folder == True:
        # Read actual folder and folders inside
        Nested_Path = [x[0] for x in os.walk(Selected_path)]
        File_Count = sum([len(files) for r, d, files in os.walk(Selected_path)])
    else:
        Nested_Path = [Selected_path]
        File_Count = [len(files) for r, d, files in os.walk(Selected_path)]
        File_Count = File_Count[0]
    return Nested_Path, File_Count

def Prepare_Process_Metadata(Settings: dict, Configuration: dict, window: CTk, Metadata_Path_row: WidgetRow_Input_Entry, Progress_Bar: CTkProgressBar) -> None:
    Nested_Folder = Settings["0"]["MetaData"]["Nested_Folders"]
    Selected_path = Metadata_Path_row.Get_Value()
    if Selected_path == "":
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"No path selected.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    else:
        import Libs.Process.Change_metadata as Change_metadata
        Nested_Path, File_Count = Nested_Folders(Nested_Folder=Nested_Folder, Selected_path=Selected_path)
        Progress_Bar.configure(determinate_speed = round(number=50 / File_Count, ndigits=3), progress_color="#517A31")
        Generate_META_thread = threading.Thread(target=Change_metadata.Change_Metadata, args=(Settings, Configuration, Nested_Path, window, Progress_Bar))
        Generate_META_thread.start()
        Generate_META_thread.join(timeout=0.1) 

def Prepare_Process_Rename(Settings: dict, Configuration: dict, window: CTk, Rename_Path_Row: WidgetRow_Input_Entry, Progress_Bar: CTkProgressBar) -> None:
    Nested_Folder = Settings["0"]["Rename"]["Nested_Folders"]
    Selected_path = Rename_Path_Row.Get_Value()
    if Selected_path == "":
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"No path selected.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    else:
        import Libs.Process.Rename_Files as Rename_Files

        Nested_Path, File_Count = Nested_Folders(Nested_Folder=Nested_Folder, Selected_path=Selected_path)
        Progress_Bar.configure(determinate_speed = round(number=50 / File_Count, ndigits=3), progress_color="#517A31")
        Generate_RENAME_thread = threading.Thread(target=Rename_Files.Rename_Files, args=(Settings, Configuration, Nested_Path, window, Progress_Bar))
        Generate_RENAME_thread.start()
        Generate_RENAME_thread.join(timeout=0.1) 

def Prepare_Process_GeoJson(Settings: dict, Configuration: dict, window: CTk, File_Name_Row: WidgetRow_Input_Entry, Export_Path_Row: WidgetRow_Input_Entry, Progress_Bar: CTkProgressBar) -> None:
    Nested_Folder = Settings["0"]["GEOJson"]["Nested_Folders"]
    Export_File_Name = File_Name_Row.Get_Value()
    Selected_path = Export_Path_Row.Get_Value()
    if Selected_path == "":
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"No path selected.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
    else:
        import Libs.Process.Generate_GEO_json as Generate_GEO_json
        Nested_Path, File_Count = Nested_Folders(Nested_Folder=Nested_Folder, Selected_path=Selected_path)
        Progress_Bar.configure(determinate_speed = round(number=50 / File_Count, ndigits=3), progress_color="#517A31")
        Generate_GEO_thread = threading.Thread(target=Generate_GEO_json.GEO_Json, args=(Settings, Configuration, Nested_Path, window, Progress_Bar, Export_File_Name))
        Generate_GEO_thread.start()
        Generate_GEO_thread.join(timeout=0.1) 


# -----------------------------------------------------------------------------------------Main Functions ----------------------------------------------------------------------------------------- #
def Metadata_new(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame, Progress_Bar: CTkProgressBar, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Nested_Folder_Metadata = Settings["0"]["MetaData"]["Nested_Folders"]
    Nested_Folder_Metadata_Variable = BooleanVar(master=Frame, value=Nested_Folder_Metadata, name="Nested_Folder_Metadata_Variable") 

    # ------------------------- Main Functions -------------------------#
    # Widget
    Metadata_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Metadata", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Change Date Take / Media Created date and time according to file name.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Nested_Folders_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Metadata_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Label="Nested Folders", Variable=Nested_Folder_Metadata_Variable, Save_To="Settings", Save_path=["0", "MetaData", "Nested_Folders"])
    Metadata_Path_row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Metadata_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Field_Size="Normal", Label="Path", Value="", placeholder_text="Folder path.")

    # Buttons
    Buttons_texts = ["Process"]
    Buttons_ToolTips = ["Change MetaData of files in folder/s."]
    Buttons_Functions = [lambda: Prepare_Process_Metadata(Settings=Settings, Configuration=Configuration, window=window, Metadata_Path_row=Metadata_Path_row, Progress_Bar=Progress_Bar)]
    Button_Row = Widget_Buttons_Row(Configuration=Configuration, master=Metadata_Widget.Body_Frame, Field_Frame_Type="Single_Column", Buttons_count=1, Button_Size="Small", Button_Text=Buttons_texts, Button_ToolTips=Buttons_ToolTips, Button_Functions=Buttons_Functions, GUI_Level_ID=GUI_Level_ID)

    # Add Fields to Widget Body
    Metadata_Widget.Add_row(Rows=[Nested_Folders_Row, Metadata_Path_row, Button_Row])

    return Metadata_Widget

def Rename_new(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame, Progress_Bar: CTkProgressBar, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Nested_Folder_Rename = Settings["0"]["Rename"]["Nested_Folders"]
    Nested_Folder_Rename_Variable = BooleanVar(master=Frame, value=Nested_Folder_Rename, name="Nested_Folder_Rename_Variable") 

    # ------------------------- Main Functions -------------------------#
    # Widget
    Rename_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Rename", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Rename file according to Date Taken for pictures or Created Date for video files.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Nested_Folders_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Rename_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Label="Nested Folders", Variable=Nested_Folder_Rename_Variable, Save_To="Settings", Save_path=["0", "Rename", "Nested_Folders"])
    Rename_Path_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=Rename_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Field_Size="Normal", Label="Path", Value="", placeholder_text="Folder path.")

    # Buttons
    Buttons_texts = ["Process"]
    Buttons_ToolTips = ["Change File names in folder/s."]
    Buttons_Functions = [lambda: Prepare_Process_Rename(Settings=Settings, Configuration=Configuration, window=window, Rename_Path_Row=Rename_Path_Row, Progress_Bar=Progress_Bar)]
    Button_Row = Widget_Buttons_Row(Configuration=Configuration, master=Rename_Widget.Body_Frame, Field_Frame_Type="Single_Column", Buttons_count=1, Button_Size="Small", Button_Text=Buttons_texts, Button_ToolTips=Buttons_ToolTips, Button_Functions=Buttons_Functions, GUI_Level_ID=GUI_Level_ID)

    # Add Fields to Widget Body
    Rename_Widget.Add_row(Rows=[Nested_Folders_Row, Rename_Path_Row, Button_Row])

    return Rename_Widget


def GEOJson_new(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame, Progress_Bar: CTkProgressBar, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # ---------------------------- Defaults ----------------------------#
    Nested_Folder_GEOJson = Settings["0"]["GEOJson"]["Nested_Folders"]
    Nested_Folder_GEOJson_Variable = BooleanVar(master=Frame, value=Nested_Folder_GEOJson, name="Nested_Folder_GEOJson_Variable") 
    
    # ------------------------- Main Functions -------------------------#
    # Widget
    GEOJson_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Geo json", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Creates GEO JSON file from photos/videos from selected folder/s.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Nested_Folders_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=GEOJson_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Label="Nested Folders", Variable=Nested_Folder_GEOJson_Variable, Save_To="Settings", Save_path=["0", "GEOJson", "Nested_Folders"])
    File_Name_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=GEOJson_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Field_Size="Normal", Label="File Name", Value="", placeholder_text="Folder path.")
    Export_Path_Row = WidgetRow_Input_Entry(Settings=Settings, Configuration=Configuration, master=GEOJson_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Field_Size="Normal", Label="Path", Value="", placeholder_text="Folder path.")

    # Buttons
    Buttons_texts = ["Process"]
    Buttons_ToolTips = ["Create geojson file."]
    Buttons_Functions = [lambda: Prepare_Process_GeoJson(Settings=Settings, Configuration=Configuration, window=window, File_Name_Row=File_Name_Row, Export_Path_Row=Export_Path_Row, Progress_Bar=Progress_Bar)]
    Button_Row = Widget_Buttons_Row(Configuration=Configuration, master=GEOJson_Widget.Body_Frame, Field_Frame_Type="Single_Column", Buttons_count=1, Button_Size="Small", Button_Text=Buttons_texts, Button_ToolTips=Buttons_ToolTips, Button_Functions=Buttons_Functions, GUI_Level_ID=GUI_Level_ID)

    # Add Fields to Widget Body
    GEOJson_Widget.Add_row(Rows=[Nested_Folders_Row, File_Name_Row, Export_Path_Row, Button_Row])

    return GEOJson_Widget
