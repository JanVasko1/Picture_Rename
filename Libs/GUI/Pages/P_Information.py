# Import Libraries
import os
import sys
import markdown
from pathlib import Path
from customtkinter import CTk, CTkFrame
from tkhtmlview import HTMLLabel

# Set the root directory of project before local import
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
cut_point = "Stock_Company_Analyzer"
ROOT_DIR = ROOT_DIR.partition(cut_point)[0] + ROOT_DIR.partition(cut_point)[1]
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import Libs.GUI.Elements as Elements
import Libs.Data_Functions as Data_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
# -------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------- #
def Page_Information(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame):
    Work_Area_Detail_Font = Configuration["Labels"]["Main"]["text_color"]
    Work_Area_Detail_Background = list(Configuration["Global_Appearance"]["GUI_Level_ID"]["1"]["fg_color"])
    
    # ------------------------- Main Functions -------------------------#
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

    # ------------------------- Info Text Area -------------------------#
    # Description
    Frame_Information_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Triple_size", GUI_Level_ID=1)

    with open(Data_Functions.Absolute_path(relative_path=Path("Libs\\GUI\\Information.md").resolve()), "r", encoding="UTF-8") as file:
        html_markdown=markdown.markdown( file.read())
    file.close()

    Information_html = HTMLLabel(Frame_Information_Scrollable_Area, html=f"""<p style="color: {HTML_Font_Color};">{html_markdown}</p>""", background=HTML_Background_Color, font="Roboto")
    Information_html.configure(height=270)

    # Build look of Widget
    Frame_Information_Scrollable_Area.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    Information_html.pack(side="top", fill="both", expand=True, padx=10, pady=10)

