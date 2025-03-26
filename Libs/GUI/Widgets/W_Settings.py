# Import Libraries
import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.Data_Functions as Data_Functions
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.GUI.Elements as Elements

from customtkinter import CTk, CTkFrame, CTkEntry, StringVar, IntVar, BooleanVar, CTkOptionMenu, CTkButton, set_appearance_mode
from CTkTable import CTkTable

# -------------------------------------------------------------------------------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Field_Update_Value(Variable: StringVar|IntVar|BooleanVar|None, File_Name: str, JSON_path: list, Information: int|str|list|dict) -> None:
    # Must be here as local function because 2 operation needs to be executed 
    if Variable is None:
        pass
    elif type(Variable) is None:
        pass
    elif type(Variable) is BooleanVar:
        Information = Information.get()
    else:
        Variable.set(value=Information)
    Defaults_Lists.Information_Update_Settings(File_Name=File_Name, JSON_path=JSON_path, Information=Information)

# -------------------------------------------------------------------------- Tab Appearance --------------------------------------------------------------------------#

def Settings_General_Color(Settings: dict, Configuration: dict|None, window: CTk, Frame: CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    # ---------------------------- Defaults ----------------------------#
    Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]
    Theme_List = list(Configuration["Global_Appearance"]["Window"]["Theme_List"])
    Accent_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Mode"]
    Accent_Color_Mode_List = list(Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_List"])
    Accent_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Manual"]

    Hover_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Mode"]
    Hover_Color_Mode_List = list(Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_List"])
    Hover_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Manual"]

    Theme_Variable = StringVar(master=Frame, value=Theme_Actual)
    Accent_Color_Mode_Variable = StringVar(master=Frame, value=Accent_Color_Mode)
    Hover_Color_Mode_Variable = StringVar(master=Frame, value=Hover_Color_Mode)

    # ------------------------- Local Functions ------------------------#
    def Settings_Disabling_Color_Pickers(Selected_Value: str, Entry_Field: CTkEntry, Picker_Button: CTkButton, Variable: StringVar, Helper: str) -> None:
        if Selected_Value == "Windows":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Accent only
            Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "App Default":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Both
            if Helper == "Accent":
                Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
            elif Helper == "Hover":
                Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "Accent Lighter":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Hover only
            Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "Manual":
            Entry_Field.configure(state="normal")
            Picker_Button.configure(state="normal")
            # Both
            if Helper == "Accent":
                Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
            elif Helper == "Hover":
                Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Accent Color Method not allowed", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    def Appearance_Pick_Manual_Color(Clicked_on: CTkButton, Color_Manual_Frame_Var: CTkEntry, Helper: str, GUI_Level_ID: int|None = None) -> None:
        def Quit_Save(Helper: str):
            Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", f"{Helper}", f"{Helper}_Color_Manual"], Information=Color_Picker_Frame.get())
            Color_Picker_window.destroy()

        Import_window_geometry = (300, 300)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Clicked_on, New_Window_width=Import_window_geometry[0])
        Color_Picker_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Color Picker", max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=True, Always_on_Top=True)
        Color_Picker_window.bind(sequence="<Escape>", func=lambda event: Quit_Save(Helper=Helper))

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Color_Picker_window, Name="", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="", GUI_Level_ID=GUI_Level_ID)
        Frame_Main.configure(bg_color = "#000001")
        Frame_Body = Frame_Main.children["!ctkframe2"]

        Color_Picker_Frame = Elements.Get_Color_Picker(Configuration=Configuration, Frame=Frame_Body, Color_Manual_Frame_Var=Color_Manual_Frame_Var, GUI_Level_ID=GUI_Level_ID)

        # Build look of Widget --> must be before inset
        Color_Picker_Frame.pack(padx=0, pady=0) 

    def Appearance_Change_Theme(Theme_Frame_Var: CTkOptionMenu) ->  None:
        set_appearance_mode(mode_string=Theme_Frame_Var)
        Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=Theme_Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Theme"], Information=Theme_Frame_Var)

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Colors", Additional_Text="SideBar applied after restart.", Widget_size="Single_size", Widget_Label_Tooltip="Colors", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Theme
    Theme_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Theme", Field_Type="Input_OptionMenu") 
    Theme_Frame_Var = Theme_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Theme_Frame_Var.configure(variable=Theme_Variable)
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Theme_Frame_Var, values=Theme_List, command = lambda Theme_Frame_Var: Appearance_Change_Theme(Theme_Frame_Var=Theme_Frame_Var), GUI_Level_ID=GUI_Level_ID)

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent color", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Accent Color Mode
    Accent_Color_Mode_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Mode", Field_Type="Input_OptionMenu") 
    Accent_Color_Mode_Frame_Var = Accent_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Accent_Color_Mode_Frame_Var.configure(variable=Accent_Color_Mode_Variable)
    
    # Field - Accent Color Manual
    Accent_Color_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Manual", Field_Type="Color_Picker") 
    Accent_Color_Manual_Frame_Var = Accent_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Accent_Color_Manual_Frame_Var.configure(placeholder_text=Accent_Color_Manual, placeholder_text_color="#949A9F")
    Accent_Color_Manual_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Manual"], Information=Accent_Color_Manual_Frame_Var.get()))
    Button_Accent_Color_Frame_Var = Accent_Color_Manual_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Button_Accent_Color_Frame_Var.configure(command = lambda: Appearance_Pick_Manual_Color(Clicked_on=Button_Accent_Color_Frame_Var, Color_Manual_Frame_Var=Accent_Color_Manual_Frame_Var, Helper="Accent", GUI_Level_ID=GUI_Level_ID))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Accent_Color_Frame_Var, message="ColorPicker", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Disabling fields --> Accent_Color_Mode_Variable
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Accent_Color_Mode_Frame_Var, values=Accent_Color_Mode_List, command = lambda Accent_Color_Mode_Frame_Var: Settings_Disabling_Color_Pickers(Selected_Value=Accent_Color_Mode_Frame_Var, Entry_Field=Accent_Color_Manual_Frame_Var, Picker_Button=Button_Accent_Color_Frame_Var, Variable=Accent_Color_Mode_Variable, Helper="Accent"), GUI_Level_ID=GUI_Level_ID)
    Settings_Disabling_Color_Pickers(Selected_Value=Accent_Color_Mode, Entry_Field=Accent_Color_Manual_Frame_Var, Picker_Button=Button_Accent_Color_Frame_Var, Variable=Accent_Color_Mode_Variable, Helper="Accent")  # Must be here because of initial value

    # Section Quantities
    Elements_Groups.Get_Widget_Section_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover color", Label_Size="Field_Label" , Font_Size="Section_Separator")

    # Field - Hover Color Mode
    Hover_Color_Mode_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover Color Mode", Field_Type="Input_OptionMenu") 
    Hover_Color_Mode_Frame_Var = Hover_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Hover_Color_Mode_Frame_Var.configure(variable=Hover_Color_Mode_Variable)

    # Field - Hover Color Manual
    Hover_Color_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover Color Manual", Field_Type="Color_Picker") 
    Hover_Color_Manual_Frame_Var = Hover_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Hover_Color_Manual_Frame_Var.configure(placeholder_text=Hover_Color_Manual, placeholder_text_color="#949A9F")
    Hover_Color_Manual_Frame_Var.bind("<FocusOut>", lambda Entry_value: Data_Functions.Save_Value(Settings=None, Configuration=Configuration, Documents=None, window=window, Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Manual"], Information=Hover_Color_Manual_Frame_Var.get()))
    Button_Hover_Color_Frame_Var = Hover_Color_Manual_Frame.children["!ctkframe3"].children["!ctkbutton"]
    Button_Hover_Color_Frame_Var.configure(command = lambda: Appearance_Pick_Manual_Color(Clicked_on=Button_Hover_Color_Frame_Var, Color_Manual_Frame_Var=Hover_Color_Manual_Frame_Var, Helper="Hover", GUI_Level_ID=GUI_Level_ID))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Hover_Color_Frame_Var, message="ColorPicker", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    # Disabling fields --> Hover_Color_Mode_Variable
    Elements.Get_Option_Menu_Advance(Configuration=Configuration, attach=Hover_Color_Mode_Frame_Var, values=Hover_Color_Mode_List, command = lambda Hover_Color_Mode_Frame_Var: Settings_Disabling_Color_Pickers(Selected_Value=Hover_Color_Mode_Frame_Var, Entry_Field=Hover_Color_Manual_Frame_Var, Picker_Button=Button_Hover_Color_Frame_Var, Variable=Hover_Color_Mode_Variable, Helper="Hover"), GUI_Level_ID=GUI_Level_ID)
    Settings_Disabling_Color_Pickers(Selected_Value=Hover_Color_Mode, Entry_Field=Hover_Color_Manual_Frame_Var, Picker_Button=Button_Hover_Color_Frame_Var, Variable=Hover_Color_Mode_Variable, Helper="Hover")   # Must be here because of initial value

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main




def Settings_Supported_Photo(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    Supported_Photo_postfix_list = list(Settings["General"]["Supported_postfix"]["Photos"])

    # ------------------------- Local Functions -------------------------#
    def Add_Photo_Postfix(Header_List: list, Photo_Postfix_Text_Var: CTkEntry, Frame_Photo_Table_Var: CTkTable) -> None:
        Add_flag = True
        Add_text = Photo_Postfix_Text_Var.get()

        Check_List = [element for innerList in Frame_Photo_Table_Var.values for element in innerList]
        Header_List = Header_List[0]

        # Check if . is on right place
        dot_found = Add_text.find(".")
        if dot_found == 0:
            pass
        elif dot_found > 0:
            Add_flag = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Dot symbol is not at the beginning of the added text. Please correct.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            Add_text = "." + Add_text 

        # Not To add same line
        if Add_flag == True:
            for Postfix in Check_List:
                if Postfix == Add_text:
                    Add_flag = False
                else:
                    pass
        else:
            pass

        small_postfix = Add_text.lower()
        big_postfix = Add_text.upper()

        if Add_flag == True:
            if Add_text != "":
                Frame_Photo_Table_Var.add_row(values=[small_postfix])
                Frame_Photo_Table_Var.add_row(values=[big_postfix])
            else:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Postfix is empty please fill it first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

            # Save to Settings.json
            Postfixes = [element for innerList in Frame_Photo_Table_Var.values for element in innerList]
            Postfixes.remove(Header_List)
            Postfixes.sort()
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["General", "Supported_postfix", "Photos"], Information=Postfixes)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Postfix is already within list of Photos postfixes.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    def Del_Photo_Postfix_one(Photo_Postfix_Text_Var: CTkEntry, Frame_Photo_Table_Var: CTkTable) -> None:
        # Find Index
        Deleted_flag = False
        Selected_Postfix = Photo_Postfix_Text_Var.get()

        # Check if . is on right place
        dot_found = Selected_Postfix.find(".")
        if dot_found == 0:
            pass
        elif dot_found > 0:
            Deleted_flag = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Dot symbol is not at the beginning of the added text. Please correct.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            Selected_Postfix = "." + Selected_Postfix 

        if Selected_Postfix != "Photo Formats":
            Table_len = len(Frame_Photo_Table_Var.values)
            for Table_index in range(0, Table_len):
                Table_row_value = Frame_Photo_Table_Var.values[Table_index][0]
                if Selected_Postfix == Table_row_value:
                    Frame_Photo_Table_Var.delete_row(index=Table_index)
                    Deleted_flag = True
                    break
                else:
                    pass
            if Deleted_flag == False:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Postfix not found, please check spelling.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                pass
            Postfixes = [element for innerList in Frame_Photo_Table_Var.values for element in innerList]
            Postfixes.remove("Photo Formats")
            Postfixes.sort()
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["General", "Supported_postfix", "Photos"], Information=Postfixes)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Header cannot be deleted.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    def Del_Photo_Postfix_all(Frame_Photo_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Photo_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Photo_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["General", "Supported_postfix", "Photos"], Information=[])

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Photo Postfixes", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="List of supported phots postfixes.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Subject
    Photo_Postfix_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Postfix", Field_Type="Input_Normal") 
    Photo_Postfix_Text_Var = Photo_Postfix_Text.children["!ctkframe3"].children["!ctkentry"]
    Photo_Postfix_Text_Var.configure(placeholder_text="Add postfix")

    # Skip Events Table
    Header_List = ["Photo Formats"]
    Photo_Formats_list = [Header_List]
    for Format in Supported_Photo_postfix_list:
        Photo_Formats_list.append([Format])
        
    Frame_Photo_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Body, Table_Size="Single_size", Table_Values=Photo_Formats_list, Table_Columns=len(Header_List), Table_Rows=len(Photo_Formats_list), GUI_Level_ID=GUI_Level_ID + 1)
    Frame_Photo_Table_Var = Frame_Photo_Table.children["!ctktable"]
    Frame_Photo_Table_Var.configure(wraplength=440)

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Add_Var.configure(text="Add", command = lambda:Add_Photo_Postfix(Header_List=Header_List, Photo_Postfix_Text_Var=Photo_Postfix_Text_Var, Frame_Photo_Table_Var=Frame_Photo_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Add_Var, message="Add selected postfix to skip list", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Del_One_Var.configure(text="Del", command = lambda:Del_Photo_Postfix_one(Photo_Postfix_Text_Var=Photo_Postfix_Text_Var, Frame_Photo_Table_Var=Frame_Photo_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Del_One_Var, message="Delete row from table based on input text.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Del_all_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_Del_all_Var.configure(text="Del all", command = lambda:Del_Photo_Postfix_all(Frame_Photo_Table_Var=Frame_Photo_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Del_all_Var, message="Delete all rows from table.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)


    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Supported_Video(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> CTkFrame:
    Supported_Video_postfix_list = list(Settings["General"]["Supported_postfix"]["Videos"])
    # ------------------------- Local Functions -------------------------#
    def Add_Video_Postfix(Header_List: list, Video_Postfix_Text_Var: CTkEntry, Frame_Video_Table_Var: CTkTable) -> None:
        Add_flag = True
        Add_text = Video_Postfix_Text_Var.get()

        Check_List = [element for innerList in Frame_Video_Table_Var.values for element in innerList]
        Header_List = Header_List[0]

        # Check if . is on right place
        dot_found = Add_text.find(".")
        if dot_found == 0:
            pass
        elif dot_found > 0:
            Add_flag = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Dot symbol is not at the beginning of the added text. Please correct.", icon="cancel", fade_in_duration=1, GUI_Level_ID=GUI_Level_ID)
        else:
            Add_text = "." + Add_text 

        # Not To add same line
        if Add_flag == True:
            for Postfix in Check_List:
                if Postfix == Add_text:
                    Add_flag = False
                else:
                    pass
        else:
            pass

        small_postfix = Add_text.lower()
        big_postfix = Add_text.upper()

        if Add_flag == True:
            if Add_text != "":
                Frame_Video_Table_Var.add_row(values=[small_postfix])
                Frame_Video_Table_Var.add_row(values=[big_postfix])
            else:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Postfix is empty please fill it first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=GUI_Level_ID)

            # Save to Settings.json
            Postfixes = [element for innerList in Frame_Video_Table_Var.values for element in innerList]
            Postfixes.remove(Header_List)
            Postfixes.sort()
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["General", "Supported_postfix", "Videos"], Information=Postfixes)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Postfix is already within list of Videos postfixes.", icon="cancel", fade_in_duration=1, GUI_Level_ID=GUI_Level_ID)

    def Del_Video_Postfix_one(Video_Postfix_Text_Var: CTkEntry, Frame_Video_Table_Var: CTkTable) -> None:
        # Find Index
        Deleted_flag = False
        Selected_Postfix = Video_Postfix_Text_Var.get()

        # Check if . is on right place
        dot_found = Selected_Postfix.find(".")
        if dot_found == 0:
            pass
        elif dot_found > 0:
            Deleted_flag = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Dot symbol is not at the beginning of the added text. Please correct.", icon="cancel", fade_in_duration=1, GUI_Level_ID=GUI_Level_ID)
        else:
            Selected_Postfix = "." + Selected_Postfix 

        if Selected_Postfix != "Video Formats":
            Table_len = len(Frame_Video_Table_Var.values)
            for Table_index in range(0, Table_len):
                Table_row_value = Frame_Video_Table_Var.values[Table_index][0]
                if Selected_Postfix == Table_row_value:
                    Frame_Video_Table_Var.delete_row(index=Table_index)
                    Deleted_flag = True
                    break
                else:
                    pass
            if Deleted_flag == False:
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Postfix not found, please check spelling.", icon="cancel", fade_in_duration=1, GUI_Level_ID=GUI_Level_ID)
            else:
                pass
            Postfixes = [element for innerList in Frame_Video_Table_Var.values for element in innerList]
            Postfixes.remove("Video Formats")
            Postfixes.sort()
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["General", "Supported_postfix", "Videos"], Information=Postfixes)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Header cannot be deleted.", icon="cancel", fade_in_duration=1, GUI_Level_ID=GUI_Level_ID)

    def Del_Video_Postfix_all(Frame_Video_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Video_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Video_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["General", "Supported_postfix", "Videos"], Information=[])

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Frame, Name="Video Postfixes", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="List of supported phots postfixes.", GUI_Level_ID=GUI_Level_ID)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Subject
    Video_Postfix_Text = Elements_Groups.Get_Widget_Input_row(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Postfix", Field_Type="Input_Normal") 
    Video_Postfix_Text_Var = Video_Postfix_Text.children["!ctkframe3"].children["!ctkentry"]
    Video_Postfix_Text_Var.configure(placeholder_text="Add postfix")

    # Skip Events Table
    Header_List = ["Video Formats"]
    Video_Formats_list = [Header_List]
    for Format in Supported_Video_postfix_list:
        Video_Formats_list.append([Format])
        
    Frame_Video_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Body, Table_Size="Single_size", Table_Values=Video_Formats_list, Table_Columns=len(Header_List), Table_Rows=len(Video_Formats_list), GUI_Level_ID=GUI_Level_ID + 1)
    Frame_Video_Table_Var = Frame_Video_Table.children["!ctktable"]
    Frame_Video_Table_Var.configure(wraplength=440)

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Add_Var.configure(text="Add", command = lambda:Add_Video_Postfix(Header_List=Header_List, Video_Postfix_Text_Var=Video_Postfix_Text_Var, Frame_Video_Table_Var=Frame_Video_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Add_Var, message="Add selected postfix to skip list", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Del_One_Var.configure(text="Del", command = lambda:Del_Video_Postfix_one(Video_Postfix_Text_Var=Video_Postfix_Text_Var, Frame_Video_Table_Var=Frame_Video_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Del_One_Var, message="Delete row from table based on input text.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Button_Del_all_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_Del_all_Var.configure(text="Del all", command = lambda:Del_Video_Postfix_all(Frame_Video_Table_Var=Frame_Video_Table_Var))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Del_all_Var, message="Delete all rows from table.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)


    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

