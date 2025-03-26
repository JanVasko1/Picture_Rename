# Import Libraries
import os
import markdown

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

import customtkinter
from customtkinter import CTk, CTkFrame
from tkhtmlview import HTMLLabel

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

def Get_Current_Theme() -> str:
    Current_Theme = customtkinter.get_appearance_mode()
    return Current_Theme

# -------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------- #
def Page_Information(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame):
    Work_Area_Detail_Font = Configuration["Labels"]["Main"]["text_color"]
    Work_Area_Detail_Background = Configuration["Frames"]["Widgets"]["Widget_Frames"]["Scrollable_Frames"]["Triple_size"]["fg_color"]
    
    # ------------------------- Main Functions -------------------------#
    # Get Theme --> because of background color
    Current_Theme = Get_Current_Theme() 

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

    # ------------------------- Info Text Area -------------------------#
    # Description
    Frame_Information_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Triple_size", GUI_Level_ID=1)

    with open(Defaults_Lists.Absolute_path(relative_path="Libs\\GUI\\Information.md"), "r", encoding="UTF-8") as file:
        html_markdown=markdown.markdown( file.read())
    file.close()

    Information_html = HTMLLabel(Frame_Information_Scrollable_Area, html=f"{html_markdown}", background=HTML_Background_Color, font="Roboto", fg=HTML_Font_Color)
    Information_html.configure(height=700)

    # Build look of Widget
    Frame_Information_Scrollable_Area.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    Information_html.pack(side="top", fill="both", expand=True, padx=10, pady=10)

