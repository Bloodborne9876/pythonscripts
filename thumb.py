from PIL import Image
import random
import os
import sys
from pathlib import Path



def create_thumbnail(image_folder, num_cols, padding, output_path):
    imageSize = 1500
    # 画像フォルダ内の画像を取得
    image_files = []
    fileList = os.listdir(image_folder)
    random.shuffle(fileList)
    for filename in fileList[:16]:
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_files.append(os.path.join(image_folder, filename))

    # サムネイルの行数を計算
    num_images = len(image_files)
    num_rows =2 # (num_images + num_cols - 1) // num_cols

    # サムネイルの幅と高さを計算
    thumbnail_width = imageSize // num_cols
    thumbnail_height = imageSize // num_rows

    # 左右の余白を計算
    total_width = thumbnail_width * num_cols + padding * (num_cols - 1)
    left_margin = (imageSize - total_width) // 2

    # サムネイル用のキャンバスを作成
    thumbnail_size = (total_width, imageSize)
    thumbnail_canvas = Image.new('RGB', thumbnail_size, (255, 255, 255))

    # 画像を縮小してサムネイルに追加
    for i, image_path in enumerate(image_files):
        image = Image.open(image_path)
        image.thumbnail((thumbnail_width, thumbnail_height))

        # サムネイルをキャンバスに貼り付け
        col_idx = i % num_cols
        row_idx = i // num_cols
        x = left_margin + (thumbnail_width + padding) * col_idx
        y = thumbnail_height * row_idx
        thumbnail_canvas.paste(image, (x, y))

    # サムネイルを保存
    thumbnail_canvas.save(output_path)

# 入力画像のフォルダパスを指定
#image_folder = r'C:\stable-diffusion-webui\成果\保存\キャラ\原神\Genryu\Genryu_jpg\投稿'  # 実際のフォルダパスに置き換えてください
image_folder = sys.argv[1]

# 列数を指定
num_cols = 3

# 左右の空白を指定
padding = 0  # ピクセル単位で指定してください

# 出力パスを指定11
output_path = os.path.join(os.path.abspath(os.path.join(image_folder, os.pardir)), 'thumbnail.jpg')  # サムネイルの保存先を指定してください

# サムネイルを作成
create_thumbnail(image_folder, num_cols, padding, output_path)
