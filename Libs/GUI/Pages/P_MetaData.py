# Import Libraries
import os
import threading

import Libs.GUI.Elements as Elements
import Libs.GUI.Widgets.W_All_pages as W_All_pages

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
def Page_Metadata(Settings: dict, Configuration: dict, window: CTk, Frame: CTkFrame):
    def Prepare_Process_Metadata(Metadata_Widget: CTkFrame) -> None:
        import Libs.Change_metadata as Change_metadata
        Nested_Folder = Metadata_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkcheckbox"].get()
        Selected_path = Metadata_Widget.children["!ctkframe2"].children["!ctkframe2"].children["!ctkframe3"].children["!ctkentry"].get()
        if Selected_path == "":
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"No path selected.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            Nested_Path, File_Count = Nested_Folders(Nested_Folder=Nested_Folder, Selected_path=Selected_path)
            Progress_Bar.configure(determinate_speed=50/File_Count)
            Generate_META_thread = threading.Thread(target=Change_metadata.Change_Metadata, args=(Settings, Nested_Path, window, Progress_Bar))
            Generate_META_thread.start()
            Generate_META_thread.join(timeout=0.1) 

    # Progress Bar
    Progress_Bar_Frame = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Status_Line", GUI_Level_ID=1)
    Progress_Bar = Elements.Get_ProgressBar(Configuration=Configuration, Frame=Progress_Bar_Frame, orientation="Horizontal", Progress_Size="Download_Process", GUI_Level_ID=1)
    Progress_Bar.set(value=0)

    # ---------- Tab View ---------- #
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame, Tab_size="Normal", GUI_Level_ID=1)
    TabView.pack_propagate(flag=False)
    Tab_META = TabView.add("MetaData")
    TabView.set("MetaData")
    Tab_PO_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_PO_ToolTip_But, message="Process for to change metadata of pictures and video files.", ToolTip_Size="Normal", GUI_Level_ID=1)

    Frame_META_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_META, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Metadata_Widget = W_All_pages.Metadata(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_META_Column_A, GUI_Level_ID=2)
    Metadata_Process_var = Metadata_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe"].children["!ctkbutton"]
    Metadata_Process_var.configure(command = lambda: Prepare_Process_Metadata(Metadata_Widget=Metadata_Widget))

    Progress_Bar_Frame.pack(side="top", fill="x", expand=False, padx=10, pady=(10, 0))
    Progress_Bar.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))
    Frame_META_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Metadata_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)