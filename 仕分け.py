import os
import shutil
from PIL import Image
import re
from tqdm import tqdm
import colorama
from colorama import Fore, Style
import logging
from pathlib import Path
from typing import Dict, Optional, List, Tuple
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
from functools import partial
import threading

# coloramaを初期化（Windows対応）
colorama.init()

# ログ設定
logging.basicConfig(
    filename="genre_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# JPG品質設定
JPG_QUALITY = 95
JPG_OPTIMIZE = True
JPG_PROGRESSIVE = True

# パフォーマンス設定
MAX_WORKERS = min(32, (os.cpu_count() or 1) + 4)  # スレッド数
CHUNK_SIZE = 10  # バッチサイズ

class GenreClassifier:
    """ジャンル分類器クラス"""
    
    def __init__(self):
        self.genre_keywords = {
            "ブルアカ": r"\b(archive)\b",
            "学マス": r"\b(ume|misuzu|katsuragi|sumika|hanami|kotone|himesaki|aarinami|sena)\b",
            "アーリャ": r"\b(alisa)\b",
            "イリヤ": r"\b(aaillya|fate/kaleid liner prisma illya)\b",
            "ロリ": r"\b(loli|toddler|flat chest)\b"
        }
    
    def infer_genre(self, prompt: str) -> str:
        """プロンプトからジャンルを推論する"""
        if not prompt:
            return "オリジナル"
        
        prompt_lower = prompt.lower()
        
        for genre, pattern in self.genre_keywords.items():
            if re.search(pattern, prompt_lower):
                return genre
        
        return "その他"

def extract_metadata_worker(file_path: str) -> str:
    """メタデータ抽出（ワーカー関数）"""
    try:
        with Image.open(file_path) as img:
            return img.info.get("parameters", "")
    except Exception:
        return ""

def convert_to_jpg_worker(source_path: str, dest_path: str, quality: int = JPG_QUALITY) -> bool:
    """JPG変換（ワーカー関数）"""
    try:
        with Image.open(source_path) as img:
            # RGBAの場合はRGBに変換
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            # 高品質でJPG保存
            img.save(
                dest_path,
                'JPEG',
                quality=quality,
                optimize=JPG_OPTIMIZE,
                progressive=JPG_PROGRESSIVE,
                subsampling=0,
                qtables='web_high'
            )
            return True
    except Exception as e:
        logging.error(f"JPG変換エラー: {source_path} -> {dest_path} - {e}")
        return False

def process_image_batch(batch_data: List[Tuple[Path, str, str, int]]) -> List[Tuple[bool, str, str]]:
    """画像バッチ処理（マルチプロセス用）"""
    results = []
    classifier = GenreClassifier()
    
    for file_path, output_folder, genre_base, start_counter in batch_data:
        try:
            # メタデータ取得
            metadata = extract_metadata_worker(str(file_path))
            genre = classifier.infer_genre(metadata)
            
            # 出力パス作成
            genre_folder = Path(output_folder) / genre
            genre_folder.mkdir(parents=True, exist_ok=True)
            
            # ファイル名生成
            counter = start_counter + len([r for r in results if r[0] and r[2] == genre])
            new_filename = f"{genre}_{counter:03d}.jpg"
            dest_path = genre_folder / new_filename
            
            # JPG変換
            success = convert_to_jpg_worker(str(file_path), str(dest_path))
            results.append((success, str(file_path), genre))
            
        except Exception as e:
            logging.error(f"バッチ処理エラー: {file_path} - {e}")
            results.append((False, str(file_path), "error"))
    
    return results

class ImageProcessor:
    """画像処理クラス（パラレル対応）"""
    
    def __init__(self, quality: int = JPG_QUALITY, max_workers: int = MAX_WORKERS):
        self.quality = quality
        self.max_workers = max_workers
        self.classifier = GenreClassifier()
    
    def extract_metadata(self, file_path: str) -> str:
        """画像からメタデータを抽出"""
        return extract_metadata_worker(file_path)
    
    def convert_to_jpg(self, source_path: str, dest_path: str) -> bool:
        """PNGをJPGに変換"""
        return convert_to_jpg_worker(source_path, dest_path, self.quality)
    
    def get_new_filename(self, original_filename: str, genre: str, counter: int) -> str:
        """新しいファイル名を生成"""
        return f"{genre}_{counter:03d}.jpg"

class ImageOrganizer:
    """画像整理メインクラス（パラレル対応）"""
    
    def __init__(self, input_folder: str, output_folder: str, max_workers: int = MAX_WORKERS):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.processor = ImageProcessor(max_workers=max_workers)
        self.max_workers = max_workers
        self.genre_counters: Dict[str, int] = {}
        self.stats = {
            'processed': 0,
            'errors': 0,
            'converted': 0
        }
        self.lock = threading.Lock()
    
    def setup_output_folder(self) -> None:
        """出力フォルダを準備"""
        if self.output_folder.exists():
            try:
                shutil.rmtree(self.output_folder)
                logging.info(f"出力フォルダを削除: {self.output_folder}")
                print(f"{Fore.YELLOW}出力フォルダを削除: {self.output_folder}{Style.RESET_ALL}")
            except Exception as e:
                logging.error(f"出力フォルダ削除エラー: {e}")
                print(f"{Fore.RED}出力フォルダ削除エラー: {e}{Style.RESET_ALL}")
        
        self.output_folder.mkdir(parents=True, exist_ok=True)
    
    def get_png_files(self) -> List[Path]:
        """入力フォルダからPNGファイルを収集"""
        png_files = []
        for file_path in self.input_folder.rglob("*.png"):
            if file_path.is_file():
                png_files.append(file_path)
        return png_files
    
    def process_single_image_parallel(self, file_path: Path) -> Tuple[bool, str, str]:
        """単一画像処理（パラレル用）"""
        try:
            # メタデータ取得とジャンル分類
            metadata = self.processor.extract_metadata(str(file_path))
            genre = self.processor.classifier.infer_genre(metadata)
            
            # スレッドセーフなカウンター更新
            with self.lock:
                self.genre_counters[genre] = self.genre_counters.get(genre, 0) + 1
                counter = self.genre_counters[genre]
            
            # ジャンルフォルダ作成
            genre_folder = self.output_folder / genre
            genre_folder.mkdir(exist_ok=True)
            
            # ファイル名生成と変換
            new_filename = self.processor.get_new_filename(file_path.name, genre, counter)
            dest_path = genre_folder / new_filename
            
            success = self.processor.convert_to_jpg(str(file_path), str(dest_path))
            
            # ログ記録
            prompt_snippet = metadata[:50] + ("..." if len(metadata) > 50 else "")
            logging.info(f"処理: {file_path.name}, ジャンル: {genre}, プロンプト: {prompt_snippet}")
            
            return success, str(file_path), genre
            
        except Exception as e:
            logging.error(f"並列処理エラー: {file_path} - {e}")
            return False, str(file_path), "error"
    
    def organize_images_parallel(self) -> None:
        """パラレル画像整理処理"""
        self.setup_output_folder()
        
        png_files = self.get_png_files()
        if not png_files:
            print(f"{Fore.YELLOW}PNGファイルが見つかりませんでした{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}並列処理開始: {len(png_files)}個のPNGファイルを{self.max_workers}スレッドで処理{Style.RESET_ALL}")
        
        # ThreadPoolExecutorで並列処理
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # プログレスバー付きで実行
            results = list(tqdm(
                executor.map(self.process_single_image_parallel, png_files),
                total=len(png_files),
                desc="画像変換中",
                unit="ファイル"
            ))
        
        # 結果集計
        for success, file_path, genre in results:
            self.stats['processed'] += 1
            if success:
                self.stats['converted'] += 1
                print(f"{Fore.GREEN}変換完了: {Path(file_path).name}{Style.RESET_ALL}")
            else:
                self.stats['errors'] += 1
        
        self.show_results()
        self.open_output_folder()
    
    def organize_images(self) -> None:
        """画像整理のメイン処理（パラレル版を使用）"""
        self.organize_images_parallel()
    
    def show_results(self) -> None:
        """処理結果を表示"""
        print(f"\n{Fore.CYAN}=== 処理結果 ==={Style.RESET_ALL}")
        print(f"{Fore.GREEN}処理済み: {self.stats['processed']}ファイル{Style.RESET_ALL}")
        print(f"{Fore.GREEN}変換成功: {self.stats['converted']}ファイル{Style.RESET_ALL}")
        print(f"{Fore.RED}エラー: {self.stats['errors']}ファイル{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}品質: {JPG_QUALITY}% (最適化あり){Style.RESET_ALL}")
        print(f"{Fore.CYAN}使用スレッド数: {self.max_workers}{Style.RESET_ALL}")
        
        # ジャンル別統計
        if self.genre_counters:
            print(f"\n{Fore.CYAN}=== ジャンル別統計 ==={Style.RESET_ALL}")
            for genre, count in sorted(self.genre_counters.items()):
                print(f"{Fore.BLUE}{genre}: {count}ファイル{Style.RESET_ALL}")
    
    def open_output_folder(self) -> None:
        """出力フォルダを開く"""
        try:
            os.startfile(str(self.output_folder))
            logging.info(f"出力フォルダを開きました: {self.output_folder}")
            print(f"{Fore.BLUE}出力フォルダを開きました: {self.output_folder}{Style.RESET_ALL}")
        except Exception as e:
            error_msg = f"出力フォルダを開く際にエラー: {e}"
            logging.error(error_msg)
            print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")

def main():
    """メイン実行関数"""
    # 設定
    input_folder = r"C:\temp\outputs\sample"
    output_base_folder = r"C:\temp\outputs\sample\temp"
    
    # CPU数に基づいてワーカー数を最適化
    cpu_count = os.cpu_count() or 1
    max_workers = min(32, cpu_count + 4)
    
    print(f"{Fore.CYAN}システム情報: CPU {cpu_count}コア, 使用スレッド数: {max_workers}{Style.RESET_ALL}")
    
    # 処理実行
    organizer = ImageOrganizer(input_folder, output_base_folder, max_workers=max_workers)
    organizer.organize_images()
    
    print(f"\n{Fore.BLUE}画像の整理が完了しました。ログは genre_log.txt に保存されています。{Style.RESET_ALL}")

if __name__ == "__main__":
    main()