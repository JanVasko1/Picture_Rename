# Import Libraries
import time

from customtkinter import CTk, CTkFrame

import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Pages.P_GEO_json as P_GEO_json
import Libs.GUI.Pages.P_Information as P_Information
import Libs.GUI.Pages.P_MetaData as P_MetaData
import Libs.GUI.Pages.P_Rename as P_Rename
import Libs.GUI.Pages.P_Settings as P_Settings

import Libs.GUI.Elements as Elements

def Get_Side_Bar(Settings: dict, Configuration: dict|None, window: CTk, Frame_Work_Area_Main: CTkFrame, Side_Bar_Frame: CTkFrame) -> None:
    Application = Defaults_Lists.Load_Application()
    Program_Version = Application["Application"]["Version"]

    Icon_Default_pady = 10
    Side_Bar_Top_pady = 65
    Side_Bar_Bottom_pady = 35

    # ------------------------- Local Functions -------------------------#
    def Clear_Frame(Pre_Working_Frame: CTkFrame) -> None:
        # Find
        for widget in Pre_Working_Frame.winfo_children():
            widget.destroy()

    def Show_ChangeMetaData_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=(Side_Bar_Top_pady, Icon_Default_pady), sticky="e")
        P_MetaData.Page_Metadata(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)

    def Show_RenameFile_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        P_Rename.Page_Rename(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)

    def Show_GEOJSON_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        P_GEO_json.Page_Geo_Json(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)

    def Show_Information_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        P_Information.Page_Information(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)

    def Show_Settings_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        P_Settings.Page_Settings(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)

    # ------------------------- Main Functions -------------------------#
    Active_Window = Elements.Get_Frame(Configuration=Configuration, Frame=Side_Bar_Frame, Frame_Size="SideBar_active")

    # Page - Metadata
    Icon_Frame_MetaData = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="replace", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_MetaData.configure(command = lambda: Show_ChangeMetaData_Page(Active_Window = Active_Window, Side_Bar_Row=0))    
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_MetaData, message="Change metadata photo / video file.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - REname file
    Icon_Frame_Rename_File = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="file-pen", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Rename_File.configure(command = lambda: Show_RenameFile_Page(Active_Window = Active_Window, Side_Bar_Row=1))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Rename_File, message="Rename File.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Data
    Icon_Frame_GeoJson = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="map-pin", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_GeoJson.configure(command = lambda: Show_GEOJSON_Page(Active_Window = Active_Window, Side_Bar_Row=2))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_GeoJson, message="GEO Json creation.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Information
    Icon_Frame_Information = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="info", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Information.configure(command = lambda: Show_Information_Page(Active_Window = Active_Window, Side_Bar_Row=3))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Information, message="Information page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Settings
    Icon_Frame_Settings = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="settings", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    Icon_Frame_Settings.configure(command = lambda: Show_Settings_Page(Active_Window = Active_Window, Side_Bar_Row=4))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Settings, message="Settings page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Close Application
    Icon_Frame_Close = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="power", Icon_Size="Side_Bar_close", Button_Size="Picture_Transparent")
    Icon_Frame_Close.configure(command = lambda: window.quit())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Close, message="Close.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Program Version
    Program_Version_text = Elements.Get_Label(Configuration=Configuration, Frame=Side_Bar_Frame, Label_Size="Field_Label", Font_Size="Field_Label")
    Program_Version_text.configure(text=f"{Program_Version}")

    # Build look of Widget
    Active_Window.grid(row=0, column=0, padx=(10, 2), pady=(Side_Bar_Top_pady, Icon_Default_pady), sticky="e")
    Icon_Frame_MetaData.grid(row=0, column=1, padx=(0, 0), pady=(Side_Bar_Top_pady, Icon_Default_pady), sticky="w")
    Icon_Frame_Rename_File.grid(row=1, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_GeoJson.grid(row=2, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_Information.grid(row=3, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_Settings.grid(row=4, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_Close.grid(row=5, column=1, padx=(0, 10), pady=(Icon_Default_pady, Side_Bar_Bottom_pady), sticky="w")
    Program_Version_text.grid(row=9, column=0, padx=(0, 0), pady=(0, 10), sticky="s", columnspan=2)

    # Initiate default window
    Show_ChangeMetaData_Page(Active_Window = Active_Window, Side_Bar_Row=0)