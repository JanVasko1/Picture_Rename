# Import Libraries
import os

from customtkinter import CTk, deactivate_automatic_dpi_awareness, get_appearance_mode, set_appearance_mode

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Data_Functions as Data_Functions

import Libs.GUI.Pages.P_Header as P_Header
import Libs.GUI.Pages.P_Side_Bar as P_Side_Bar
import Libs.GUI.Pages.P_Side_Bar as P_Side_Bar

# ------------------------------------------------------------------------------------------------------------------------------------ Local Functions ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Current_Theme() -> str:
    Current_Theme = get_appearance_mode()
    return Current_Theme

# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Program -------------------------------------------------------------------------------------------------------------------------------------------------- #
class Win(CTk):
    def __init__(self):
        super().__init__()
        super().overrideredirect(True)
        super().title("HQ Testing Tool")
        super().iconbitmap(bitmap=Data_Functions.Absolute_path(relative_path=f"Libs\\GUI\\Icons\\Logo.ico"))

        display_width = self.winfo_screenwidth()
        display_height = self.winfo_screenheight()
        Window_Frame_width = 660
        Window_Frame_height = 450
        left_position = int(display_width // 2 - Window_Frame_width // 2)
        top_position = int(display_height // 2 - Window_Frame_height // 2)
        self.geometry(f"{Window_Frame_width}x{Window_Frame_height}+{left_position}+{top_position}")

        # Rounded corners 
        self.config(background="#000001")
        self.attributes("-transparentcolor", "#000001")

        self._offsetx = 0
        self._offsety = 0
        super().bind("<Button-1>",self.click_win)
        super().bind("<B1-Motion>", self.drag_win)

    def drag_win(self, event):
        # Move only when on Side Bar
        if (self._offsetx < SideBar_Width):
            x = super().winfo_pointerx() - self._offsetx
            y = super().winfo_pointery() - self._offsety
            super().geometry(f"+{x}+{y}")
        else:
            pass

    def click_win(self, event):
        self._offsetx = super().winfo_pointerx() - super().winfo_rootx()
        self._offsety = super().winfo_pointery() - super().winfo_rooty()


if __name__ == "__main__":
    window = Win()
    deactivate_automatic_dpi_awareness()
    Settings = Defaults_Lists.Load_Settings()
    Configuration = Defaults_Lists.Load_Configuration() 

    # Base Windows style setup --> always keep normal before change
    Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]
    SideBar_Width = Configuration["Frames"]["Page_Frames"]["SideBar"]["width"]
    set_appearance_mode(mode_string=Theme_Actual)

    # ---------------------------------- Content ----------------------------------#
    # Background
    Frame_Background = Elements.Get_Frame(Configuration=Configuration, Frame=window, Frame_Size="Background", GUI_Level_ID=0)
    Frame_Background.pack(side="top", fill="none", expand=False)

    # SideBar
    Frame_Side_Bar = Elements.Get_SideBar_Frame(Configuration=Configuration, Frame=Frame_Background, Frame_Size="SideBar")
    Frame_Side_Bar.pack(side="left", fill="y", expand=False)

    # Work Area
    Frame_Work_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Background, Frame_Size="Work_Area", GUI_Level_ID=0)
    Frame_Work_Area.pack(side="top", fill="both", expand=False)

    Frame_Header = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Work_Area, Frame_Size="Header", GUI_Level_ID=0)
    Frame_Header.pack_propagate(flag=False)
    Frame_Header.pack(side="top", fill="both", expand=False)

    Frame_Work_Area_Main = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Work_Area, Frame_Size="Work_Area_Main", GUI_Level_ID=0)
    Frame_Work_Area_Main.pack_propagate(flag=False)
    Frame_Work_Area_Main.pack(side="left", fill="none", expand=False)

    P_Header.Get_Header(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Header)
    SideBar = P_Side_Bar.SidebarApp(Side_Bar_Frame=Frame_Side_Bar, Settings=Settings, Configuration=Configuration, window=window, Frame_Work_Area_Main=Frame_Work_Area_Main)
    # run
    window.mainloop()