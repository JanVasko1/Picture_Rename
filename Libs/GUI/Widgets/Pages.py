# Import Libraries
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

from customtkinter import CTk, CTkFrame, CTkEntry, BooleanVar


# -------------------------------------------------------------------------------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def Entry_field_Insert(Field: CTkEntry, Value: str|int) -> None:
    if type(Value) == str:
        if Value != "":
            Field.delete(first_index=0, last_index=1000)
            Field.insert(index=0, string=Value)
        else:
            pass
    elif type(Value) == int:
        if Value > 0:
            Field.delete(first_index=0, last_index=1000)
            Field.insert(index=0, string=Value)
        else:
            pass
    else:
        pass

def Metadata(Frame: CTk|CTkFrame) -> CTkFrame:
    Nested_Folder_Variable = BooleanVar(master=Frame, value=False)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Metadata", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Change Date Take / Media Created date and time according to file name.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Nested_Folders_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Nested Folders", Field_Type="Input_CheckBox") 
    Nested_Folders_Frame_Var = Nested_Folders_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Nested_Folders_Frame_Var.configure(variable=Nested_Folder_Variable, text="")

    # Field - Search Text
    Metadata_Path = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Path", Field_Type="Input_Normal") 
    Metadata_Path_Var = Metadata_Path.children["!ctkframe3"].children["!ctkentry"]
    Metadata_Path_Var.configure(placeholder_text="Folder path.")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Normal") 
    Button_Process_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Process_Var.configure(text="Process")
    Elements.Get_ToolTip(widget=Button_Process_Var, message="Change MetaData of files in folder/s.", ToolTip_Size="Normal")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def Rename(Frame: CTk|CTkFrame) -> CTkFrame:
    Rename_Nested_Folder_Variable = BooleanVar(master=Frame, value=False)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Rename", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Change names in path from Date_Take of Media Created.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Nested_Folders_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Nested Folders", Field_Type="Input_CheckBox") 
    Nested_Folders_Frame_Var = Nested_Folders_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Nested_Folders_Frame_Var.configure(variable=Rename_Nested_Folder_Variable, text="")

    # Field - Search Text
    Rename_Path = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Path", Field_Type="Input_Normal") 
    Rename_Path_Var = Rename_Path.children["!ctkframe3"].children["!ctkentry"]
    Rename_Path_Var.configure(placeholder_text="Folder path.")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Normal") 
    Button_Process_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Process_Var.configure(text="Process")
    Elements.Get_ToolTip(widget=Button_Process_Var, message="Change File names in folder/s.", ToolTip_Size="Normal")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main

def GEOJson(Frame: CTk|CTkFrame) -> CTkFrame:
    Rename_Nested_Folder_Variable = BooleanVar(master=Frame, value=False)

    # Frame - General
    Frame_Main = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Geo json", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Create geo_json file from media files in path.")
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Field - Use
    Nested_Folders_Frame = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Nested Folders", Field_Type="Input_CheckBox") 
    Nested_Folders_Frame_Var = Nested_Folders_Frame.children["!ctkframe3"].children["!ctkcheckbox"]
    Nested_Folders_Frame_Var.configure(variable=Rename_Nested_Folder_Variable, text="")

    # Field - Search Text
    GEOJson_Path = Elements_Groups.Get_Widget_Input_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Label="Path", Field_Type="Input_Normal") 
    GEOJson_Path_Var = GEOJson_Path.children["!ctkframe3"].children["!ctkentry"]
    GEOJson_Path_Var.configure(placeholder_text="Folder path.")

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Frame=Frame_Body, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Normal") 
    Button_Process_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Process_Var.configure(text="Process")
    Elements.Get_ToolTip(widget=Button_Process_Var, message="Change File names in folder/s.", ToolTip_Size="Normal")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)

    return Frame_Main