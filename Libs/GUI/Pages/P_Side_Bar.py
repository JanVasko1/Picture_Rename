# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Pages.P_GEO_json as P_GEO_json
import Libs.GUI.Pages.P_Information as P_Information
import Libs.GUI.Pages.P_MetaData as P_MetaData
import Libs.GUI.Pages.P_Rename as P_Rename
import Libs.GUI.Pages.P_Settings as P_Settings

import Libs.GUI.Elements as Elements

class SidebarApp:
    def __init__(self, Side_Bar_Frame: CTkFrame, Settings: dict, Configuration: dict, window: CTk, Frame_Work_Area_Main: CTkFrame):
        self.Side_Bar_Frame = Side_Bar_Frame
        self.Settings = Settings
        self.Configuration = Configuration
        self.window = window
        self.Frame_Work_Area_Main = Frame_Work_Area_Main

        # Application
        self.Application = Defaults_Lists.Load_Application()
        self.Program_Version = self.Application["Application"]["Version"]
            
        # Add buttons to the sidebar
        self.names = ["MetaData", 
                        "Rename", 
                        "GEOJson", 
                        "Information", 
                        "Settings", 
                        "Close"]
        
        self.icons = ["replace", 
                      "file-pen", 
                      "map-pin", 
                      "info", 
                      "settings", 
                      "power"]
        
        self.messages = ["Change metadata photo / video file.", 
                        "Rename File.", 
                        "GEO Json creation.", 
                        "Information page.", 
                        "Application settings page.", 
                        "Close application."]
        
        # Icons
        self.Icon_Default_pady = 10
        self.Side_Bar_Top_pady = 65
        self.Side_Bar_Bottom_pady = 35
        self.Icon_count = len(self.names)

        # Active button tracker
        self.active_button = "MetaData"
        
        # Build SideBar
        self.create_sidebar_buttons()
        self.create_Application_version()
        self.Show_ChangeMetaData_Page()

    def create_sidebar_buttons(self):
        self.Active_Window = 0
        self.buttons = []
        for button_index, button_name in enumerate(self.names):
            if button_name == "Close":
                # TurnOff wit red color
                button = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Icon_Name=self.icons[button_index], Icon_Size="Side_Bar_close", Button_Size="Picture_Transparent")
            elif  button_name == self.active_button:
                # Initiate Active Button
                button = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Icon_Name=self.icons[button_index], Icon_Size="Side_Bar_Active", Button_Size="Picture_Transparent")
            else:
                button = Elements.Get_Button_Icon(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Icon_Name=self.icons[button_index], Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
            button.configure(command = self.create_command(button_index=button_index, button_name=button_name))
            Elements.Get_ToolTip(Configuration=self.Configuration, widget=button, message=self.messages[button_index], ToolTip_Size="Normal", GUI_Level_ID=0)

            # Place button 
            if button_index == 0:
                # First Icon
                button.pack(side="top", fill="none", expand=False, padx=5, pady=(self.Side_Bar_Top_pady, self.Icon_Default_pady))
            elif (button_index > 0) and (button_index < self.Icon_count - 1):
                # Middle Icons
                button.pack(side="top", fill="none", expand=False, padx=5, pady=self.Icon_Default_pady)
            else:
                # Last Icon
                button.pack(side="top", fill="none", expand=False, padx=5, pady=(self.Icon_Default_pady, self.Side_Bar_Bottom_pady))
            self.buttons.append(button)

    def create_Application_version(self):
        Program_Version_text = Elements.Get_Label(Configuration=self.Configuration, Frame=self.Side_Bar_Frame, Label_Size="Field_Label", Font_Size="Field_Label")
        Program_Version_text.configure(text=f"{self.Program_Version}")
        Program_Version_text.pack(side="top", fill="none", expand=False, padx=5, pady=(0, 10))


    def create_command(self, button_index, button_name):
        """Return a command function for the given page."""
        def command():
            self.change_page(button_index=button_index, button_name=button_name)
        return command

    def change_page(self, button_index, button_name):
        # Reset the color of all buttons
        for button_index_intern, button in enumerate(self.buttons):
            if button_index_intern < self.Icon_count - 1:
                button.configure(image=Elements.Get_CTk_Icon(Configuration=self.Configuration, Icon_Name=self.icons[button_index_intern], Icon_Size="Side_Bar_regular"))

        # Mark Active button
        self.buttons[button_index].configure(image=Elements.Get_CTk_Icon(Configuration=self.Configuration, Icon_Name=self.icons[button_index], Icon_Size="Side_Bar_Active"))

        if button_name == "MetaData":
            self.Show_ChangeMetaData_Page()
        elif button_name == "Rename":
            self.Show_RenameFile_Page()
        elif button_name == "GEOJson":
            self.Show_GEOJSON_Page()
        elif button_name == "Information":
            self.Show_Information_Page()
        elif button_name == "Settings":
            self.Show_Settings_Page()
        elif button_name == "Close":
            self.Show_Close_Page()
        else:
            pass

    def Clear_Frame(self, Pre_Working_Frame: CTkFrame) -> None:
        # Find
        for widget in Pre_Working_Frame.winfo_children():
            widget.destroy()

    def Show_ChangeMetaData_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_MetaData.Page_Metadata(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)

    def Show_RenameFile_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Rename.Page_Rename(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)

    def Show_GEOJSON_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_GEO_json.Page_Geo_Json(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)

    def Show_Information_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Information.Page_Information(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)

    def Show_Settings_Page(self) -> None:
        self.Clear_Frame(Pre_Working_Frame=self.Frame_Work_Area_Main)
        P_Settings.Page_Settings(Settings=self.Settings, Configuration=self.Configuration, window=self.window, Frame=self.Frame_Work_Area_Main)

    def Show_Close_Page(self) -> None:
        self.window.quit()