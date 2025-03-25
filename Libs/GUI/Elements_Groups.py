from customtkinter import CTk, CTkFrame, CTkScrollableFrame
from CTkMessagebox import CTkMessagebox

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

def Get_Widget_Frame(Configuration:dict, Frame: CTk|CTkFrame, Name: str, Additional_Text: str, Widget_size: str, Widget_Label_Tooltip: str) -> CTkFrame:
    # Build base Frame for Widget
    Frame_Single_Body = Elements.Get_Widget_Frame_Body(Configuration=Configuration, Frame=Frame, Widget_size=Widget_size)

    Frame_Single_Header = Elements.Get_Widget_Frame_Header(Configuration=Configuration, Frame=Frame_Single_Body, Widget_size=Widget_size)
    
    Header_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header")
    Header_text.configure(text=f"{Name}")

    Header_text_Additional = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header_Additional", Font_Size="Column_Header_Additional")
    Header_text_Additional.configure(text=f"{Additional_Text}")

    Icon_Label_text = Elements.Get_Label_Icon(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header", Icon_Set="lucide", Icon_Name="circle-help", Icon_Size="Question")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Label_text, message=Widget_Label_Tooltip, ToolTip_Size="Normal")

    Frame_Single_Data_Area = Elements.Get_Widget_Frame_Area(Configuration=Configuration, Frame=Frame_Single_Body, Widget_size=Widget_size)

    # Build look of Widget
    Frame_Single_Body.pack(side="top", fill="none", expand=False, padx=0, pady=0)
    Frame_Single_Header.pack(side="top", fill="x", expand=False, padx=7, pady=7)
    Header_text.pack(side="left", fill="x")
    Icon_Label_text.pack(side="left", fill="none", expand=False, padx=1, pady=0)
    Header_text_Additional.pack(side="right", fill="x")
    Frame_Single_Data_Area.pack(side="top", fill="y", expand=True, padx=7, pady=7)

    return Frame_Single_Body

def Get_Widget_Input_row(Settings: dict, Configuration:dict, Frame: CTk|CTkFrame, Field_Frame_Type: str, Label: str, Field_Type: str, Var_Value: int|str|None = None,  Validation: str|None = None) -> CTkFrame:
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

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack_propagate(flag=False)
    Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    if Field_Type == "Input_Normal":
        Field_Normal = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, Frame=Frame_Value, Field_Size="Normal", Validation=Validation)
        Field_Normal.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Password_Normal":
        Field_Normal = Elements.Get_Password_Normal(Configuration=Configuration, Frame=Frame_Value)
        Field_Normal.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Input_Small":
        Field_Small = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, Frame=Frame_Value, Field_Size="Small", Validation=Validation)
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
    else:
        CTkMessagebox(title="Error", message=f"Field type: {Field_Type} not supported.", icon="cancel", fade_in_duration=1)

    return Frame_Area

def Get_Widget_Button_row(Configuration:dict, Frame: CTk|CTkFrame, Field_Frame_Type: str, Buttons_count: int, Button_Size: str) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Value
    Frame_Buttons = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Buttons.pack_propagate(flag=False)
    Frame_Buttons.pack(side="right", fill="x", expand=True, padx=0, pady=0)

    for Button in range(Buttons_count): 
        Button_Normal = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Buttons, Button_Size=Button_Size)
        Button_Normal.pack(side="right", fill="none", expand=False, padx=(10,0))

    return Frame_Area

def Get_Table_Frame(Configuration:dict, Frame: CTk|CTkFrame, Table_Size: str, Table_Values: list|None, Table_Columns: int, Table_Rows: int) -> CTkScrollableFrame:
    # Build only one frame which contain whole Table
    Frame_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame, Frame_Size=Table_Size)
    Frame_Scrollable_Area.pack(side="top", fill="y", expand=True, padx=10, pady=(0,5))

    # Table
    Skip_List_Table = Elements.Get_Table(Configuration=Configuration, Frame=Frame_Scrollable_Area, Table_size=Table_Size, columns=Table_Columns, rows=Table_Rows)
    if Table_Values == None:
        pass
    else:
        Skip_List_Table.configure(values=Table_Values)
    Skip_List_Table.pack(side="top", fill="y", expand=True, padx=10, pady=10)

    return Frame_Scrollable_Area
