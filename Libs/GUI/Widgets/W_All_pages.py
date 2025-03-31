# Import Libraries
import Libs.GUI.Elements_Groups as Elements_Groups
from Libs.GUI.Widgets.Widgets_Class import WidgetFrame, WidgetRow_CheckBox, WidgetRow_Input_Normal
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

def Metadata_new(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # Widget
    Metadata_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Metadata", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Change Date Take / Media Created date and time according to file name.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Nested_Folder_Variable = BooleanVar(master=Frame, value=False)
    Nested_Folders_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Metadata_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Label="Nested Folders", Variable=Nested_Folder_Variable)
    Metadata_Path_row = WidgetRow_Input_Normal(Settings=Settings, Configuration=Configuration, master=Metadata_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Label="Path", placeholder_text="Folder path.")
    Metadata_Widget.Add_row(Rows=[Nested_Folders_Row, Metadata_Path_row])

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Metadata_Widget.Body_Frame, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Normal") 
    Button_Process_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Process_Var.configure(text="Process")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Process_Var, message="Change MetaData of files in folder/s.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    return Metadata_Widget

def Rename_new(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # Widget
    Rename_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Rename", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Change Date Take / Media Created date and time according to file name.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Nested_Folder_Variable = BooleanVar(master=Frame, value=False)
    Nested_Folders_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=Rename_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Label="Nested Folders", Variable=Nested_Folder_Variable)
    Rename_Path_Row = WidgetRow_Input_Normal(Settings=Settings, Configuration=Configuration, master=Rename_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Label="Path", placeholder_text="Folder path.")
    Rename_Widget.Add_row(Rows=[Nested_Folders_Row, Rename_Path_Row])

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=Rename_Widget.Body_Frame, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Normal") 
    Button_Process_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Process_Var.configure(text="Process")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Process_Var, message="Change File names in folder/s.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    return Rename_Widget


def GEOJson_new(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame, GUI_Level_ID: int|None = None) -> WidgetFrame:
    # Widget
    GEOJson_Widget = WidgetFrame(Configuration=Configuration, Frame=Frame, Name="Geo json", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Change Date Take / Media Created date and time according to file name.", GUI_Level_ID=GUI_Level_ID)

    # Fields
    Nested_Folder_Variable = BooleanVar(master=Frame, value=False)
    Nested_Folders_Row = WidgetRow_CheckBox(Settings=Settings, Configuration=Configuration, master=GEOJson_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Label="Nested Folders", Variable=Nested_Folder_Variable)
    File_Name_Row = WidgetRow_Input_Normal(Settings=Settings, Configuration=Configuration, master=GEOJson_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Label="File Name", placeholder_text="Folder path.")
    Export_Path_Row = WidgetRow_Input_Normal(Settings=Settings, Configuration=Configuration, master=GEOJson_Widget.Body_Frame, window=window, Field_Frame_Type="Single_Column" , Label="Path", placeholder_text="Folder path.")
    GEOJson_Widget.Add_row(Rows=[Nested_Folders_Row, File_Name_Row, Export_Path_Row])

    # Buttons
    Button_Frame = Elements_Groups.Get_Widget_Button_row(Configuration=Configuration, Frame=GEOJson_Widget.Body_Frame, Field_Frame_Type="Single_Column" , Buttons_count=1, Button_Size="Normal") 
    Button_Process_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Process_Var.configure(text="Process")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Process_Var, message="Create geojson file.", ToolTip_Size="Normal", GUI_Level_ID=GUI_Level_ID)

    return GEOJson_Widget
