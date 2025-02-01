# Import Libraries
import time
import os
import markdown

from tkinter import ttk
import customtkinter
from customtkinter import CTk, CTkFrame

import Libs.GUI.Widgets.Pages as Pages
import Libs.GUI.Widgets.Settings as Settings_Widgets
import Libs.GUI.Elements as Elements
import pywinstyles
from tkhtmlview import HTMLLabel

import Libs.Defaults_Lists as Defaults_Lists

# ------------------------------------------------------------------------------------------------------------------------------------ Set Defaults ------------------------------------------------------------------------------------------------------------------------------------ #
Configuration = Defaults_Lists.Load_Configuration() 

Win_Style_Actual = Configuration["Global_Appearance"]["Window"]["Style"]
Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]

SideBar_Width = Configuration["Frames"]["Page_Frames"]["SideBar"]["width"]

# ------------------------------------------------------------------------------------------------------------------------------------ Local Functions ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Current_Theme() -> str:
    Current_Theme = customtkinter.get_appearance_mode()
    return Current_Theme

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


# ------------------------------------------------------------------------------------------------------------------------------------ Header ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Header(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Local Functions -------------------------#
    def Theme_Change():
        Current_Theme = Get_Current_Theme() 
        if Current_Theme == "Dark":
            customtkinter.set_appearance_mode(mode_string="light")
        elif Current_Theme == "Light":
            customtkinter.set_appearance_mode(mode_string="dark")
        elif Current_Theme == "System":
            customtkinter.set_appearance_mode(mode_string="dark")
        else:
            customtkinter.set_appearance_mode(mode_string="system")

    # ------------------------- Main Functions -------------------------#
    # Theme Change - Button
    Icon_Theme = Elements.Get_Button_Icon(Frame=Frame, Icon_Set="lucide", Icon_Name="sun-moon", Icon_Size="Header", Button_Size="Picture_Theme")
    Icon_Theme.configure(text="")
    Icon_Theme.configure(command = lambda: Theme_Change())
    Elements.Get_ToolTip(widget=Icon_Theme, message="Change theme.", ToolTip_Size="Normal")

    # Build look of Widget
    Icon_Theme.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    

# ------------------------------------------------------------------------------------------------------------------------------------ Side Bar ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Side_Bar(Side_Bar_Frame: CTk|CTkFrame, Side_Bar_Frame_Height: int) -> CTkFrame:
    global Side_Bar_Icon_top_pady, Side_Bar_Icon_Bottom_pady, Icon_Default_pady, Logo_Height, Logo_width, Icon_Button_Height, Logo_pady
    
    Icon_count = 6
    Icon_Default_pady = 10
    Logo_Height = 0
    Logo_width = 0
    Logo_pady = 0
    
    Icon_Button_Height = Configuration["Buttons"]["Picture_SideBar"]["height"]

    # ------------------------- Local Functions -------------------------#
    def Clear_Frame(Pre_Working_Frame:CTk|CTkFrame) -> None:
        # Find
        for widget in Pre_Working_Frame.winfo_children():
            widget.destroy()
            window.update_idletasks()

    def Show_ChangeMetaData_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=(Side_Bar_Icon_top_pady, Icon_Default_pady), sticky="e")
        time.sleep(0.1)
        Page_Metadata(Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_RenameFile_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        Page_Rename(Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_GEOJSON_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        Page_Geo_Json(Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Information_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        Page_Information(Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Settings_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        Page_Settings(Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Define_Icons_Top_Bottom_indent(Frame_Height: int, Icon_count: int, Icon_Button_Height: int, Icon_Default_pady: int, Logo_height: int, Logo_pady: int) -> list[int, int]:
        Total_Logo_Height = Logo_height + (2 * Logo_pady)
        Total_Icons_Height = Icon_count * (Icon_Button_Height + (2 * Icon_Default_pady))
        Side_Bar_Middle_point = Frame_Height // 2
        Side_Bar_Icon_top_pady = Side_Bar_Middle_point - (Total_Icons_Height // 2)
        Side_Bar_Icon_Bottom_pady = Side_Bar_Middle_point - (Total_Icons_Height // 2) - Total_Logo_Height - Logo_pady

        return Side_Bar_Icon_top_pady, Side_Bar_Icon_Bottom_pady

    # ------------------------- Main Functions -------------------------#
    Active_Window = Elements.Get_Frame(Frame=Side_Bar_Frame, Frame_Size="SideBar_active")

    # Page - Metadata
    Icon_Frame_MetaData = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="replace", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    Icon_Frame_MetaData.configure(command = lambda: Show_ChangeMetaData_Page(Active_Window = Active_Window, Side_Bar_Row=0))    
    Elements.Get_ToolTip(widget=Icon_Frame_MetaData, message="Change metadata photo / video file.", ToolTip_Size="Normal")

    # Page - REname file
    Icon_Frame_Rename_File = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="file-pen", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    Icon_Frame_Rename_File.configure(command = lambda: Show_RenameFile_Page(Active_Window = Active_Window, Side_Bar_Row=1))
    Elements.Get_ToolTip(widget=Icon_Frame_Rename_File, message="Rename File.", ToolTip_Size="Normal")

    # Page - Data
    Icon_Frame_GeoJson = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="map-pin", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    Icon_Frame_GeoJson.configure(command = lambda: Show_GEOJSON_Page(Active_Window = Active_Window, Side_Bar_Row=2))
    Elements.Get_ToolTip(widget=Icon_Frame_GeoJson, message="GEO Json creation.", ToolTip_Size="Normal")

    # Page - Information
    Icon_Frame_Information = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="info", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    Icon_Frame_Information.configure(command = lambda: Show_Information_Page(Active_Window = Active_Window, Side_Bar_Row=3))
    Elements.Get_ToolTip(widget=Icon_Frame_Information, message="Information page.", ToolTip_Size="Normal")

    # Page - Settings
    Icon_Frame_Settings = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="settings", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    Icon_Frame_Settings.configure(command = lambda: Show_Settings_Page(Active_Window = Active_Window, Side_Bar_Row=4))
    Elements.Get_ToolTip(widget=Icon_Frame_Settings, message="Settings page.", ToolTip_Size="Normal")

    # Close Application
    Icon_Frame_Close = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="power", Icon_Size="Side_Bar_close", Button_Size="Picture_SideBar")
    Icon_Frame_Close.configure(command = lambda: window.quit())
    Elements.Get_ToolTip(widget=Icon_Frame_Close, message="Close.", ToolTip_Size="Normal")

    # Define intend
    Side_Bar_Icon_top_pady, Side_Bar_Icon_Bottom_pady = Define_Icons_Top_Bottom_indent(Frame_Height=Side_Bar_Frame_Height, Icon_count=Icon_count, Icon_Button_Height=Icon_Button_Height, Icon_Default_pady=Icon_Default_pady, Logo_height=Logo_Height, Logo_pady=Logo_pady)

    # Build look of Widget
    Active_Window.grid(row=1, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
    Icon_Frame_MetaData.grid(row=0, column=1, padx=(0, 0), pady=(Side_Bar_Icon_top_pady, Icon_Default_pady), sticky="w")
    Icon_Frame_Rename_File.grid(row=1, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_GeoJson.grid(row=2, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_Information.grid(row=3, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_Settings.grid(row=4, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
    Icon_Frame_Close.grid(row=5, column=1, padx=(0, 10), pady=(Icon_Default_pady, Side_Bar_Icon_Bottom_pady), sticky="w")

# ------------------------------------------------------------------------------------------------------------------------------------ Metadata Page ------------------------------------------------------------------------------------------------------------------------------------ #
def Page_Metadata(Frame: CTk|CTkFrame):
    def Prepare_Process_Metadata(Metadata_Widget: CTkFrame) -> None:
        from Libs.Change_metadata import Change_Metadata
        Nested_Folder = Metadata_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkcheckbox"].get()
        Selected_path = Metadata_Widget.children["!ctkframe2"].children["!ctkframe2"].children["!ctkframe3"].children["!ctkentry"].get()
        Nested_Path, File_Count = Nested_Folders(Nested_Folder=Nested_Folder, Selected_path=Selected_path)
        Progress_Bar.configure(determinate_speed=50/File_Count)
        Change_Metadata(Nested_Path=Nested_Path, window=window, Progress_Bar=Progress_Bar)

    # Progress Bar
    Progress_Bar = Elements.Get_ProgressBar(Frame=Frame, orientation="Horizontal", Progress_Size="Download_Process")
    Progress_Bar.set(value=0)
    Progress_Bar.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    # ------------------------- Main Functions -------------------------#
    Frame_MetaData_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_MetaData_Work_Detail_Area.grid_propagate(flag=False)

    Metadata_Widget = Pages.Metadata(Frame=Frame_MetaData_Work_Detail_Area)
    Metadata_Process_var = Metadata_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe"].children["!ctkbutton"]
    Metadata_Process_var.configure(command = lambda: Prepare_Process_Metadata(Metadata_Widget=Metadata_Widget))

    Frame_MetaData_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    Metadata_Widget.grid(row=0, column=0, padx=20, pady=(5, 20), sticky="n")

# ------------------------------------------------------------------------------------------------------------------------------------ Rename Page ------------------------------------------------------------------------------------------------------------------------------------ #
def Page_Rename(Frame: CTk|CTkFrame):
    def Prepare_Process_Rename(Rename_Widget: CTkFrame) -> None:
        from Libs.Rename_Files import Rename_File
        Nested_Folder = Rename_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkcheckbox"].get()
        Selected_path = Rename_Widget.children["!ctkframe2"].children["!ctkframe2"].children["!ctkframe3"].children["!ctkentry"].get()
        Nested_Path, File_Count = Nested_Folders(Nested_Folder=Nested_Folder, Selected_path=Selected_path)
        Progress_Bar.configure(determinate_speed=50/File_Count)
        Rename_File(Nested_Path=Nested_Path, window=window, Progress_Bar=Progress_Bar)

    # Progress Bar
    Progress_Bar = Elements.Get_ProgressBar(Frame=Frame, orientation="Horizontal", Progress_Size="Download_Process")
    Progress_Bar.set(value=0)
    Progress_Bar.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    # ------------------------- Main Functions -------------------------#
    Frame_Rename_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Rename_Work_Detail_Area.grid_propagate(flag=False)

    Rename_Widget = Pages.Rename(Frame=Frame_Rename_Work_Detail_Area)
    Rename_Process_var = Rename_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe"].children["!ctkbutton"]
    Rename_Process_var.configure(command = lambda: Prepare_Process_Rename(Rename_Widget=Rename_Widget))
    
    Frame_Rename_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    Rename_Widget.grid(row=0, column=0, padx=20, pady=(5, 20), sticky="n")

# ------------------------------------------------------------------------------------------------------------------------------------ GeoJson Page ------------------------------------------------------------------------------------------------------------------------------------ #
def Page_Geo_Json(Frame: CTk|CTkFrame):
    def Prepare_Process_GeoJson(GeoJson_Widget: CTkFrame) -> None:
        from Libs.Generate_GEO_json import GEO_Json
        Nested_Folder = GeoJson_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkcheckbox"].get()
        Selected_path = GeoJson_Widget.children["!ctkframe2"].children["!ctkframe2"].children["!ctkframe3"].children["!ctkentry"].get()
        Nested_Path, File_Count = Nested_Folders(Nested_Folder=Nested_Folder, Selected_path=Selected_path)
        Progress_Bar.configure(determinate_speed=50/File_Count)
        GEO_Json(Nested_Path=Nested_Path, window=window, Progress_Bar=Progress_Bar)


    # Progress Bar
    Progress_Bar = Elements.Get_ProgressBar(Frame=Frame, orientation="Horizontal", Progress_Size="Download_Process")
    Progress_Bar.set(value=0)
    Progress_Bar.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    # ------------------------- Main Functions -------------------------#
    Frame_GEOJSON_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_GEOJSON_Work_Detail_Area.grid_propagate(flag=False)

    GeoJson_Widget = Pages.GEOJson(Frame=Frame_GEOJSON_Work_Detail_Area)
    GeoJson_Process_var = GeoJson_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe"].children["!ctkbutton"]
    GeoJson_Process_var.configure(command = lambda: Prepare_Process_GeoJson(GeoJson_Widget=GeoJson_Widget))

    Frame_GEOJSON_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    GeoJson_Widget.grid(row=0, column=0, padx=20, pady=(5, 20), sticky="n")

# ------------------------------------------------------------------------------------------------------------------------------------ Information Page ------------------------------------------------------------------------------------------------------------------------------------ #
def Page_Information(Frame: CTk|CTkFrame):
    Work_Area_Detail_Background = Configuration["Frames"]["Widgets"]["Widget_Frames"]["Scrollable_Frames"]["Triple_size"]["fg_color"]
    
    Work_Area_Detail_Font = Configuration["Labels"]["Main"]["text_color"]

    # ------------------------- Main Functions -------------------------#
    Frame_Information_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Information_Work_Detail_Area.grid_propagate(flag=False)

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
    Frame_Information_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Frame=Frame_Information_Work_Detail_Area, Frame_Size="Triple_size")

    with open("Libs\\GUI\\Information.md", "r", encoding="UTF-8") as file:
        html_markdown=markdown.markdown( file.read())
    file.close()

    Information_html = HTMLLabel(Frame_Information_Scrollable_Area, html=f"{html_markdown}", background=HTML_Background_Color, font="Roboto", fg=HTML_Font_Color)
    Information_html.configure(height=700)

    # Build look of Widget
    Frame_Information_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    Frame_Information_Scrollable_Area.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    Information_html.pack(side="top", fill="both", expand=True, padx=10, pady=10)

def Page_Settings(Frame: CTk|CTkFrame):
    # ------------------------- Main Functions -------------------------#
    Frame_Settings_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Settings_Work_Detail_Area.grid_propagate(flag=False)

    # Tab View
    TabView = Elements.Get_Tab_View(Frame=Frame_Settings_Work_Detail_Area, Tab_size="Normal")
    TabView.pack_propagate(flag=False)
    Tab_Gen = TabView.add("General")
    Tab_Gen.pack_propagate(flag=False)
    TabView.set("General")

    Tab_Gen_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(widget=Tab_Gen_ToolTip_But, message="Application General Setup.", ToolTip_Size="Normal")

    Theme_Widget = Settings_Widgets.Settings_General_Theme(Frame=Tab_Gen, window=window)
    Color_Palette_Widget = Settings_Widgets.Settings_General_Color(Frame=Tab_Gen)

    # Build look of Widget
    Frame_Settings_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    TabView.grid(row=0, column=0, padx=5, pady=15, sticky="n")
    Theme_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Color_Palette_Widget.grid(row=1, column=0, padx=5, pady=5, sticky="nw")


# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Program -------------------------------------------------------------------------------------------------------------------------------------------------- #
class Win(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        super().overrideredirect(True)
        super().title("Time Sheet Downloader")
        super().iconbitmap(bitmap=f"Libs\\GUI\\Icons\\Logo.ico")
        self._offsetx = 0
        self._offsety = 0
        super().bind("<Button-1>",self.click_win)
        super().bind("<B1-Motion>", self.drag_win)

    def drag_win(self,event):
        # Move only when on Side Bar
        if (self._offsetx < SideBar_Width):
            x = super().winfo_pointerx() - self._offsetx
            y = super().winfo_pointery() - self._offsety
            super().geometry(f"+{x}+{y}")
        else:
            pass

    def click_win(self,event):
        self._offsetx = super().winfo_pointerx() - super().winfo_rootx()
        self._offsety = super().winfo_pointery() - super().winfo_rooty()


if __name__ == "__main__":
    window = Win()
    display_width = window.winfo_screenwidth()
    display_height = window.winfo_screenheight()
    Window_Frame_width = 800
    Window_Frame_height = 600
    left_position = int(display_width // 2 - Window_Frame_width // 2)
    top_position = int(display_height // 2 - Window_Frame_height // 2)
    window.geometry(f"{Window_Frame_width}x{Window_Frame_height}+{left_position}+{top_position}")

    # Rounded corners 
    window.config(background="#000001")
    window.attributes("-transparentcolor", "#000001")

    # Base Windows style setup --> always keep normal before change
    customtkinter.set_appearance_mode(mode_string=Theme_Actual)
    pywinstyles.apply_style(window=window, style="normal")
    pywinstyles.apply_style(window=window, style=Win_Style_Actual)

    # ---------------------------------- Content ----------------------------------#
    # Background
    Frame_Background = Elements.Get_Frame(Frame=window, Frame_Size="Background")
    Frame_Background.pack(side="top", fill="none", expand=False)

    # SideBar
    Frame_Side_Bar = Elements.Get_SideBar_Frame(Frame=Frame_Background, Frame_Size="SideBar")
    Frame_Side_Bar.pack(side="left", fill="y", expand=False)

    # Work Area
    Frame_Work_Area = Elements.Get_Frame(Frame=Frame_Background, Frame_Size="Work_Area")
    Frame_Work_Area.pack(side="top", fill="both", expand=False)

    Frame_Header = Elements.Get_Frame(Frame=Frame_Work_Area, Frame_Size="Work_Area_Header")
    Frame_Header.pack_propagate(flag=False)
    Frame_Header.pack(side="top", fill="both", expand=False)

    Frame_Work_Area_Detail = Elements.Get_Frame(Frame=Frame_Work_Area, Frame_Size="Work_Area_Main")
    Frame_Work_Area_Detail.pack_propagate(flag=False)
    Frame_Work_Area_Detail.pack(side="left", fill="none", expand=False)

    Get_Side_Bar(Side_Bar_Frame=Frame_Side_Bar, Side_Bar_Frame_Height=Window_Frame_height)
    Get_Header(Frame=Frame_Header)
    Page_Metadata(Frame=Frame_Work_Area_Detail)

    # run
    window.mainloop()