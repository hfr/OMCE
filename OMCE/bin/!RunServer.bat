@ECHO OFF
"%~d0%~p0OMCEserver" --IMPORTS=..\Examples\imports
IF ERRORLEVEL 1 GOTO ERROR
goto end
:ERROR
ECHO ====================== Error! ======================
:wait
pause
:end
