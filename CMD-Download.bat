@echo off
echo CIVIT Image Downloader Loop
echo Type "exit" as ID to quit.
:loop
set /p ID=Enter model_id: 
if /I "%ID%"=="exit" goto end

python civit_image_downloader.py --timeout 5 --quality 2 --redownload 1 --mode 2 --no_sort --model_id %ID%

echo.
echo ---- Completed for ID: %ID% ----
echo.
goto loop

:end
echo Exiting...
pause