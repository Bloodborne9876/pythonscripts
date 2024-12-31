
@echo off
set /p name="ファイル名を値を入力してください : "
set /p dir="フォルダ名を値を入力してください : "
set /p shuffle="シャッフルする場合 = y : "

:: 相対パスを使って一時的に移動（この場合は`%script_dir%`の親ディレクトリ）
set parent = %dir%..

python deleteMeta.py %name% %dir% %shuffle"
python thumb.py %dir%
CreatePDF\CreatePDF.exe %dir% %name%
"C:\ProgramData\chocolatey\tools\7z.exe" a %dir%_%name%.zip %dir%