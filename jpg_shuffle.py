import os
import sys
from PIL import Image
import random

def remove_png_metadata_and_rename(folder_path, prefix):
    # 指定したフォルダ内のファイルを取得
    file_list = os.listdir(folder_path)

    random.shuffle(file_list)

    # ファイル名のカウンター
    counter = 1
    
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        # ファイル名をリネームする
        new_file_name = f"{prefix}_{counter:03}.jpg"
        counter += 1
        os.rename(file_path, os.path.join(folder_path , new_file_name)) 

# ユーザーから任意の文字列を入力
#prefix = input("名前を入力してください: ")
# prefix = sys.argv[1]

prefix = "bronya"

# ユーザーからフォルダパスを入力
#folder_path = input("フォルダのパスを入力してください: ")
# folder_path = sys.argv[2]

folder_path = r"C:\イラスト関係\成果\販売\20230816\ブローニャとイチャラブエッチイラスト集 - コピー"

# フォルダの存在チェック
if not os.path.isdir(folder_path):
    print("指定したフォルダが存在しません。")
else:
    remove_png_metadata_and_rename(folder_path, prefix)