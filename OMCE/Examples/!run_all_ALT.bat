@ECHO OFF
if "%1"=="" goto start
goto runit
:start
for %%f in (S02.xml S03.xml S04.xml S05_1.xml S05_2.xml S06.xml S07.xml) do call !run_all_ALT.bat %%f
ECHO "All examples completed!"
goto wait
:runit
..\bin\OMCE %1 -info=0 -ap=0.95 -ad=1 -mcs=100 -k=2 -fi=1 -pdf=1 -ofd=ALT -vfd=ALT -seed=1 -de=0 -hc=100 -hp=0.999 -hf=1.1 -pa=1.0
IF ERRORLEVEL 1 GOTO ERROR
comp %1.sta .\ref\%1.sta <_n.txt
ECHO n
IF ERRORLEVEL 1 GOTO ERROR
ECHO Delete Output %1.sta
del %1.sta
goto end
:ERROR
ECHO ====================== Error! ======================
:wait
pause
:end
