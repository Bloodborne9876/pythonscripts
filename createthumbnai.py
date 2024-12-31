import os
from PIL import Image, ImageDraw, ImageFont
import random
import sys
import cv2
import numpy as np

def create_thumbnail(folder_path):
    # フォルダから全ての画像ファイルを取得
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    if len(image_files) < 4:
        print(f"エラー: {folder_path} には最低4枚の画像が必要です")
        return
    
    # 最初の画像を選択
    first_image = image_files[0]
    first_image_path = os.path.join(folder_path, first_image)
    first_size = Image.open(first_image_path).size
    
    # 同じサイズの画像を探す
    # ランダムに最初の画像を選択
    first_image = random.choice(image_files)
    first_image_path = os.path.join(folder_path, first_image)
    first_size = Image.open(first_image_path).size

    same_size_images = [first_image]
    error_count = 0
    while len(same_size_images) < 4 and error_count < 3:
        for img_file in image_files:
            if img_file not in same_size_images:
                img_path = os.path.join(folder_path, img_file)
                if Image.open(img_path).size == first_size:
                    same_size_images.append(img_file)
        if len(same_size_images) < 4:
            first_image = random.choice(image_files)
            first_image_path = os.path.join(folder_path, first_image)
            first_size = Image.open(first_image_path).size
            same_size_images = [first_image]
            error_count += 1

    if len(same_size_images) < 4:
        print(f"エラー: {folder_path} には同じサイズの画像が4枚必要です")
        return
    
    # 最初の画像と同じサイズの画像から3枚をランダムに選択
    selected_images = [first_image] + random.sample(same_size_images[1:], 3)
    
    # 画像を読み込み、最大サイズを取得
    images = []
    max_width = 0
    max_height = 0
    
    for img_file in selected_images:
        img_path = os.path.join(folder_path, img_file)
        img = Image.open(img_path)
        images.append(img)
        max_width = max(max_width, img.width)
        max_height = max(max_height, img.height)
    
    # サムネイルサイズを計算（2x2グリッドで表示するため2で割る）
    thumb_width = max_width // 2
    thumb_height = max_height // 2
    # パディングとテキストエリアを含む新しい画像を作成
    padding = 10
    text_height = int(thumb_height * 0.2)  # テキスト用に高さの20%を確保
    canvas_width = (thumb_width * 2) + (padding * 3)
    canvas_height = (thumb_height * 2) + (padding * 3) + text_height
    
    # 白い背景を作成
    result = Image.new('RGB', (canvas_width, canvas_height), 'white')
    draw = ImageDraw.Draw(result)
    
    # フォルダ名のテキストを追加
    parent_name = os.path.basename(os.path.dirname(folder_path))
    folder_name = f"{parent_name}_{os.path.basename(folder_path)}"

    try:
        # 利用可能な幅に合わせてフォントサイズを計算
        font_size = 1
        font = ImageFont.truetype("meiryo.ttc", font_size)
        text_bbox = draw.textbbox((0, 0), folder_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height_actual = text_bbox[3] - text_bbox[1]
        
        # テキストが収まる最大のフォントサイズを見つける
        while text_width < (canvas_width - padding * 2) and text_height_actual < text_height:
            font_size += 1
            font = ImageFont.truetype("meiryo.ttc", font_size)
            text_bbox = draw.textbbox((0, 0), folder_name, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height_actual = text_bbox[3] - text_bbox[1]
        
        # 最後の増加分を戻す
        font_size = max(1, font_size - 1)
        font = ImageFont.truetype("meiryo.ttc", int(font_size * 0.7))
    except:
        font = ImageFont.load_default()
    text_bbox = draw.textbbox((0, 0), folder_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (canvas_width - text_width) // 2
    draw.text((text_x, padding), folder_name, font=font, fill='black')
    
    # サムネイルを配置
    positions = [
        (padding, text_height + padding),
        (thumb_width + padding * 2, text_height + padding),
        (padding, text_height + thumb_height + padding * 2),
        (thumb_width + padding * 2, text_height + thumb_height + padding * 2)
    ]
    
    # Print positions for debugging
    # print("Thumbnail positions:")
    # for i, pos in enumerate(positions):
    #     print(f"Position {i+1}: {pos}")
    for img, pos in zip(images, positions):
        # アスペクト比を保持しながら画像をリサイズ
        img.thumbnail((thumb_width, thumb_height))
        # 画像をいったん貼り付け
        result.paste(img, pos)
        
        # サムネイル領域を切り出し
        x, y = pos
        area = result.crop((x, y, x + thumb_width, y + thumb_height))
        
        # PIL ImageをOpenCV形式に変換
        area_cv = cv2.cvtColor(np.array(area), cv2.COLOR_RGB2BGR)
        
        # ガウスぼかし処理
        h, w = area_cv.shape[:2]
        kernel_size = (99, 99)
        blurred_area = cv2.GaussianBlur(area_cv, kernel_size, 0)
        
        # OpenCV形式からPIL Imageに変換
        blurred_area_pil = Image.fromarray(cv2.cvtColor(blurred_area, cv2.COLOR_BGR2RGB))
        
        # ぼかし処理した画像を元の位置に貼り付け
        result.paste(blurred_area_pil, pos)
            
    # 親ディレクトリに結果を保存
    parent_dir = os.path.dirname(folder_path)
    output_filename = os.path.join(folder_path, folder_name + '_thumbnail.png')
    if os.path.exists(output_filename):
        os.remove(output_filename)
    result.save(output_filename, 'PNG')
    print(f"サムネイルを作成しました: {output_filename}")


# 使用例
if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        if not os.path.exists(folder_path):
            print(f"エラー: フォルダ '{folder_path}' が見つかりません。")
            sys.exit(1)
        create_thumbnail(folder_path)
    else:
        folder_path = input("フォルダパスを入力してください: ")
        # folder_path = r'C:\イラスト関係\成果\003_サブスク\202412\ブルーアーカイブ\test'
        while not os.path.exists(folder_path):
            print("フォルダが見つかりません。")
            folder_path = input("正しいフォルダパスを入力してください: ")
        create_thumbnail(folder_path)