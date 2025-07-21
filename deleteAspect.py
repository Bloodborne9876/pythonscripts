import os
from PIL import Image
import argparse
import time
import logging

# ロギング設定
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def is_png_file(filename: str) -> bool:
    """ファイルがPNG形式か判定する"""
    return filename.lower().endswith('.png')

def get_image_resolution(file_path: str) -> tuple[int, int] | None:
    """画像の解像度を取得する"""
    try:
        with Image.open(file_path) as img:
            return img.size
    except Exception as e:
        logger.error(f"画像処理エラー: {file_path} - {e}")
        return None

def try_delete_file(file_path: str, max_retries: int = 3, base_delay: float = 0.5) -> bool:
    """ファイルを削除し、失敗時は再試行する"""
    for attempt in range(max_retries):
        try:
            os.remove(file_path)
            logger.info(f"削除成功: {file_path}")
            return True
        except PermissionError:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)  # 指数バックオフ
                logger.warning(f"ファイル使用中: {file_path} - {attempt + 1}/{max_retries}回目、{delay}秒待機")
                time.sleep(delay)
            else:
                logger.error(f"削除失敗: {file_path} - ファイルが使用中のため削除できません")
                return False
        except Exception as e:
            logger.error(f"削除エラー: {file_path} - {e}")
            return False
    return False

def delete_low_resolution_png(folder_path: str, max_width: int, max_height: int, max_retries: int = 3):
    """
    指定フォルダ内で、指定解像度以下のPNGファイルを削除する。

    Args:
        folder_path (str): 対象のフォルダパス
        max_width (int): 最大幅（ピクセル）
        max_height (int): 最大高さ（ピクセル）
        max_retries (int): 削除失敗時の最大再試行回数
    """
    if not os.path.isdir(folder_path):
        logger.error(f"無効なフォルダ: {folder_path}")
        return

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if not is_png_file(filename):
                continue
            file_path = os.path.join(root, filename)
            resolution = get_image_resolution(file_path)
            if resolution is None:
                continue
            width, height = resolution
            if width <= max_width and height <= max_height:
                try_delete_file(file_path, max_retries)
            else:
                logger.debug(f"保持: {file_path} ({width}x{height})")

def main():
    parser = argparse.ArgumentParser(description="指定解像度以下のPNGファイルを削除するスクリプト")
    parser.add_argument("folder", help="対象フォルダのパス")
    parser.add_argument("width", type=int, help="最大幅（ピクセル）")
    parser.add_argument("height", type=int, help="最大高さ（ピクセル）")
    parser.add_argument("--retries", type=int, default=3, help="削除再試行回数（デフォルト: 3）")
    args = parser.parse_args()

    delete_low_resolution_png(args.folder, args.width, args.height, args.retries)
    logger.info("処理が完了しました。")

if __name__ == "__main__":
    # デバッグ用にハードコードされた値（本番ではコマンドライン引数を使用）
    folder = r"C:\temp\outputs"
    # folder = r"D:\000_Backup\000_AI\001_Output"
    width = 1392
    height = 960
    delete_low_resolution_png(folder, width, height)
    delete_low_resolution_png(folder, height, width)  # 縦横を入れ替えても同じ処理を行う
    # main()  # コマンドライン引数を使用する場合はこちらを有効に