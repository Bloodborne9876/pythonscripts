
@echo off
set /p name="�t�@�C������l����͂��Ă������� : "
set /p dir="�t�H���_����l����͂��Ă������� : "
set /p shuffle="�V���b�t������ꍇ = y : "

:: ���΃p�X���g���Ĉꎞ�I�Ɉړ��i���̏ꍇ��`%script_dir%`�̐e�f�B���N�g���j
set parent = %dir%..

python deleteMeta.py %name% %dir% %shuffle"
python thumb.py %dir%
CreatePDF\CreatePDF.exe %dir% %name%
"C:\ProgramData\chocolatey\tools\7z.exe" a %dir%_%name%.zip %dir%