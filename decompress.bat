@echo off
setlocal

REM ���[�U�[�Ƀt�H���_�p�X����͂�����
set /p "TARGET_DIR=�𓀂���t�H���_�̃p�X����͂��Ă�������: "

REM 7zip�̃p�X���w��
set "SEVEN_ZIP_PATH=C:\Program Files\7-Zip\7z.exe"

REM �t�H���_���̂��ׂĂ�zip�t�@�C������
for %%i in ("%TARGET_DIR%\*.zip") do (
    "%SEVEN_ZIP_PATH%" x "%%i" -o"%TARGET_DIR%\%%~ni"
)

REM �t�H���_�ꗗ��matome.txt�ɏo��
tree "%TARGET_DIR%" /F > "%TARGET_DIR%\matome.txt"

endlocal
@echo on
