
@echo off
set /p name="�t�@�C������l����͂��Ă������� : "
set /p dir="�t�H���_����l����͂��Ă������� : "

python jpg_shuffle.py %name% %dir%
python thumb.py %dir%