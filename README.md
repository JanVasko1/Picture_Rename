# Photo Rename / change metadata
This program was developed to make TimeSheet administration easier and harmonize it over all fo Konica Minolta employee.

# Setup
### <span style="color:blue;">Installation</span>
1. Install [Python 3.11.2](https://www.python.org/downloads/release/python-3112/) - recomended or higher
2. Run `Installation_libs.ps1` code (reflect correct path to your python installation)
3. Update:
    1. `Photo_Rename_Files.bat` to reflect correct path to your python installation
    2. `Photo_Chage_metadata.bat` to reflect correct path to your python installation
    3. `Photo_Generate_GEO_json.bat` to reflect correct path to your python installation

### <span style="color:blue;">Process</span></span>
![Process](https://github.com/JanVasko1/Pictu/blob/main/images/Process.png?raw=true
 "Overal process")

- red --> manual steps
- green --> automatic steps

### <span style="color:blue;">Outlook Callendar - Pre-Requisit</span>
There must be special Events created for each day and special behavior must be followed
- `Work Start` --> tells program when is particular working day starts
    - must be 0 minutes duration 
    - Event Subject is defined in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Start_End_Events / Start`)

- `Work End` --> tells program when is particular working day ends
    - must be 0 minutes duration 
    - Event Subject is defined in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Start_End_Events / End`)

- `Lunch` --> tells program when is particular lunch is 
    - Event Subject is defined in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events/ Special_Events / Lunch / Search_Text`)

- `Category` --> is considerate as “Project” from TimeSheets
    - Must be manually updated when needed from TimeSheet from Shareponit
    - If event is marke by category, then whole program counts with it base on setup in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Project / Method`)

> [!TIP]
> ![Category ](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Category.png?raw=true
 "Category")

- `Templates` --> is considerate to contain “Activity” from Timesheets
    - If event has line: “Activity: Activity”, then whole program counts with it base on setup in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Activity / Method`)

> [!TIP]
> ![Tempaltes ](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Templates.png?raw=true
 "Tempaltes")

> [!TIP]
> ![Event body](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Activity.png?raw=true
 "Event body")


### <span style="color:blue;">Main Setup File `Settings.json`</span>
- `Calendar`
    - `Working Hours` - specify working hours for each day in week
        [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`General / Calendar / ... / Work_Hours`)
    - `Vacation Hours` - specify vacation hours for each day in week when all day Vacation is used
        [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`General / Calendar / ... / Vacation`)
- `Personal Information` - contains your KM Code and full name (Code is used as Personnel number in TimeSheets)

# Downloader
This first part of program is used to download events from calendar

### <span style="color:blue;">Sharepoint</span>
- Program prompts at the beginning if you want to directly download missing days from Sharepoint (online) and analyze missing days

- Setup data must be correctly maintained to have a correct link to proper TimeSheet Excel on Sharepoint 
    - `Authentication`
        - first attempt is required to put password (hashed and stored)
        - It is required to reenter it time to time

    - `Link` 
        - link to the TimeSheet Excel on the KM sharepoint site

### <span style="color:blue;">Manual Input</span>
- Manual input you have to select form and to dates
- `Format`: 
    - YYYY-MM-DD
    - Special sign: “t” = Today

### <span style="color:blue;">Methods</span>
- `Outlook_classic` --> download events from Outlook (classic) application installed on Windows, there is draback, must be only one account in Outlook client
- `API_Exchange_server` --> download events directly from Exchange Server for defined User

> [!CAUTION]
> API_Exchange_server --> Under Developemnt

# Events Handlers
Here are steps which process the downloaded date into the shape suitable for TimeSheets

### <span style="color:blue;">Overnights</span>
- This handler splits Events if they go over midnight
- This doesn´t require any setup as it is programmed.
- Videly used for multiday Vacation, travel-time ...

> [!TIP]
> ![Overnight Events](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/OverNight.png?raw=true
 "Overnight Events")

### <span style="color:blue;">Fill Empty: General</span>
- This is for filling empty space in the calendar between events where it react on `coverage` palced by each record (sum must be equal to 100%)
- Works only between “Work - Start” and “Work - End” events (only at the time when I'm at work)
- It select one from the list from [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Empty / General / ...`) and use then coverage [%] to simulate real usage

> [!TIP]
> ![Fill Empty General](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Empty_General.png?raw=true
 "Fill Empty General")

> [!TIP]
> ![Empty General setup](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Empty_General_setup.png?raw=true
 "Empty General setup")

> [!CAUTION]
> Coverage split --> Under Developemnt

### <span style="color:blue;">Fill Empty: Scheduled</span>
- This agenda is used for regular record planning like if I have Administration and Emails done after lunch at 11:30 – 12:00 of the week day
- Agenda can have multiple setup (only one used on picture)
- If in the period is another Event then this scheduled is not filled

> [!TIP]
> ![Empty Schedules setup](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Empty_Schedules_setup.png?raw=true
 "Empty Schedules setup")

### <span style="color:blue;">Location</span>
- Currently set for all events `Office`

### <span style="color:blue;">Lunch</span>
- lunch is special event which should be skipped from Timesheet
- Also is used to split  parallel meeting which is planned over the lunch (like whole day meetings)
- Search text can be modified in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Special_Events / Lunch / ...`) 

> [!TIP]
> ![Lunch Event](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Lunch.png?raw=true
 "!unch")

### <span style="color:blue;">Skip Events</span>
- This is the list of evens which should be skiped from registering them into TimeSheets
- Can be extended in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Skip / ...`) 

- Text from `Settings.json` is compared with Event subject and if a part of subject contain text from (`Event_Handler / Events / Skip / ...`) then is recognized and event is not considerate for Time Sheets

### <span style="color:blue;">Parralel Events</span>
- This handler helps to process Events which might be in parallelly set in Calendar
- has 2 modes only one can be selected in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Parralel_Events / Divide_Method`):
    - `Divide` --> will divide Parralle Events based on logic (eveerytime takes as separator the begining of Event)
    - `Keep_Parralel` --> will keep both parallel events for TimeSheet
    
> [!TIP]
> Divide:
>
> ![Parralel 1](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Parralel1.png?raw=true
 "Divide")

> [!TIP]
> Divide and Use Shorter:
>
> ![Parralel 2](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Parralel2.png?raw=true
 "Divide and use shorter")

> [!TIP]
> Keep parralel:
>
> ![Parralel Keep](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Parralel_keep.png?raw=true
 "Parralel Keep")

- has 2 methods for Events start at the same time:
    - `Use_Shorter` --> will consider the shortest event as first pick
    - `Use_Longer` --> will consider the shortest event as first pick

> [!CAUTION]
> Use_Longer --> Under development (now is defaulty used Use_Shorter)

### <span style="color:blue;">AutoFiller</span>
- This special function to help automatically fill: `Project`, `Activity`, `Location`
- It can be enhanced in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Auto_Filler / Details / ...`)
- If there is empty text --> then is not used
- As [`Skip Events`](https://github.com/JanVasko1/KM-Calendar_Reading?tab=readme-ov-file#skip-events) program is based on searching text in the Event Subject to apply mapping

### <span style="color:blue;">Vacation</span>
- Handler of Vacation to register correctly 
    - `All Day` --> takes hours from [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
  and apply them into TimeSheet
    - `Half Day` --> uses only the time defined by Event
- If the text appeared (defined by OKBase) in the event Subject [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Special_Events / Vacation / ...`) 

- All Events within the Vacation period and Working hours are deleted

### <span style="color:blue;">Home Office</span>
- Currently is not maintaining anything as HomeOffice is not used as special Location of TimeSheets

# Summary
Is defined to print statistic and all records of selected period to provide better overview of Time spent:
    - Total Statistics
    - Project Statistics
    - Activity Statistics
    - WeekDay Statistics
    - Week Statistics

# Uploader
> [!CAUTION]
> Under Developemnt as whole functionality

# Export csv
The processed result is automatically exported to the defined path and automatically opened by Windows in the format ready to “Copy + Paste” to TimeSheet on Sharepoint

# Footer
The Settings.json is real file of Jan Vasko usage