import os
import sys
from PIL import Image
import random

def remove_png_metadata_and_rename(folder_path, prefix , shuffle : bool = False ):
    # 指定したフォルダ内のファイルを取得
    file_list = os.listdir(folder_path)

    if(shuffle == True):
        print("シャッフル開始")
        random.shuffle(file_list)

    # ファイル名のカウンター
    counter = 1
    
    for file_name in file_list:
        # 拡張子がPNGの場合のみ処理する
        if file_name.lower().endswith('.png'):
            file_path = os.path.join(folder_path, file_name)
            try:
                # 画像を開いてメタデータを削除する
                image = Image.open(file_path)
                data = list(image.getdata())
                image_without_metadata = Image.new(image.mode, image.size)
                image_without_metadata.putdata(data)
                
                # 元のファイルを削除して、メタデータが削除された画像を保存する
                os.remove(file_path)

                # ファイル名をリネームする
                # new_file_name = f"{prefix}_{counter:03}.png"
                # new_file_path = os.path.join(folder_path, new_file_name)
                # image_without_metadata.save(new_file_path)
                image_without_metadata.save(file_path)
                counter += 1

                print(f"メタデータが削除されました：{file_path}")
            except Exception as e:
                print(f"メタデータの削除とファイル名の変更中にエラーが発生しました: {file_name}")
                print(e)

# ユーザーから任意の文字列を入力
prefix = sys.argv[1]
# prefix = 'Lamy_unsensored'

# ユーザーからフォルダパスを入力
folder_path = sys.argv[2]
# folder_path = r"C:\イラスト関係\成果\002_販売\patreon\202402\02_022_Lamy\Lamy_base"

# シャッフルする場合 y を入力
is_shuffle = ""
# is_shuffle = sys.argv[3]
# is_shuffle = "y"

if( is_shuffle == "y" or is_shuffle =="Y"):
    is_shuffle = True

# フォルダの存在チェック
if not os.path.isdir(folder_path):
    print("指定したフォルダが存在しません。")
else:
    remove_png_metadata_and_rename(folder_path, prefix , is_shuffle)