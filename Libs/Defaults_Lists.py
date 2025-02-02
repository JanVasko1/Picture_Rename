# Import Libraries
import json

from CTkMessagebox import CTkMessagebox

def Load_Settings() -> dict:
    File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
    Settings = json.load(fp=File)
    File.close()
    return Settings

def Load_Configuration() -> dict:
    File = open(file=f"Libs\\GUI\\Configuration.json", mode="r", encoding="UTF-8", errors="ignore")
    Configuration = json.load(fp=File)
    File.close()
    return Configuration

def Information_Update_Settings(File_Name: str, JSON_path: list, Information: int|str|list|dict) -> None:
    def update_value(File_dict: dict, JSON_path: list, Information: int|str|list|dict) -> None:
        # Must be in local function !!!!
        for key in JSON_path[:-1]:
            File_dict = File_dict[key]
        File_dict[JSON_path[-1]] = Information

    try:
        # Load File
        if File_Name == "Settings":
            File_dict = Load_Settings()
        elif File_Name == "Configuration":
            File_dict = Load_Configuration()
        else:
            pass

        # Update values
        update_value(File_dict=File_dict, JSON_path=JSON_path, Information=Information)
        
        # Save in Settings.json
        if File_Name == "Settings":
            with open(f"Libs\\Settings.json", mode="wt", encoding="UTF-8", errors="ignore") as file:
                json.dump(obj=File_dict, fp=file, indent=4, default=str, ensure_ascii=False)
            file.close()
        elif File_Name == "Configuration":
            with open(f"Libs\\GUI\\Configuration.json", mode="wt", encoding="UTF-8", errors="ignore") as file:
                json.dump(obj=File_dict, fp=file, indent=4, default=str, ensure_ascii=False)
            file.close()
        else:
            pass
            
    except Exception as Error:
        CTkMessagebox(title="Error", message=f"Not possible to update {Information} into Field: {JSON_path} of {File_Name}", icon="cancel", fade_in_duration=1)