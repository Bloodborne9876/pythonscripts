import os
import sys
import random
import math
import datetime
from PIL import Image, ImageFilter

def get_image_files(root_dir):
    """指定フォルダ以下の画像ファイルを再帰的に取得する"""
    image_extensions = {'.jpg', '.jpeg', '.png'}
    image_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in image_extensions:
                image_files.append(os.path.join(dirpath, filename))
    return image_files

def crop_center_square(img):
    """画像を中央で正方形にクロップする"""
    width, height = img.size
    size = min(width, height)
    
    left = (width - size) // 2
    top = (height - size) // 2
    right = (width + size) // 2
    bottom = (height + size) // 2
    
    return img.crop((left, top, right, bottom))

def apply_mosaic(img, radius=15):
    """画像にガウスぼかしを適用する（すりガラス風）"""
    return img.filter(ImageFilter.GaussianBlur(radius))

def create_collage(folder_path, used_files_history, num_images=4, output_size=2048, suffix="", use_mosaic=False):
    """
    フォルダ内の画像を使って正方形のコラージュを作成する。
    指定枚数に応じてグリッドサイズを自動調整する。
    """
    image_files = get_image_files(folder_path)
    
    if not image_files:
        print("画像ファイル(jpg, png)が見つかりませんでした。")
        return

    # 過去に使用された画像を除外候補とする
    # ただし、未使用画像が足りない場合は、全画像から選ぶ（リセット的な挙動）
    available_files = [f for f in image_files if f not in used_files_history]
    
    if len(available_files) < num_images:
        print("未使用の画像が足りないため、使用済み画像も含めて選択します。")
        available_files = image_files

    # グリッドサイズの計算 (指定枚数を収める最小の正方形グリッド)
    # 例: 4枚->2x2, 5枚->3x3, 9枚->3x3
    grid_size = math.ceil(math.sqrt(num_images))
    total_cells = grid_size * grid_size
    
    # 画像選択
    if len(available_files) < num_images:
        # 画像が足りない場合はあるだけ繰り返して埋める
        selected_files = available_files * (num_images // len(available_files) + 1)
        selected_files = selected_files[:num_images]
    else:
        selected_files = random.sample(available_files, num_images)

    # 使用履歴に追加
    for f in selected_files:
        used_files_history.add(f)

    print(f"使用する画像: {len(selected_files)}枚 (グリッド: {grid_size}x{grid_size})")
    for f in selected_files:
        print(f" - {os.path.basename(f)}")

    # グリッドの余白を埋めるために、選ばれた画像からランダムに追加して埋める
    # これにより余白(白い部分)が出ないようにする
    files_for_grid = selected_files[:]
    while len(files_for_grid) < total_cells:
        files_for_grid.append(random.choice(selected_files))

    # 出力キャンバス作成
    collage = Image.new('RGB', (output_size, output_size), (255, 255, 255))
    
    # 1セルあたりのサイズ
    cell_size = output_size // grid_size

    for index, file_path in enumerate(files_for_grid):
        try:
            with Image.open(file_path) as img:
                # 画像をRGBモードに変換（PNGの透過対策など）
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 正方形にクロップ
                img_cropped = crop_center_square(img)
                
                # モザイク処理 (必要であれば)
                if use_mosaic:
                    # radiusでぼかしの強さを調整 (数値が大きいほど強くぼける)
                    img_cropped = apply_mosaic(img_cropped, radius=30)

                # セルサイズにリサイズ (LANCZOSは高品質なリサイズフィルタ)
                img_resized = img_cropped.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
                
                # 配置位置の計算
                x = (index % grid_size) * cell_size
                y = (index // grid_size) * cell_size
                
                collage.paste(img_resized, (x, y))
                
        except Exception as e:
            print(f"画像の読み込みに失敗しました: {file_path}, Error: {e}")

    # 保存
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    filename = f"thumbnail_collage_{date_str}{suffix}.jpg"
    output_path = os.path.join(folder_path, filename)

    try:
        collage.save(output_path, quality=95)
        print(f"サムネイルを作成しました: {output_path}")
    except Exception as e:
        print(f"保存に失敗しました: {e}")

if __name__ == "__main__":
    # 引数処理
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        print("指定したフォルダ内の画像をランダムに選んで正方形のコラージュを作成します。")
        target_dir = input("対象のフォルダパスを入力してください: ").strip('"').strip("'")
    
    if os.path.exists(target_dir):
        # 枚数入力
        num_input = input("使用する画像の枚数を入力してください (デフォルト: 9): ").strip()
        if num_input.isdigit() and int(num_input) > 0:
            num_images = int(num_input)
        else:
            num_images = 9

        # 繰り返し回数入力
        repeat_input = input("繰り返し回数を入力してください (デフォルト: 1): ").strip()
        if repeat_input.isdigit() and int(repeat_input) > 0:
            repeat_count = int(repeat_input)
        else:
            repeat_count = 1

        # モザイク処理の確認
        use_mosaic = False
        while True:
            mosaic_input = input("画像にモザイクをかけますか？ (y/n) [n]: ").lower().strip()
            if mosaic_input == 'y' or mosaic_input == 'yes':
                use_mosaic = True
                break
            elif mosaic_input == '' or mosaic_input == 'n' or mosaic_input == 'no':
                use_mosaic = False
                break
            else:
                print("y または n を入力してください。")

        # Pillowがインストールされているかチェック
        try:
            import PIL
            used_files_history = set()
            for i in range(repeat_count):
                suffix = ""
                if repeat_count > 1:
                    suffix = f"_{i+1:03d}"
                create_collage(target_dir, used_files_history, num_images=num_images, suffix=suffix, use_mosaic=use_mosaic)
        except ImportError:
            print("エラー: Pillowライブラリがインストールされていません。")
            print("以下のコマンドでインストールしてください:")
            print("pip install Pillow")
    else:
        print(f"指定されたフォルダが存在しません: {target_dir}")
