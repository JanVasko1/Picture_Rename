# Import Libraries
import os
import json
from glob import glob

from customtkinter import CTk, CTkFrame, CTkButton, set_appearance_mode
from Libs.GUI.CTk.ctk_scrollable_dropdown import CTkScrollableDropdown as CTkScrollableDropdown 
from tkhtmlview import HTMLLabel
from markdown import markdown

import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.CustomTkinter_Functions as CustomTkinter_Functions

import Libs.Data_Functions as Data_Functions

# ------------------------------------------------------------------------------------------------------------------------------------ Header ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Header(Settings: dict, Configuration: dict|None, window: CTk, Frame: CTkFrame) -> CTkFrame:
    # ------------------------- Local Functions -------------------------#
    def Theme_Change():
        Current_Theme = CustomTkinter_Functions.Get_Current_Theme() 
        if Current_Theme == "Dark":
            set_appearance_mode(mode_string="light")
        elif Current_Theme == "Light":
            set_appearance_mode(mode_string="dark")
        elif Current_Theme == "System":
            set_appearance_mode(mode_string="dark")
        else:
            set_appearance_mode(mode_string="system")

    def Show_Version_List(Clicked_on: CTkButton) -> None:
        Work_Area_Detail_Font = Configuration["Labels"]["Main"]["text_color"]
        Work_Area_Detail_Background = list(Configuration["Global_Appearance"]["GUI_Level_ID"]["2"]["fg_color"])

        # TopUp Window
        Version_List_Window_geometry = (1400, 800)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Clicked_on, New_Window_width=Version_List_Window_geometry[0])
        Version_List_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Version List", max_width=Version_List_Window_geometry[0], max_height=Version_List_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=True, Always_on_Top=True)

         # Get Theme --> because of background color
        Current_Theme = CustomTkinter_Functions.Get_Current_Theme() 

        if Current_Theme == "Dark":
            HTML_Background_Color = Work_Area_Detail_Background[1]
            HTML_Font_Color = Work_Area_Detail_Font[1]
        elif Current_Theme == "Light":
            HTML_Background_Color = Work_Area_Detail_Background[0]
            HTML_Font_Color = Work_Area_Detail_Font[0]
        elif Current_Theme == "System":
            HTML_Background_Color = Work_Area_Detail_Background[1]
            HTML_Font_Color = Work_Area_Detail_Font[1]
        else:
            HTML_Background_Color = Work_Area_Detail_Background[1]
            HTML_Font_Color = Work_Area_Detail_Font[1]

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Version_List_Window, Name="Version List", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Show software changes.", GUI_Level_ID=1)
        Frame_Main.configure(bg_color = "#000001", height=700)
        Frame_Body = Frame_Main.children["!ctkframe2"]

        Frame_Information_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Double_size", GUI_Level_ID=2)

        with open(Data_Functions.Absolute_path(relative_path=f"Libs\\App\\Version_list.md"), "r", encoding="UTF-8") as file:
            html_markdown=markdown(text=file.read())
        file.close()

        Information_html = HTMLLabel(Frame_Information_Scrollable_Area, html=html_markdown, background=HTML_Background_Color, font=("Roboto", 11), fg=HTML_Font_Color,)

        # Build look of Widget
        Frame_Main.pack(side="top", fill="y", expand=False, padx=10, pady=10)
        Frame_Information_Scrollable_Area.pack(side="top", fill="none", expand=False, padx=10, pady=10)
        Information_html.pack(side="top", fill="both", expand=False, padx=10, pady=10)

    # ------------------------- Main Functions -------------------------#
    # Theme Change - Button
    Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="sun-moon", Icon_Size="Header", Button_Size="Picture_Transparent")
    Icon_Theme.configure(text="")
    Icon_Theme.configure(command = lambda: Theme_Change())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Change theme.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Version list
    Icon_Versions = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="file-stack", Icon_Size="Header", Button_Size="Picture_Transparent")
    Icon_Versions.configure(command = lambda: Show_Version_List(Clicked_on=Icon_Versions))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Versions, message="Show version changes log.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Build look of Widget
    Icon_Theme.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Icon_Versions.pack(side="right", fill="none", expand=False, padx=5, pady=5)
