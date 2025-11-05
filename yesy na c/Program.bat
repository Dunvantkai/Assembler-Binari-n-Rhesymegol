@echo off
title Binary to Minecraft Program Code
setlocal enabledelayedexpansion
:RESTART
CLS
echo ================================
echo Binary to Minecraft Program Code
echo ================================
echo.
color 0a
set /p TName=Enter TXT File Name (like "Test.txt"):
if not exist "%TName%" (
    echo File not found!
    pause
    Goto RESTART
)
for %%f in ("%TName%") do set "BaseName=%%~nf"
mkdir %BaseName%
set "Pack=MC_Data\pack.mcmeta"
cd %BaseName%
set "RendCom=%BaseName%_RendCom.txt" 
copy "..\%TName%" "%RendCom%"
for /f "usebackq delims=" %%A in ("%RendCom%") do (
set "line=%%A"
set "line=!line:*:=!"
for /f "delims=:" %%B in ("%%A") do echo %%B >> "Temp.txt"
)
copy "%RendCom%" "%BaseName%.txt"
copy "Temp.txt" "%RendCom%"
del Temp.txt
mkdir my_datapack
copy "..\%Pack%" "my_datapack\pack.mcmeta"
cd my_datapack
mkdir data
cd data
mkdir myfunc
cd myfunc
mkdir function
cd function
echo say Start > runcommands.mcfunction"
set "squ= ~"
set "sot=setblock ~"
set "glass= minecraft:glass"
set "red= minecraft:repeater[facing=west]"
set /a z=2
set /a y=0
set /a x=0
for /f "usebackq delims=" %%A in ("..\..\..\..\%RendCom%") do call :process_line "%%A"
goto END
:process_line
set "line=%~1"
echo Line: !line!
set /a pos=0
:char_loop
set "char=!line:~%pos%,1!"
if not defined char goto :eof

if "!char!"=="0" (
    echo !sot!!x!!squ!!y!!squ!!z!!glass! >> "runcommands.mcfunction"
    set /a y=y - 2
    set /a pos+=1
    if "!y!"=="-16" (
    set /a z=z + 2
    set /a y=0
    if "!z!"=="130" (
    set /a z=2
    set /a x=x - 7
)
)
    goto char_loop
)
if "!char!"=="1" (
    echo !sot!!x!!squ!!y!!squ!!z!!red! >> "runcommands.mcfunction"
    set /a y=y - 2
    set /a pos+=1
    if "!y!"=="-16" (
    set /a z=z + 2
    set /a y=0
    if "!z!"=="130" (
    set /a z=2
    set /a x=x - 7
)
)
    goto char_loop
)
set /a pos+=1
goto char_loop

:END
echo say Finshed >> "runcommands.mcfunction"
echo Done processing.
cd..
cd..
cd..
cd..
cd..
pause
Goto RESTART



