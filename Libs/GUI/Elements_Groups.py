from customtkinter import CTk, CTkFrame, CTkScrollableFrame, CTkToplevel

import Libs.GUI.Elements as Elements
import Libs.Data_Functions as Data_Functions

def Get_Widget_Frame(Configuration:dict, Frame: CTkFrame, Name: str, Additional_Text: str, Widget_size: str, Widget_Label_Tooltip: str, GUI_Level_ID: int|None = None) -> CTkFrame:
    # Build base Frame for Widget
    Frame_Single_Body = Elements.Get_Widget_Frame_Body(Configuration=Configuration, Frame=Frame, Widget_size=Widget_size, GUI_Level_ID=GUI_Level_ID)

    Frame_Single_Header = Elements.Get_Widget_Frame_Header(Configuration=Configuration, Frame=Frame_Single_Body, Widget_size=Widget_size)
    
    Header_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header")
    Header_text.configure(text=f"{Name}")

    Header_text_Additional = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header_Additional", Font_Size="Column_Header_Additional")
    Header_text_Additional.configure(text=f"{Additional_Text}")

    if Widget_Label_Tooltip == "":
        pass
    else:
        Icon_Label_text = Elements.Get_Label_Icon(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header", Icon_Name="circle-help", Icon_Size="Question")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Label_text, message=Widget_Label_Tooltip, ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    Frame_Single_Data_Area = Elements.Get_Widget_Frame_Area(Configuration=Configuration, Frame=Frame_Single_Body, Widget_size=Widget_size)

    # Build look of Widget
    Frame_Single_Body.pack(side="top", fill="none", expand=False, padx=0, pady=0)
    Frame_Single_Header.pack(side="top", fill="x", expand=False, padx=7, pady=7)
    Header_text.pack(side="left", fill="x")
    if Widget_Label_Tooltip == "":
        pass
    else:
        Icon_Label_text.pack(side="left", fill="none", expand=False, padx=1, pady=0)
    Header_text_Additional.pack(side="right", fill="x")
    Frame_Single_Data_Area.pack(side="top", fill="y", expand=True, padx=7, pady=7)

    return Frame_Single_Body

def Get_Widget_Section_row(Configuration:dict, Frame: CTkFrame, Field_Frame_Type: str, Label: str, Label_Size: str, Font_Size: str) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Area, Label_Size=Label_Size, Font_Size=Font_Size)
    Label_text.configure(text=f"{Label}")
    Label_text.pack(side="right", fill="none", expand=False, padx=(50, 0), pady=5)

    return Frame_Area

def Get_Widget_Input_row(Settings: dict, Configuration:dict, window: CTk, Frame: CTkFrame, Field_Frame_Type: str, Label: str, Field_Type: str, Var_Value: int|str|None = None,  Validation: str|None = None, Field_ToolTip: list|None = None) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"{Label}:")
    Label_text.pack(side="right", fill="none")
    if type(Field_ToolTip) == list:
        Elements.Get_ToolTip(Configuration=Configuration, widget=Label_text, message=Field_ToolTip[0], ToolTip_Size="Normal", GUI_Level_ID=Field_ToolTip[1])
    else:
        pass

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack_propagate(flag=False)
    Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    if Field_Type == "Input_Normal":
        Field_Normal = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Value, Field_Size="Normal", Validation=Validation)
        Field_Normal.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Password_Normal":
        Field_Normal = Elements.Get_Password_Normal(Configuration=Configuration, Frame=Frame_Value)
        Field_Normal.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Input_Small":
        Field_Small = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Value, Field_Size="Small", Validation=Validation)
        Frame_Area.configure(width=300)
        Field_Small.pack(side="left", fill="none")
    elif Field_Type == "Input_RadioButton":
        RadioButton = Elements.Get_RadioButton_Normal(Configuration=Configuration, Frame=Frame_Value, Var_Value=Var_Value)
        RadioButton.pack(side="left", fill="none")
    elif Field_Type == "Input_OptionMenu":
        Input_OptionMenu = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Value)
        Input_OptionMenu.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Input_CheckBox":
        Input_Check_Box = Elements.Get_CheckBox(Configuration=Configuration, Frame=Frame_Value)
        Input_Check_Box.pack(side="left", fill="x", expand=True)
    elif (Field_Type == "Date_Picker") or (Field_Type == "Color_Picker"):
        Field_Normal = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Value, Field_Size="Normal", Validation=Validation)
        if Field_Type == "Date_Picker":
            Button_Drop_Down = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Value, Icon_Name="calendar-days", Icon_Size="Entry_DropDown", Button_Size="Tiny")
        elif Field_Type == "Color_Picker":
            Button_Drop_Down = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Value, Icon_Name="paintbrush", Icon_Size="Entry_DropDown", Button_Size="Tiny")
        else:
            pass
        Field_Normal.configure(width = Field_Normal._current_width - Button_Drop_Down._current_width)
        Field_Normal.pack(side="left", fill="x", expand=True)
        Button_Drop_Down.pack(side="left", fill="none", expand=True)
    else:
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Field type: {Field_Type} not supported.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    return Frame_Area

def Get_Widget_Button_row(Configuration:dict, Frame: CTkFrame, Field_Frame_Type: str, Buttons_count: int, Button_Size: str) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Value
    Frame_Buttons = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Buttons.pack_propagate(flag=False)
    Frame_Buttons.pack(side="right", fill="x", expand=True, padx=0, pady=0)

    for Button in range(Buttons_count): 
        Button_Normal = Elements.Get_Button_Text(Configuration=Configuration, Frame=Frame_Buttons, Button_Size=Button_Size)
        Button_Normal.pack(side="right", fill="none", expand=False, padx=(10,0))

    return Frame_Area

def Get_Table_Frame(Configuration:dict, Frame: CTk|CTkFrame, Table_Size: str, Table_Values: list|None, Table_Columns: int, Table_Rows: int, GUI_Level_ID: int|None = None) -> CTkScrollableFrame:
    # Build only one frame which contain whole Table
    Frame_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame, Frame_Size=Table_Size, GUI_Level_ID=GUI_Level_ID)
    Frame_Scrollable_Area.pack(side="top", fill="y", expand=True, padx=10, pady=(0,5))

    # Table
    Skip_List_Table = Elements.Get_Table(Configuration=Configuration, Frame=Frame_Scrollable_Area, Table_size=Table_Size, columns=Table_Columns, rows=Table_Rows, GUI_Level_ID=GUI_Level_ID)
    if Table_Values == None:
        pass
    else:
        Skip_List_Table.configure(values=Table_Values)
    Skip_List_Table.pack(side="top", fill="y", expand=True, padx=10, pady=10)

    return Frame_Scrollable_Area

def Get_Pop_up_window(Configuration:dict, title: str, max_width: int, max_height: int, Top_middle_point: list, Fixed: bool, Always_on_Top: bool) -> CTkToplevel:
    def drag_win():
        x = Pop_Up_Window.winfo_pointerx() - Pop_Up_Window._offsetx
        y = Pop_Up_Window.winfo_pointery() - Pop_Up_Window._offsety
        Pop_Up_Window.geometry(f"+{x}+{y}")

    def click_win():
        Pop_Up_Window._offsetx = Pop_Up_Window.winfo_pointerx() - Pop_Up_Window.winfo_rootx()
        Pop_Up_Window._offsety = Pop_Up_Window.winfo_pointery() - Pop_Up_Window.winfo_rooty()

    # TopUp Window
    Pop_Up_Window = CTkToplevel()
    Pop_Up_Window.configure(fg_color="#000001")
    Pop_Up_Window.title(title)

    left_position = Top_middle_point[0]
    top_position = Top_middle_point[1]
    Pop_Up_Window.geometry("+%d+%d" % (left_position, top_position))
    Pop_Up_Window.maxsize(width=max_width, height=max_height)

    #Pop_Up_Window.geometry(f"{width}x{height}")
    Pop_Up_Window.bind(sequence="<Escape>", func=lambda event: Pop_Up_Window.destroy())
    Pop_Up_Window.attributes("-topmost", Always_on_Top)
    if Fixed == False:
        Pop_Up_Window.bind(sequence="<Button-1>", func=lambda event:click_win())
        Pop_Up_Window.bind(sequence="<B1-Motion>", func=lambda event:drag_win())
    else:
        pass
    Pop_Up_Window.overrideredirect(boolean=True)
    Pop_Up_Window.iconbitmap(bitmap=Data_Functions.Absolute_path(relative_path=f"Libs\\GUI\\Icons\\Logo.ico"))
    Pop_Up_Window.resizable(width=False, height=False)

    # Rounded corners 
    Pop_Up_Window.config(background="#000001")
    Pop_Up_Window.attributes("-transparentcolor", "#000001")

    return Pop_Up_Window
