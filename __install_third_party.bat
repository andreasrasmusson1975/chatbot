REM Install script for the application

REM Install tesseract
powershell -ExecutionPolicy Bypass -File .\installation_scripts\install_vc_redist.ps1
REM Install python 3.10.0
powershell -ExecutionPolicy Bypass -File .\installation_scripts\install_python.ps1
REM Install tesseract
powershell -ExecutionPolicy Bypass -File .\installation_scripts\install_tesseract.ps1





