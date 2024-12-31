@echo off
setlocal

REM ユーザーにフォルダパスを入力させる
set /p "TARGET_DIR=解凍するフォルダのパスを入力してください: "

REM 7zipのパスを指定
set "SEVEN_ZIP_PATH=C:\Program Files\7-Zip\7z.exe"

REM フォルダ内のすべてのzipファイルを解凍
for %%i in ("%TARGET_DIR%\*.zip") do (
    "%SEVEN_ZIP_PATH%" x "%%i" -o"%TARGET_DIR%\%%~ni"
)

REM フォルダ一覧をmatome.txtに出力
tree "%TARGET_DIR%" /F > "%TARGET_DIR%\matome.txt"

endlocal
@echo on
