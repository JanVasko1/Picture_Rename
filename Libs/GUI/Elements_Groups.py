from customtkinter import CTk, CTkFrame, CTkScrollableFrame

import Libs.GUI.Elements as Elements


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

