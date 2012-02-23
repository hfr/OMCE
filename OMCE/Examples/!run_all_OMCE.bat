@ECHO OFF
if [%1]==[] goto start
goto runit
:start
rem set opt=/run
for %%f in (MM5point.omc S02.omc S03.omc S04.omc S05_1.omc S05_2.omc S06.omc S07.omc TypeB.omc) do call %0 %%f %opt%
for %%f in (JCGM_101_9.5.omc JCGM_101_9.2.2.omc JCGM_101_9.2.3.omc JCGM_101_9.2.4.omc JCGM_101_9.3.omc JCGM_101_9.4.3.omc JCGM_101_9.4.omc) do call %0 %%f %opt%
for %%f in (log_atan.omc Pythagoras.omc Discrete_Normal.omc Import_Normal.omc Normal.omc Cuberoot.omc) do call %0 %%f %opt%
ECHO "All examples completed!"
goto wait
:runit
if [%2]==[] goto mcs
if [%2]==[/cmp] goto cmp
if [%2]==[/run] goto mcs
if [%2]==[/del] goto delete
goto errorp2
:mcs
"%~d0%~p0..\bin\OMCE" "%~d0%~p0%1" -ap=0.95 -ad=1 -mcs=100 -k=2 -fi=0 -pdf=1 -ofd=OMCE_V1_1 -vfd=OMCE -seed=1 -de=0 -hc=100 -hp=0.999 -hf=1.1 -pa=1.0 -imp=..\Examples\imports
IF ERRORLEVEL 1 GOTO ERROR
:cmp
"%~d0%~p0..\bin\OMCEcomp" "%~d0%~p0%1.ohd" "%~d0%~p0ref\%1.ohd" 
IF ERRORLEVEL 1 GOTO ERROR
if [%2]==[] goto delete
goto end
:delete
ECHO Delete Output %1.ohd
del "%~d0%~p0%1.ohd"
goto end
:ERRORP2
ECHO Parameter 2 unknown (%2)
:ERROR
ECHO ====================== Error! ======================
:wait
pause
:end
