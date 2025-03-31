# Import Libraries
import os

import Libs.GUI.Elements as Elements
import Libs.GUI.Widgets.W_Settings as W_Settings

from customtkinter import CTk, CTkFrame

# -------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------- #
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

# -------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------- #
def Page_Settings(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame):
    # ------------------------- Main Functions -------------------------#

    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame, Tab_size="Normal", GUI_Level_ID=1)
    TabView.pack_propagate(flag=False)
    Tab_Gen = TabView.add("General")
    Tab_Gen.pack_propagate(flag=False)
    Tab_Photos = TabView.add("Photo formats")
    Tab_Photos.pack_propagate(flag=False)
    Tab_Videos = TabView.add("Video formats")
    Tab_Videos.pack_propagate(flag=False)
    TabView.set("General")

    Tab_Gen_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_Photos_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Tab_Videos_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Gen_ToolTip_But, message="Application General Setup.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Photos_ToolTip_But, message="Supported Photo formats postfixes.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Videos_ToolTip_But, message="Supported Video formats postfixes.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # ---------- Settings ---------- #
    Frame_Settings_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Gen, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_P_Formats_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Photos, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_V_Formats_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Videos, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    
    Photo_Postfix_Widget = W_Settings.Settings_Supported_Photo(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_P_Formats_Column_A, GUI_Level_ID=2)
    Video_Postfix_Widget = W_Settings.Settings_Supported_Video(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_V_Formats_Column_A, GUI_Level_ID=2)

    # Build look of Widget
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    Frame_Settings_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)


    Frame_P_Formats_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Photo_Postfix_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Frame_V_Formats_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Video_Postfix_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Apperance_Widget = W_Settings.Settings_General_Color(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Settings_Column_A, GUI_Level_ID=2)
    Apperance_Widget.Show()   
