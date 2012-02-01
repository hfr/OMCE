@ECHO OFF
rem P1: ohd-file
rem P2: pdf-file
rem P3: switch to activate comparison with ref (0|1)
rem P4-Pn pass through Viewer
if [%1]==[] goto start
goto runit
:start
rem
rem ***************************Tests start here
rem
rem format:
rem call %0 <ohd-file> <pdf-file> <comp> "Opt1" ... "Optn"
rem         <comp>=1: compare with pref\<pdf-file>
rem
call %0 tref\Stat_funcs10k Stat_funcs10k.0 0
call %0 tref\Stat_funcs10k Stat_funcs10k.1 0 "-sym=X_1,X_2"
call %0 tref\Stat_funcs10k Stat_funcs10k.2 0 "-sym=X_1" "-ttl=Rectangular Distribution" "-xl=X-Axis" "-yl=Y-Axis"
rem
rem ***************************Tests end here
rem
ECHO "All Tests completed!"
goto wait
:runit
if [%2]==[] goto ERROR
set OHD=%1
set PDF=%2
set REF=%3
shift
shift
shift
set params=%1
:loop
shift
if [%1]==[] goto afterloop
set params=%params% %1
goto loop
:afterloop
..\viewer\OMCEview "%OHD%.ohd" "-fo=%PDF%.pdf" "-pdf=1" %params%
IF ERRORLEVEL 1 GOTO ERROR
if "%REF%"=="1" goto COMPARE
goto end
:COMPARE
comp %PDF%.pdf .\pref\%PDF%.pdf <_n.txt
ECHO n
IF ERRORLEVEL 1 GOTO ERROR
:DELETE
ECHO Delete Output %OHD%.ohd
del %OHD%.ohd
goto end
:ERROR
ECHO ====================== Error! ======================
:wait
pause
:end
