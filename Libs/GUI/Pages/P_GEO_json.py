# Import Libraries
import Libs.GUI.Elements as Elements
import Libs.GUI.Widgets.W_All_pages as W_All_pages

from customtkinter import CTk, CTkFrame

# -------------------------------------------------------------------------- Main Functions -------------------------------------------------------------------------- #
def Page_Geo_Json(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame):
    # Progress Bar
    Progress_Bar_Frame = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Status_Line", GUI_Level_ID=1)
    Progress_Bar = Elements.Get_ProgressBar(Configuration=Configuration, Frame=Progress_Bar_Frame, orientation="Horizontal", Progress_Size="Download_Process", GUI_Level_ID=1)
    Progress_Bar.set(value=0)

    # ---------- Tab View ---------- #
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame, Tab_size="Normal", GUI_Level_ID=1)
    TabView.pack_propagate(flag=False)
    Tab_GEO = TabView.add("GEO JSON")
    TabView.set("GEO JSON")
    Tab_PO_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PO_ToolTip_But, message="Process for GEO Json file preparation.", ToolTip_Size="Normal", GUI_Level_ID=1)

    Frame_GEO_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_GEO, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_GEO_Column_A.pack_propagate(flag=False)

    Progress_Bar_Frame.pack(side="top", fill="x", expand=False, padx=10, pady=(10, 0))
    Progress_Bar.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))
    Frame_GEO_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    # Widgets
    GEOJson_Widget = W_All_pages.GEOJson_new(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_GEO_Column_A, Progress_Bar=Progress_Bar, GUI_Level_ID=2)
    GEOJson_Widget.Show()   