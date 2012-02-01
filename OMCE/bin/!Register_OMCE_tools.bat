@echo off
set edit=%SystemRoot%\system32\NOTEPAD.EXE
rem
set dbs=%~d0%~p0double_bs.exe
set RF="%~d0%~p0_add_registery.reg"
set tmp="%~d0%~p0_add_registery.tmp"
set OMCE=%~d0%~p0OMCE
set viewer=%~d0%~p0..\viewer\OMCEview
set RV=%~d0%~p0!runview.bat
set OMC=OMCE_simulation_model
set OHD=OMCE_histogram_data
rem
"%dbs%" "%OMCE%" > %tmp%
for /f "usebackq" %%P in (%tmp%) do (set OMCE=%%P)
rem
"%dbs%" "%RV%" > %tmp%
for /f "usebackq" %%P in (%tmp%) do (set RV=%%P)
rem
"%dbs%" "%edit%" > %tmp%
for /f "usebackq" %%P in (%tmp%) do (set edit=%%P)
rem
"%dbs%" "%viewer%" > %tmp%
for /f "usebackq" %%P in (%tmp%) do (set viewer=%%P)
rem
echo Windows Registry Editor Version 5.00 > %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\.ohd] >> %RF%
echo @="%OHD%" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\.omc] >> %RF%
echo @="%OMC%" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OMC%] >> %RF%
echo @="" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OMC%\shell] >> %RF%
echo @="edit" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OMC%\shell\edit] >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OMC%\shell\edit\command] >> %RF%
echo @="%edit% \"%%1\"" >> %RF%
echo. >> %RF%
rem echo [HKEY_CLASSES_ROOT\%OMC%\shell\open] >> %RF%
rem echo. >> %RF%
rem echo [HKEY_CLASSES_ROOT\%OMC%\shell\open\command] >> %RF%
rem echo @="\"%edit%\" \"%%1\"" >> %RF%
rem echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OMC%\shell\Simulate] >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OMC%\shell\Simulate\command] >> %RF%
echo @="\"%OMCE%\" \"%%1\"" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OMC%\shell\Simulate_CS] >> %RF%
echo @="Simulate Client/Server" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OMC%\shell\Simulate_CS\command] >> %RF%
echo @="\"%OMCE%client\" \"%%1\"" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OMC%\shell\Simulate_View] >> %RF%
echo @="Simulate && View" >> %RF%
echo "Position"="Top" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OMC%\shell\Simulate_View\command] >> %RF%
echo @="\"%RV%\" \"%%1\"" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OHD%] >> %RF%
echo @="" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OHD%\shell] >> %RF%
echo @="view" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OHD%\shell\view] >> %RF%
echo @="View Histogram" >> %RF%
echo "Position"="Top" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OHD%\shell\view\command] >> %RF%
echo @="%viewer% \"%%1\"" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OHD%\shell\pdf] >> %RF%
echo @="Generate PDF-file" >> %RF%
echo. >> %RF%
echo [HKEY_CLASSES_ROOT\%OHD%\shell\pdf\command] >> %RF%
echo @="%viewer% -pdf=1 \"%%1\"" >> %RF%
echo. >> %RF%
reg import %RF%
del %RF%
del %tmp%
goto end
:ERR1
ECHO FINDSTR not available!
goto end
:END
