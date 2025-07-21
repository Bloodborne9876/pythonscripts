from PIL import Image
import math
import os
import argparse
import sys

def create_square_collage(image_paths, output_path="collage.jpg", padding=10):
    """
    複数の画像を正方形のコラージュにまとめる（画像を正方形にクロップ）
    
    Args:
        image_paths: 画像ファイルのパスのリスト
        output_path: 出力ファイルのパス
        padding: 画像間の余白
    """
    if not image_paths:
        print("画像が指定されていません")
        return
    
    # 画像を読み込み
    images = []
    for path in image_paths:
        try:
            img = Image.open(path)
            images.append(img)
        except Exception as e:
            print(f"画像の読み込みに失敗: {path} - {e}")
    
    if not images:
        print("有効な画像がありません")
        return
    
    # グリッドサイズを計算（正方形に近い配置）
    num_images = len(images)
    grid_size = math.ceil(math.sqrt(num_images))
    
    # セルサイズを決定（最大画像サイズから適切なサイズを選択）
    max_size = max(max(img.width, img.height) for img in images)
    cell_size = max_size // 2 if max_size > 1000 else max_size
    
    # 最終的なコラージュサイズ
    collage_size = grid_size * cell_size + (grid_size - 1) * padding
    
    # 新しい正方形画像を作成
    collage = Image.new('RGB', (collage_size, collage_size), 'white')
    
    # 画像を配置
    for i, img in enumerate(images):
        row = i // grid_size
        col = i % grid_size
        
        # 画像を正方形にクロップ
        img_square = crop_to_square(img)
        
        # 画像をセルサイズにリサイズ
        img_resized = img_square.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
        
        # 配置位置を計算
        x = col * (cell_size + padding)
        y = row * (cell_size + padding)
        
        # 画像を貼り付け
        collage.paste(img_resized, (x, y))
    
    # 保存
    collage.save(output_path, quality=95)
    print(f"コラージュを保存しました: {output_path}")
    print(f"サイズ: {collage_size}x{collage_size}px")
    print(f"グリッド: {grid_size}x{grid_size}, セルサイズ: {cell_size}x{cell_size}px")

def crop_to_square(image):
    """
    画像を正方形にクロップ（中央部分を取得）
    """
    width, height = image.size
    
    # 正方形のサイズを決定（短い辺に合わせる）
    square_size = min(width, height)
    
    # クロップ位置を計算（中央）
    left = (width - square_size) // 2
    top = (height - square_size) // 2
    right = left + square_size
    bottom = top + square_size
    
    # クロップして返す
    return image.crop((left, top, right, bottom))

def resize_image_to_fit(image, max_width, max_height):
    """
    アスペクト比を維持して画像をリサイズ（旧関数、互換性のため残す）
    """
    original_width, original_height = image.size
    
    # アスペクト比を計算
    width_ratio = max_width / original_width
    height_ratio = max_height / original_height
    ratio = min(width_ratio, height_ratio)
    
    # 新しいサイズを計算
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def main():
    parser = argparse.ArgumentParser(description="複数の画像を正方形のコラージュにまとめる（画像をクロップ）")
    parser.add_argument("images", nargs="+", help="入力画像のパス")
    parser.add_argument("-o", "--output", default="collage.jpg", help="出力ファイル名")
    parser.add_argument("-p", "--padding", type=int, default=10, help="画像間の余白")
    
    args = parser.parse_args()
    
    # 存在する画像ファイルのみをフィルタ
    valid_images = [path for path in args.images if os.path.exists(path)]
    
    if not valid_images:
        print("有効な画像ファイルが見つかりません")
        return
    
    create_square_collage(valid_images, args.output, args.padding)

if __name__ == "__main__":
    # デバッグ用の引数設定
    if len(sys.argv) == 1:  # 引数が指定されていない場合
        # ここにデバッグ用の引数を設定
        sys.argv = [
            "Part.py",  # スクリプト名
            r"C:\temp\outputs\2025-06-05\20250605_201823_545133_700482487.png",  # 入力画像1
            r"C:\temp\outputs\2025-06-05\20250605_201738_007993_1436391244.png",  # 入力画像2
            "-o", r"C:\temp\outputs\2025-06-05\debug_collage.jpg",  # 出力ファイル名
            "-p", "15"  # パディング
        ]
    
    main()