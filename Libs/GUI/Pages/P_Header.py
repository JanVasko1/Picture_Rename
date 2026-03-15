# Import Libraries
import os
import sys
from customtkinter import CTk, CTkFrame, CTkButton, set_appearance_mode
from tkhtmlview import HTMLLabel
from markdown import markdown
from pathlib import Path

# Set the root directory of project before local import
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
cut_point = "Stock_Company_Analyzer"
ROOT_DIR = ROOT_DIR.partition(cut_point)[0] + ROOT_DIR.partition(cut_point)[1]
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.Data_Functions as Data_Functions
from Libs.GUI.CTk.ctk_scrollable_dropdown import CTkScrollableDropdown as CTkScrollableDropdown 

class HeaderBarApp:
    def __init__(self, Settings: dict, Configuration: dict|None, window: CTk|None, Frame: CTkFrame, Frame_Side_Bar: CTkFrame):    
        self.Settings = Settings
        self.Configuration = Configuration
        self.window = window
        self.Frame = Frame
        self.Frame_Side_Bar = Frame_Side_Bar

        # ------------------- Templates ------------------- #
        # Theme Change - Button
        self.Icon_Theme = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Frame, Icon_Name="sun-moon", Icon_Size="Header", Button_Size="Picture_Transparent")
        self.Icon_Theme.configure(text="")
        self.Icon_Theme.configure(command = lambda: self.Theme_Change())
        Elements.Get_ToolTip(Configuration=self.Configuration, widget=self.Icon_Theme, message="Change theme.", ToolTip_Size="Normal", GUI_Level_ID=0)

        # Version list
        self.Icon_Versions = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Frame, Icon_Name="file-stack", Icon_Size="Header", Button_Size="Picture_Transparent")
        self.Icon_Versions.configure(command = lambda: self.Show_Version_List(Clicked_on=self.Icon_Versions))
        Elements.Get_ToolTip(Configuration=self.Configuration, widget=self.Icon_Versions, message="Show version changes log.", ToolTip_Size="Normal", GUI_Level_ID=0)

        # Build look of Widget
        self.Icon_Theme.pack(side="right", fill="none", expand=False, padx=5, pady=5)
        self.Icon_Versions.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    def Theme_Change(self):
        self.Current_Theme = CustomTkinter_Functions.Get_Current_Theme() 
        if self.Current_Theme == "Dark":
            set_appearance_mode(mode_string="light")
        elif self.Current_Theme == "Light":
            set_appearance_mode(mode_string="dark")
        elif self.Current_Theme == "System":
            set_appearance_mode(mode_string="dark")
        else:
            set_appearance_mode(mode_string="system")

    def Show_Version_List(self, Clicked_on: CTkButton) -> None:
        Work_Area_Detail_Font = self.Configuration["Labels"]["Main"]["text_color"]
        Work_Area_Detail_Background = list(self.Configuration["Global_Appearance"]["GUI_Level_ID"]["2"]["fg_color"])

        # TopUp Window
        Version_List_Window_geometry = (1400, 800)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Clicked_on, New_Window_width=Version_List_Window_geometry[0])
        Version_List_Window = Elements_Groups.Get_Pop_up_window(Configuration=self.Configuration, title="Version List", max_width=Version_List_Window_geometry[0], max_height=Version_List_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=True, Always_on_Top=True)

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
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=self.Configuration, Frame=Version_List_Window, Name="Version List", Additional_Text="<ESC> to close.", Widget_size="Single_size", Widget_Label_Tooltip="Show software changes.", GUI_Level_ID=1)
        Frame_Main.configure(bg_color = "#000001", height=700)
        Frame_Body = Frame_Main.children["!ctkframe2"]

        Frame_Information_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=self.Configuration, Frame=Frame_Body, Frame_Size="Double_size", GUI_Level_ID=2)

        with open(Data_Functions.Absolute_path(relative_path=Path(f"Libs\\App\\Version_list.md").resolve()), "r", encoding="UTF-8") as file:
            html_markdown=markdown(text=file.read())
        file.close()

        Information_html = HTMLLabel(Frame_Information_Scrollable_Area, html=f"""<p style="color: {HTML_Font_Color};">{html_markdown}</p>""", background=HTML_Background_Color, font=("Roboto", 11))
        Information_html.configure(height=210)

        # Build look of Widget
        Frame_Main.pack(side="top", fill="y", expand=False, padx=10, pady=10)
        Frame_Information_Scrollable_Area.pack(side="top", fill="none", expand=False, padx=10, pady=10)
        Information_html.pack(side="top", fill="both", expand=False, padx=10, pady=10)
