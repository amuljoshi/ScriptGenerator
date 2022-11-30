@echo off
title Starting RunMe.bat
:: See the title at the top
echo Changing the directory containing Python File...
cd "Folder where the python file is present in local drive"
echo Changed directory successfully
title Running the Python script file
echo Running the Python file to generate scripts...
"Location of python.exe file" AAA.py
echo End of script!!
title End of RunMe.bat
Pause
