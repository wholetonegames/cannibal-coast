@echo off

REM cd assets
REM IF EXIST "*ArmatureAction*" DEL "*ArmatureAction*" /s
REM IF EXIST "*Tpose*" DEL "*Tpose*" /s
REM IF EXIST "*00*" DEL "*00*" /s
REM cd ..

:: convert *.egg into *.egg.bam
for %%f in (./assets/*.egg) do (
    echo %%~nf
    Rem must be *.egg.bam, otherwise fails
    egg2bam -ps rel -o "./assets/%%~nf.egg.bam" "./assets/%%~nf.egg"
)

multify -c -f assets.mf -v assets &:: package all files into a *.mf

python y_md5_check.py &:: get *.mf md5 into a *.txt

@echo off
setlocal
:PROMPT
SET /P AREYOUSURE=Do you want to build this project (Y/N)?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

echo Building project...
python setup.py build_apps &:: build apps needs requirements.txt
pause

:END
endlocal
