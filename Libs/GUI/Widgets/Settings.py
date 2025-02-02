# Import Libraries
import Libs.Defaults_Lists as Defaults_Lists
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

import pywinstyles
import customtkinter
from customtkinter import CTk, CTkFrame, CTkEntry, StringVar, IntVar, BooleanVar, CTkToplevel, CTkOptionMenu, CTkButton
from CTkMessagebox import CTkMessagebox
from CTkTable import CTkTable

# -------------------------------------------------------------------------------------------------------------------------------------------------- Set Defaults -------------------------------------------------------------------------------------------------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Supported_Photo_postfix_list = list(Settings["General"]["Supported_postfix"]["Photos"])
Supported_Video_postfix_list = list(Settings["General"]["Supported_postfix"]["Videos"])

# Appearance
Configuration = Defaults_Lists.Load_Configuration() 
Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]
Theme_List = list(Configuration["Global_Appearance"]["Window"]["Theme_List"])
Win_Style_Actual = Configuration["Global_Appearance"]["Window"]["Style"]
Win_Style_List = list(Configuration["Global_Appearance"]["Window"]["Style_List"])
Accent_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Mode"]
Accent_Color_Mode_List = list(Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_List"])
Accent_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Accent"]["Accent_Color_Manual"]

Hover_Color_Mode = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Mode"]
Hover_Color_Mode_List = list(Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_List"])
Hover_Color_Manual = Configuration["Global_Appearance"]["Window"]["Colors"]["Hover"]["Hover_Color_Manual"]

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
def Settings_General_Theme(Frame: CTk|CTkFrame, window: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Local Functions -------------------------#
    def Appearance_Change_Theme(Theme_Frame_Var: CTkOptionMenu) ->  None:
        customtkinter.set_appearance_mode(mode_string=Theme_Frame_Var)
        Field_Update_Value(Variable=Theme_Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Theme"], Information=Theme_Frame_Var)

    def Appearance_Change_Win_Style(Win_Style_Selected: str, window: CTk|CTkFrame) -> None:
        # Base Windows style setup --> always keep normal before change
        pywinstyles.apply_style(window=window, style="normal")
        pywinstyles.apply_style(window=window, style=Win_Style_Selected)
        Field_Update_Value(Variable=Win_Style_Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Style"], Information=Win_Style_Selected)

    # ------------------------- Main Functions -------------------------#
    Theme_Variable = StringVar(master=Frame, value=Theme_Actual)
    Win_Style_Variable = StringVar(master=Frame, value=Win_Style_Actual)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="General Appearance", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="General Appearance settings.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Theme
    Theme_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Theme", Field_Type="Input_OptionMenu") 
    Theme_Frame_Var = Theme_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Theme_Frame_Var.configure(variable=Theme_Variable)
    Elements.Get_Option_Menu_Advance(attach=Theme_Frame_Var, values=Theme_List, command = lambda Theme_Frame_Var: Appearance_Change_Theme(Theme_Frame_Var=Theme_Frame_Var))

    # Field - Windows Style
    Win_Style_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Window Style", Field_Type="Input_OptionMenu") 
    Win_Style_Frame_Var = Win_Style_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Win_Style_Frame_Var.configure(variable=Win_Style_Variable)
    Elements.Get_Option_Menu_Advance(attach=Win_Style_Frame_Var, values=Win_Style_List, command= lambda Win_Style_Selected: Appearance_Change_Win_Style(Win_Style_Selected=Win_Style_Selected, window=window))

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_General_Color(Frame: CTk|CTkFrame) -> CTkFrame:
    # ------------------------- Local Functions -------------------------#
    def Settings_Disabling_Color_Pickers(Selected_Value: str, Entry_Field: CTkEntry, Picker_Button: CTkButton, Variable: StringVar, Helper: str) -> None:
        if Selected_Value == "Windows":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Accent only
            Field_Update_Value(Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "App Default":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Both
            if Helper == "Accent":
                Field_Update_Value(Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
            elif Helper == "Hover":
                Field_Update_Value(Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "Accent Lighter":
            Entry_Field.configure(state="disabled")
            Picker_Button.configure(state="disabled")
            # Hover only
            Field_Update_Value(Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        elif Selected_Value == "Manual":
            Entry_Field.configure(state="normal")
            Picker_Button.configure(state="normal")
            # Both
            if Helper == "Accent":
                Field_Update_Value(Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Mode"], Information=Selected_Value)
            elif Helper == "Hover":
                Field_Update_Value(Variable=Variable, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Mode"], Information=Selected_Value)
        else:
            CTkMessagebox(title="Error", message="Accent Color Method not allowed", icon="cancel", fade_in_duration=1)

    def Appearance_Pick_Manual_Color(Color_Manual_Frame_Var: CTkEntry, Helper: str) -> None:
        def Quit_Save(Helper: str):
            Defaults_Lists.Information_Update_Settings(File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", f"{Helper}", f"{Helper}_Color_Manual"], Information=Color_Picker_Frame.get())
            Color_Picker_window.destroy()

        def drag_win():
            x = Color_Picker_window.winfo_pointerx() - Color_Picker_window._offsetx
            y = Color_Picker_window.winfo_pointery() - Color_Picker_window._offsety
            Color_Picker_window.geometry(f"+{x}+{y}")

        def click_win():
            Color_Picker_window._offsetx = Color_Picker_window.winfo_pointerx() - Color_Picker_window.winfo_rootx()
            Color_Picker_window._offsety = Color_Picker_window.winfo_pointery() - Color_Picker_window.winfo_rooty()

            
        Color_Picker_window = CTkToplevel()
        #Color_Picker_window.configure(fg_color="#000001")
        Color_Picker_window.title("Color Picker")
        Color_Picker_window.geometry("295x240")
        Color_Picker_window.bind(sequence="<Escape>", func=lambda event: Quit_Save(Helper=Helper))
        #Color_Picker_window.bind(sequence="<Button-1>", func=lambda event:click_win())
        #Color_Picker_window.bind(sequence="<B1-Motion>", func=lambda event:drag_win())
        #Color_Picker_window.overrideredirect(boolean=True)
        Color_Picker_window.iconbitmap(bitmap=f"Libs\\GUI\\Icons\\Logo.ico")
        Color_Picker_window.resizable(width=False, height=False)

        # Rounded corners 
        #Color_Picker_window.config(background="#000001")
        #Color_Picker_window.attributes("-transparentcolor", "#000001")

        Color_Picker_Frame = Elements.Get_Color_Picker(Frame=Color_Picker_window, Color_Manual_Frame_Var=Color_Manual_Frame_Var)

        # Build look of Widget --> must be before inset
        Color_Picker_Frame.pack(padx=0, pady=0) 

    # ------------------------- Main Functions -------------------------#
    Accent_Color_Mode_Variable = StringVar(master=Frame, value=Accent_Color_Mode)
    Hover_Color_Mode_Variable = StringVar(master=Frame, value=Hover_Color_Mode)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Colors", Additional_Text="Applied after restart.", Widget_size="Single_size", Widget_Label_Tooltip="Colors")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Accent Color Mode
    Accent_Color_Mode_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Mode", Field_Type="Input_OptionMenu") 
    Accent_Color_Mode_Frame_Var = Accent_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Accent_Color_Mode_Frame_Var.configure(variable=Accent_Color_Mode_Variable)
    
    # Field - Accent Color Manual
    Accent_Color_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Accent Color Manual", Field_Type="Input_Normal") 
    Accent_Color_Manual_Frame_Var = Accent_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Accent_Color_Manual_Frame_Var.configure(placeholder_text=Accent_Color_Manual, placeholder_text_color="#949A9F")
    Accent_Color_Manual_Frame_Var.bind("<FocusOut>", lambda Entry_value: Field_Update_Value(Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Accent", "Accent_Color_Manual"], Information=Accent_Color_Manual_Frame_Var.get()))

    # Button - Color Picker
    Accent_Color_Picker_Button = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
    Accent_Color_Picker_Button_Var = Accent_Color_Picker_Button.children["!ctkframe"].children["!ctkbutton"]
    Accent_Color_Picker_Button_Var.configure(text="Accent Color Picker", command = lambda :Appearance_Pick_Manual_Color(Color_Manual_Frame_Var=Accent_Color_Manual_Frame_Var, Helper="Accent"))
    Elements.Get_ToolTip(widget=Accent_Color_Picker_Button_Var, message="Select manually Accent color.", ToolTip_Size="Normal")

    # Disabling fields --> Accent_Color_Mode_Variable
    Elements.Get_Option_Menu_Advance(attach=Accent_Color_Mode_Frame_Var, values=Accent_Color_Mode_List, command = lambda Accent_Color_Mode_Frame_Var: Settings_Disabling_Color_Pickers(Selected_Value=Accent_Color_Mode_Frame_Var, Entry_Field=Accent_Color_Manual_Frame_Var, Picker_Button=Accent_Color_Picker_Button_Var, Variable=Accent_Color_Mode_Variable, Helper="Accent"))
    Settings_Disabling_Color_Pickers(Selected_Value=Accent_Color_Mode, Entry_Field=Accent_Color_Manual_Frame_Var, Picker_Button=Accent_Color_Picker_Button_Var, Variable=Accent_Color_Mode_Variable, Helper="Accent")  # Must be here because of initial value

    # Field - Hover Color Mode
    Hover_Color_Mode_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover Color Mode", Field_Type="Input_OptionMenu") 
    Hover_Color_Mode_Frame_Var = Hover_Color_Mode_Frame.children["!ctkframe3"].children["!ctkoptionmenu"]
    Hover_Color_Mode_Frame_Var.configure(variable=Hover_Color_Mode_Variable)

    # Field - Hover Color Manual
    Hover_Color_Manual_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Hover Color Manual", Field_Type="Input_Normal") 
    Hover_Color_Manual_Frame_Var = Hover_Color_Manual_Frame.children["!ctkframe3"].children["!ctkentry"]
    Hover_Color_Manual_Frame_Var.configure(placeholder_text=Hover_Color_Manual, placeholder_text_color="#949A9F")
    Hover_Color_Manual_Frame_Var.bind("<FocusOut>", lambda Entry_value: Field_Update_Value(Variable=None, File_Name="Configuration", JSON_path=["Global_Appearance", "Window", "Colors", "Hover", "Hover_Color_Manual"], Information=Hover_Color_Manual_Frame_Var.get()))

    # Button - Color Picker
    Hover_Color_Picker_Button = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Small") 
    Hover_Color_Picker_Button_Var = Hover_Color_Picker_Button.children["!ctkframe"].children["!ctkbutton"]
    Hover_Color_Picker_Button_Var.configure(text="Hover Color Picker", command = lambda:Appearance_Pick_Manual_Color(Color_Manual_Frame_Var=Hover_Color_Manual_Frame_Var, Helper="Hover"))
    Elements.Get_ToolTip(widget=Hover_Color_Picker_Button_Var, message="Select manually Hover Color.", ToolTip_Size="Normal")

    # Disabling fields --> Accent_Color_Mode_Variable
    Elements.Get_Option_Menu_Advance(attach=Hover_Color_Mode_Frame_Var, values=Hover_Color_Mode_List, command = lambda Hover_Color_Mode_Frame_Var: Settings_Disabling_Color_Pickers(Selected_Value=Hover_Color_Mode_Frame_Var, Entry_Field=Hover_Color_Manual_Frame_Var, Picker_Button=Hover_Color_Picker_Button_Var, Variable=Hover_Color_Mode_Variable, Helper="Hover"))
    Settings_Disabling_Color_Pickers(Selected_Value=Hover_Color_Mode, Entry_Field=Hover_Color_Manual_Frame_Var, Picker_Button=Hover_Color_Picker_Button_Var, Variable=Hover_Color_Mode_Variable, Helper="Hover")   # Must be here because of initial value

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main



def Settings_Supported_Photo(Frame: CTk|CTkFrame) -> CTkFrame:
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
            CTkMessagebox(title="Error", message=f"Dot symbol is not at the beginning of the added text. Please correct.", icon="cancel", fade_in_duration=1)
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
                CTkMessagebox(title="Error", message=f"Postfix is empty please fill it first.", icon="cancel", fade_in_duration=1)

            # Save to Settings.json
            Postfixes = [element for innerList in Frame_Photo_Table_Var.values for element in innerList]
            Postfixes.remove(Header_List)
            Postfixes.sort()
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["General", "Supported_postfix", "Photos"], Information=Postfixes)
        else:
            CTkMessagebox(title="Error", message=f"Postfix is already within list of Photos postfixes.", icon="cancel", fade_in_duration=1)

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
            CTkMessagebox(title="Error", message=f"Dot symbol is not at the beginning of the added text. Please correct.", icon="cancel", fade_in_duration=1)
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
                CTkMessagebox(title="Error", message=f"Postfix not found, please check spelling.", icon="cancel", fade_in_duration=1)
            else:
                pass
            Postfixes = [element for innerList in Frame_Photo_Table_Var.values for element in innerList]
            Postfixes.remove("Photo Formats")
            Postfixes.sort()
            Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["General", "Supported_postfix", "Photos"], Information=Postfixes)
        else:
            CTkMessagebox(title="Error", message=f"Header cannot be deleted.", icon="cancel", fade_in_duration=1)

    def Del_Photo_Postfix_all(Frame_Photo_Table_Var: CTkTable) -> None:
        Table_len = len(Frame_Photo_Table_Var.values)
        for Table_index in range(1, Table_len):
            Frame_Photo_Table_Var.delete_row(index=Table_index)
        Defaults_Lists.Information_Update_Settings(File_Name="Settings", JSON_path=["General", "Supported_postfix", "Photos"], Information=[])

    # ------------------------- Main Functions -------------------------#
    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Photo Postfixes", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="List of supported phots postfixes.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Subject
    Photo_Postfix_Text = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Postfix", Field_Type="Input_Normal") 
    Photo_Postfix_Text_Var = Photo_Postfix_Text.children["!ctkframe3"].children["!ctkentry"]
    Photo_Postfix_Text_Var.configure(placeholder_text="Add postfix")

    # Skip Events Table
    Header_List = ["Photo Formats"]
    Photo_Formats_list = [Header_List]
    for Format in Supported_Photo_postfix_list:
        Photo_Formats_list.append([Format])
        
    Frame_Photo_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Body, Table_Size="Single_size", Table_Values=Photo_Formats_list, Table_Columns=len(Header_List), Table_Rows=len(Photo_Formats_list))
    Frame_Photo_Table_Var = Frame_Photo_Table.children["!ctktable"]
    Frame_Photo_Table_Var.configure(wraplength=440)

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=3, Button_Size="Small") 
    Button_Add_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Add_Var.configure(text="Add", command = lambda:Add_Photo_Postfix(Header_List=Header_List, Photo_Postfix_Text_Var=Photo_Postfix_Text_Var, Frame_Photo_Table_Var=Frame_Photo_Table_Var))
    Elements.Get_ToolTip(widget=Button_Add_Var, message="Add selected postfix to skip list", ToolTip_Size="Normal")

    Button_Del_One_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Del_One_Var.configure(text="Del", command = lambda:Del_Photo_Postfix_one(Photo_Postfix_Text_Var=Photo_Postfix_Text_Var, Frame_Photo_Table_Var=Frame_Photo_Table_Var))
    Elements.Get_ToolTip(widget=Button_Del_One_Var, message="Delete row from table based on input text.", ToolTip_Size="Normal")

    Button_Del_all_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton3"]
    Button_Del_all_Var.configure(text="Del all", command = lambda:Del_Photo_Postfix_all(Frame_Photo_Table_Var=Frame_Photo_Table_Var))
    Elements.Get_ToolTip(widget=Button_Del_all_Var, message="Delete all rows from table.", ToolTip_Size="Normal")


    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

