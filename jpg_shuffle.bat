
@echo off
set /p name="ファイル名を値を入力してください : "
set /p dir="フォルダ名を値を入力してください : "

python jpg_shuffle.py %name% %dir%
python thumb.py %dir%