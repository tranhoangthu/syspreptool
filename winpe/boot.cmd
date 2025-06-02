@echo off
cd /d "%~dp0"
del %~dp0\bcd_backup\BCD
bcdedit /export %~dp0\bcd_backup\BCD
rem attrib -s -h -r %~dp0\bcd_backup\BCD
tbwinpe.exe /bootwim %~dp0\winpe.wim /quiet /force
exit