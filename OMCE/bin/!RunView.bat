@ECHO OFF
"%~d0%~p0OMCE" %1
IF ERRORLEVEL 1 GOTO ERROR
"%~d0%~p0..\viewer\OMCEview" "%~d1%~p1%~n1.ohd"
IF ERRORLEVEL 1 GOTO ERROR
goto end
:ERROR
ECHO ====================== Error! ======================
:wait
pause
:end
