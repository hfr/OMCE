@ECHO OFF
rem P1: omc-file
rem P2: ohd-file
rem P3: switch to activate comparison with ref (0|1)
rem P4-Pn pass through OMCE
if [%1]==[] goto start
goto runit
:start
rem
rem ***************************Tests start here
rem
rem format:
rem call %0 <omc-file> <ohd-file> <comp> "Opt1" ... "Optn"
rem         <comp>=1: compare with tref\<ohd-file>
call %0 log_atan log_atan-mcs200 1 "-mcs=200" "-v=1"
call %0 log_atan log_atan-am0 1 "-mcs=0" "-v=1" "-am=0"
call %0 log_atan log_atan-am1 1 "-mcs=0" "-v=1" "-am=1"
call %0 log_atan log_atan-am2 1 "-mcs=0" "-v=1" "-am=2"
call %0 log_atan log_atan-am3 1 "-mcs=0" "-v=1" "-am=3"
call %0 log_atan log_atan-am4 1 "-mcs=0" "-v=1" "-am=4"
call %0 log_atan.1 log_atan-mcs200 1 "-mcs=200" "-v=1"
call %0 log_atan.2 log_atan-mcs200.2 1 "-mcs=200" "-v=1"
call %0 Rectang-U Rectang-U 1 "-mcs=0" "-v=1" "-i=0" "-p1=0.5"
call %0 Stat_funcs Stat_funcs10k 1 "-mcs=20" "-bs=10000"
call %0 Stat_funcs Stat_funcs100k 1 "-mcs=20" "-bs=100000"
call %0 Sum_corr Sum_corr 1 "-p1=0.5"
rem
rem ***************************Tests end here
rem
ECHO "All Tests completed!"
goto wait
:runit
if "%2"=="" goto ERROR
set OMC=%1
set OHD=%2
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
..\bin\OMCE "%OMC%.omc" "-fo=%OHD%" "-seed=1" "-ofd=OMCE_V1_1" %params%
IF ERRORLEVEL 1 GOTO ERROR
if "%REF%"=="1" goto COMPARE
goto end
:COMPARE
..\bin\OMCEcomp %OHD%.ohd .\tref\%OHD%.ohd
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
