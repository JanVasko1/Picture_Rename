# Define path
$path =  "C:\Users\CZ011845\AppData\Local\Programs\Python\Python311\Scripts\"

# Upgrade PIP itself
python.exe -m pip install --upgrade pip

# Project Library
Invoke-Expression $($path+"pip install --upgrade tqdm")
Invoke-Expression $($path+"pip install --upgrade windows-metadata")
Invoke-Expression $($path+"pip install --upgrade pandas")
Invoke-Expression $($path+"pip install --upgrade lat-lon-parser")