@echo off
rem *************************************************
rem Registration of .omc and .ohd file extensions
rem Version 1.1.0, 2012-02-16
rem 
rem Author: Ruediger Kessel (ruediger.kessel@gmail.com) 
rem *************************************************
set edit=%SystemRoot%\system32\NOTEPAD.EXE
rem
set dbs=%~d0%~p0double_bs.exe
set RF="%temp%\_OMCE_add_registery_reg_file.reg"
set tmp_file="%temp%\_add_registery_tmp_file.tmp"
set OMCE=%~d0%~p0OMCE
set viewer=%~d0%~p0..\viewer\OMCEview
set RV=%~d0%~p0!runview.bat
set OMC=OMCE_simulation_model
set OHD=OMCE_histogram_data
rem set classroot=HKEY_CLASSES_ROOT
set classroot=HKEY_CURRENT_USER\Software\Classes
rem
"%dbs%" "%OMCE%" > "%tmp_file%"
set /P "OMCE=" < "%tmp_file%"
rem
"%dbs%" "%RV%" > "%tmp_file%"
set /P "RV=" < "%tmp_file%"
rem
"%dbs%" "%edit%" > "%tmp_file%"
set /P "edit=" < "%tmp_file%"
rem
"%dbs%" "%viewer%" > "%tmp_file%"
set /P "viewer=" < "%tmp_file%"
rem
echo Windows Registry Editor Version 5.00 > %RF%
echo. >> %RF%
echo [%classroot%\.ohd] >> %RF%
echo @="%OHD%" >> %RF%
echo. >> %RF%
echo [%classroot%\.omc] >> %RF%
echo @="%OMC%" >> %RF%
echo. >> %RF%
echo [%classroot%\%OMC%] >> %RF%
echo @="" >> %RF%
echo. >> %RF%
echo [%classroot%\%OMC%\shell] >> %RF%
echo @="edit" >> %RF%
echo. >> %RF%
echo [%classroot%\%OMC%\shell\edit] >> %RF%
echo. >> %RF%
echo [%classroot%\%OMC%\shell\edit\command] >> %RF%
echo @="\"%edit%\" \"%%1\"" >> %RF%
echo. >> %RF%
rem echo [%classroot%\%OMC%\shell\open] >> %RF%
rem echo. >> %RF%
rem echo [%classroot%\%OMC%\shell\open\command] >> %RF%
rem echo @="\"%edit%\" \"%%1\"" >> %RF%
rem echo. >> %RF%
echo [%classroot%\%OMC%\shell\Simulate] >> %RF%
echo. >> %RF%
echo [%classroot%\%OMC%\shell\Simulate\command] >> %RF%
echo @="\"%OMCE%\" \"%%1\"" >> %RF%
echo. >> %RF%
echo [%classroot%\%OMC%\shell\Simulate_CS] >> %RF%
echo @="Simulate Client/Server" >> %RF%
echo. >> %RF%
echo [%classroot%\%OMC%\shell\Simulate_CS\command] >> %RF%
echo @="\"%OMCE%client\" \"%%1\"" >> %RF%
echo. >> %RF%
echo [%classroot%\%OMC%\shell\Simulate_View] >> %RF%
echo @="Simulate && View" >> %RF%
echo "Position"="Top" >> %RF%
echo. >> %RF%
echo [%classroot%\%OMC%\shell\Simulate_View\command] >> %RF%
echo @="\"%RV%\" \"%%1\"" >> %RF%
echo. >> %RF%
echo [%classroot%\%OHD%] >> %RF%
echo @="" >> %RF%
echo. >> %RF%
echo [%classroot%\%OHD%\shell] >> %RF%
echo @="view" >> %RF%
echo. >> %RF%
echo [%classroot%\%OHD%\shell\view] >> %RF%
echo @="View Histogram" >> %RF%
echo "Position"="Top" >> %RF%
echo. >> %RF%
echo [%classroot%\%OHD%\shell\view\command] >> %RF%
echo @="\"%viewer%\" \"%%1\"" >> %RF%
echo. >> %RF%
echo [%classroot%\%OHD%\shell\pdf] >> %RF%
echo @="Generate PDF-file" >> %RF%
echo. >> %RF%
echo [%classroot%\%OHD%\shell\pdf\command] >> %RF%
echo @="\"%viewer%\" -pdf=1 \"%%1\"" >> %RF%
echo. >> %RF%
reg import %RF%
del %RF%
del %tmp_file%
:END
pause

