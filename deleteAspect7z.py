import os
import argparse
import time
import logging
import shutil
import py7zr
from PIL import Image
from pathlib import Path
from tqdm import tqdm
from colorama import init, Fore, Style

# coloramaの初期化（Windows対応）
init()

# ロギング設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

class ProcessingStats:
    """処理統計を管理"""
    def __init__(self):
        self.total_files = 0
        self.processed_files = 0
        self.deleted_files = 0
        self.errors = 0

    def log_summary(self):
        """処理のサマリーをログ出力"""
        logger.info(
            f"{Fore.CYAN}=== 処理サマリー ==={Style.RESET_ALL}\n"
            f"総7zファイル数: {self.total_files}\n"
            f"処理済みファイル数: {self.processed_files}\n"
            f"削除したファイル数: {self.deleted_files}\n"
            f"エラー発生数: {self.errors}{Style.RESET_ALL}"
        )

def is_target_file(filename: str, max_width: int, max_height: int, file_path: str) -> bool:
    """ファイルが削除対象か判定する（PNG解像度、JPG、gridを含むファイル）"""
    filename_lower = filename.lower()
    
    # JPGファイル
    if filename_lower.endswith('.jpg') or filename_lower.endswith('.jpeg'):
        return True
    
    # "grid"を含むファイル
    if 'grid' in filename_lower:
        return True
    
    # PNGファイルで解像度チェック
    if filename_lower.endswith('.png'):
        resolution = get_image_resolution(file_path)
        if resolution is None:
            return False
        width, height = resolution
        return width <= max_width and height <= max_height
    
    return False

def get_image_resolution(file_path: str) -> tuple[int, int] | None:
    """画像の解像度を取得する"""
    try:
        with Image.open(file_path) as img:
            return img.size
    except Exception as e:
        logger.error(f"{Fore.RED}画像処理エラー: {file_path} - {e}{Style.RESET_ALL}")
        return None

def try_delete_file(file_path: str, max_retries: int = 3, base_delay: float = 0.5) -> bool:
    """ファイルを削除し、失敗時は再試行する"""
    for attempt in range(max_retries):
        try:
            os.remove(file_path)
            logger.info(f"{Fore.GREEN}削除成功: {file_path}{Style.RESET_ALL}")
            return True
        except PermissionError:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)  # 指数バックオフ
                logger.warning(f"{Fore.YELLOW}ファイル使用中: {file_path} - {attempt + 1}/{max_retries}回目、{delay}秒待機{Style.RESET_ALL}")
                time.sleep(delay)
            else:
                logger.error(f"{Fore.RED}削除失敗: {file_path} - ファイルが使用中のため削除できません{Style.RESET_ALL}")
                return False
        except Exception as e:
            logger.error(f"{Fore.RED}削除エラー: {file_path} - {e}{Style.RESET_ALL}")
            return False
    return False

def extract_7z(archive_path: str, extract_dir: str) -> bool:
    """7zファイルを指定フォルダに解凍する"""
    try:
        with py7zr.SevenZipFile(archive_path, mode='r') as archive:
            archive.extractall(extract_dir)
        logger.info(f"{Fore.GREEN}解凍成功: {archive_path} -> {extract_dir}{Style.RESET_ALL}")
        return True
    except Exception as e:
        logger.error(f"{Fore.RED}解凍エラー: {archive_path} - {e}{Style.RESET_ALL}")
        return False

def compress_7z(folder_path: str, archive_path: str) -> bool:
    """フォルダを7zファイルに圧縮する"""
    try:
        # フォルダが空か確認
        if not any(os.scandir(folder_path)):
            logger.warning(f"{Fore.YELLOW}フォルダが空です: {folder_path} - 空の7zファイルを作成します{Style.RESET_ALL}")
        with py7zr.SevenZipFile(archive_path, mode='w') as archive:
            archive.writeall(folder_path)
        logger.info(f"{Fore.GREEN}圧縮成功: {folder_path} -> {archive_path}{Style.RESET_ALL}")
        return True
    except Exception as e:
        logger.error(f"{Fore.RED}圧縮エラー: {folder_path} - {e}{Style.RESET_ALL}")
        return False

def delete_folder(folder_path: str, max_retries: int = 3, base_delay: float = 0.5) -> bool:
    """フォルダを削除し、失敗時は再試行する"""
    for attempt in range(max_retries):
        try:
            shutil.rmtree(folder_path)
            logger.info(f"{Fore.GREEN}フォルダ削除成功: {folder_path}{Style.RESET_ALL}")
            return True
        except PermissionError:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                logger.warning(f"{Fore.YELLOW}フォルダ使用中: {folder_path} - {attempt + 1}/{max_retries}回目、{delay}秒待機{Style.RESET_ALL}")
                time.sleep(delay)
            else:
                logger.error(f"{Fore.RED}フォルダ削除失敗: {folder_path} - 使用中のため削除できません{Style.RESET_ALL}")
                return False
        except Exception as e:
            logger.error(f"{Fore.RED}フォルダ削除エラー: {folder_path} - {e}{Style.RESET_ALL}")
            return False
    return False

def find_7z_files(folder_path: str) -> list[str]:
    """指定フォルダとサブフォルダから7zファイルを検索"""
    seven_zip_files = []
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith('.7z'):
                seven_zip_files.append(os.path.join(root, filename))
    logger.info(f"{Fore.CYAN}7zファイル検索完了: {len(seven_zip_files)} ファイル発見{Style.RESET_ALL}")
    return seven_zip_files

def process_7z_file(archive_path: str, max_width: int, max_height: int, max_retries: int, stats: ProcessingStats) -> bool:
    """単一の7zファイルを処理（解凍、元の7z削除、ファイル削除、圧縮、フォルダ削除）"""
    # 7zファイルの存在確認
    if not os.path.isfile(archive_path) or not archive_path.lower().endswith('.7z'):
        logger.error(f"{Fore.RED}無効な7zファイル: {archive_path}{Style.RESET_ALL}")
        stats.errors += 1
        return False

    # 解凍先フォルダの作成
    archive_name = Path(archive_path).stem
    extract_dir = os.path.join(os.path.dirname(archive_path), f"temp_{archive_name}")
    os.makedirs(extract_dir, exist_ok=True)

    # 7zファイルの解凍
    if not extract_7z(archive_path, extract_dir):
        stats.errors += 1
        return False

    # 元の7zファイルを削除
    if not try_delete_file(archive_path, max_retries):
        logger.error(f"{Fore.RED}元の7zファイルの削除に失敗したため処理をスキップ: {archive_path}{Style.RESET_ALL}")
        stats.errors += 1
        return False

    # ファイルの削除
    files_to_process = []
    for root, _, files in os.walk(extract_dir):
        for filename in files:
            files_to_process.append(os.path.join(root, filename))

    if not files_to_process:
        logger.warning(f"{Fore.YELLOW}処理対象ファイルなし: {extract_dir}{Style.RESET_ALL}")
    
    for file_path in tqdm(files_to_process, desc=f"ファイル処理中 ({archive_name})", leave=True, mininterval=0.1):
        if is_target_file(os.path.basename(file_path), max_width, max_height, file_path):
            if try_delete_file(file_path, max_retries):
                stats.deleted_files += 1

    # フォルダを7zに圧縮（同じファイル名で新規作成）
    new_archive_path = os.path.join(os.path.dirname(archive_path), f"{archive_name}.7z")
    if not compress_7z(extract_dir, new_archive_path):
        stats.errors += 1
        return False

    # 解凍フォルダの削除
    if not delete_folder(extract_dir, max_retries):
        stats.errors += 1
        return False

    stats.processed_files += 1
    return True

def main():
    parser = argparse.ArgumentParser(description="指定フォルダ内の7zファイルから指定条件のファイルを削除し、再圧縮するスクリプト")
    parser.add_argument("folder", help="7zファイルを検索するフォルダパス")
    parser.add_argument("--width", type=int, default=1216, help="最大幅（ピクセル、デフォルト: 1216）")
    parser.add_argument("--height", type=int, default=832, help="最大高さ（ピクセル、デフォルト: 832）")
    parser.add_argument("--retries", type=int, default=3, help="削除再試行回数（デフォルト: 3）")

    try:
        args = parser.parse_args()
    except SystemExit:
        logger.error(f"{Fore.RED}コマンドライン引数が正しくありません。例: python process_7z_files.py <folder> [--width <width>] [--height <height>] [--retries <retries>]{Style.RESET_ALL}")
        return

    # フォルダの存在確認
    if not os.path.isdir(args.folder):
        logger.error(f"{Fore.RED}無効なフォルダ: {args.folder}{Style.RESET_ALL}")
        return

    # 7zファイルの検索
    stats = ProcessingStats()
    seven_zip_files = find_7z_files(args.folder)
    stats.total_files = len(seven_zip_files)
    if not seven_zip_files:
        logger.warning(f"{Fore.YELLOW}7zファイルが見つかりませんでした: {args.folder}{Style.RESET_ALL}")
        return

    # 各7zファイルを処理
    for i, archive in enumerate(tqdm(seven_zip_files, desc="7zファイル処理中", unit="file", leave=True, mininterval=0.1)):
        logger.info(f"{Fore.CYAN}処理開始: {archive} ({i+1}/{stats.total_files}){Style.RESET_ALL}")
        process_7z_file(archive, args.width, args.height, args.retries, stats)
        logger.info(f"{Fore.CYAN}処理完了: {archive} ({i+1}/{stats.total_files}){Style.RESET_ALL}")

    # サマリー表示
    stats.log_summary()

if __name__ == "__main__":
    # デバッグ用
    # folder = r"D:\000_Backup\000_AI\001_Output\test"
    folder = r"C:\temp\outputs"
    max_width = 1216
    max_height = 832
    max_retries = 3
    stats = ProcessingStats()

    # フォルダの存在確認
    if not os.path.isdir(folder):
        logger.error(f"{Fore.RED}無効なフォルダ: {folder}{Style.RESET_ALL}")
    else:
        # 7zファイルの検索
        seven_zip_files = find_7z_files(folder)
        stats.total_files = len(seven_zip_files)
        if not seven_zip_files:
            logger.warning(f"{Fore.YELLOW}7zファイルが見つかりませんでした: {folder}{Style.RESET_ALL}")
        else:
            # 各7zファイルを処理
            for i, archive in enumerate(tqdm(seven_zip_files, desc="7zファイル処理中", unit="file", leave=True, mininterval=0.1)):
                logger.info(f"{Fore.CYAN}処理開始: {archive} ({i+1}/{stats.total_files}){Style.RESET_ALL}")
                process_7z_file(archive, max_width, max_height, max_retries, stats)
                logger.info(f"{Fore.CYAN}処理完了: {archive} ({i+1}/{stats.total_files}){Style.RESET_ALL}")
            # サマリー表示
            stats.log_summary()

    # コマンドライン引数を使用する場合は以下を有効に
    # main()