import os
import sys
import re
import shutil
import time
import gc
import subprocess
from typing import List, Callable

try:
    from PIL import Image
except ImportError:
    Image = None


def find_7z_files(root_dir: str) -> List[str]:
    """指定フォルダ以下の7zファイルを再帰的に取得する"""
    seven_z_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.7z'):
                seven_z_files.append(os.path.join(dirpath, filename))
    return seven_z_files


def safe_remove(path: str, retries: int = 3, delay: float = 0.5):
    """ファイル削除を試行し、失敗した場合はGCを走らせてリトライする"""
    if not os.path.exists(path):
        return
    for i in range(retries):
        try:
            os.remove(path)
            return
        except Exception:
            if i < retries - 1:
                gc.collect()
                time.sleep(delay)
            else:
                raise


def safe_rmtree(path: str, retries: int = 3, delay: float = 0.5):
    """ディレクトリ削除を試行し、失敗した場合はGCを走らせてリトライする"""
    if not os.path.exists(path):
        return
    for i in range(retries):
        try:
            shutil.rmtree(path, ignore_errors=True)
            if not os.path.exists(path):
                return
            time.sleep(delay)
        except Exception:
            if i < retries - 1:
                gc.collect()
                time.sleep(delay)


def extract_7z(archive_path: str, target_dir: str):
    """7zアーカイブを解凍する"""
    subprocess.run(
        ['7z', 'x', archive_path, f'-o{target_dir}', '-y'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )


def compress_7z(archive_path: str, source_dir: str):
    """ディレクトリを7zに圧縮する"""
    subprocess.run(
        ['7z', 'a', '-r', archive_path, '.'],
        cwd=source_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )


def delete_small_pngs_in_dir(directory: str, min_pixel_size: int = 512) -> int:
    """ディレクトリ内の小さいPNGを削除する"""
    if Image is None:
        print("    警告: PILが利用できないため、PNG削除処理をスキップします")
        return 0
    
    deleted = 0
    checked = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                path = os.path.join(root, file)
                checked += 1
                try:
                    img = None
                    try:
                        img = Image.open(path)
                        w, h = img.size
                        if w <= min_pixel_size or h <= min_pixel_size:
                            # ファイルをクローズしてロックを解放
                            img.close()
                            img = None
                            gc.collect()
                            time.sleep(0.1)
                            
                            # 削除を試行
                            try:
                                os.remove(path)
                                deleted += 1
                                print(f"      削除: {file} ({w}x{h})")
                            except Exception as e:
                                print(f"      警告: {file} の削除に失敗しました: {e}")
                    finally:
                        if img is not None:
                            img.close()
                            gc.collect()
                except Exception as e:
                    print(f"      警告: {file} の読み込みに失敗しました: {e}")
    
    if checked > 0:
        print(f"    PNG処理: {checked}個確認, {deleted}個削除")
    return deleted


def delete_by_pattern_in_dir(directory: str, pattern: str) -> int:
    """ディレクトリ内のパターンに一致するファイルを削除する"""
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error as e:
        print(f"    エラー: 正規表現が無効です: {e}")
        return 0
        
    deleted = 0
    checked = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            checked += 1
            if regex.search(file):
                try:
                    os.remove(os.path.join(root, file))
                    deleted += 1
                    print(f"      削除: {file}")
                except Exception as e:
                    print(f"      警告: {file} の削除に失敗しました: {e}")
    
    if checked > 0:
        print(f"    パターン処理: {checked}個確認, {deleted}個削除")
    return deleted


def process_archive(archive_path: str, modifier_func: Callable[[str], int]) -> int:
    """7zアーカイブを解凍・変更・再圧縮する共通処理"""
    archive_dir = os.path.dirname(archive_path)
    archive_name = os.path.basename(archive_path)
    base_name = os.path.splitext(archive_name)[0]
    extract_dir = os.path.join(archive_dir, f"_tmp_{int(time.time())}_{base_name[:10]}")
    backup_path = archive_path + '.bak'
    
    deleted_count = 0
    try:
        # 解凍
        try:
            extract_7z(archive_path, extract_dir)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  ✗ 解凍エラー: 7zコマンドが実行できないか、ファイルが壊れています")
            return 0
        
        # 変更処理
        deleted_count = modifier_func(extract_dir)
        
        if deleted_count > 0:
            # バックアップ作成
            shutil.copy2(archive_path, backup_path)
            # 元ファイルを削除
            safe_remove(archive_path)
            # 再圧縮
            try:
                compress_7z(archive_path, extract_dir)
                # 成功したらバックアップ削除
                safe_remove(backup_path)
            except Exception as e:
                print(f"  ✗ 再圧縮エラー: {e}")
                if os.path.exists(backup_path):
                    if os.path.exists(archive_path):
                        safe_remove(archive_path)
                    os.rename(backup_path, archive_path)
                return 0
            
        return deleted_count

    except Exception as e:
        print(f"\n    ✗ エラー ({archive_name}): {e}")
        if os.path.exists(backup_path):
            if os.path.exists(archive_path):
                safe_remove(archive_path)
            os.rename(backup_path, archive_path)
        return 0
    finally:
        safe_rmtree(extract_dir)


def run_cleanup(target_dir: str, pattern: str, min_pixel_size: int = 512, dry_run: bool = False):
    """クリーンアップ処理の実行"""
    print(f"\n{'='*60}")
    print(f"対象ディレクトリ: {target_dir}")
    print(f"削除パターン: {pattern}")
    print(f"最小ピクセルサイズ: {min_pixel_size}")
    if dry_run:
        print("[ドライランモード] 実際の削除は行われません")
    print(f"{'='*60}\n")

    # 1. 通常フォルダのクリーンアップ
    print("[1/2] 通常フォルダのクリーンアップ中...")
    if dry_run:
        print("  (ドライランのためスキップ)")
        local_deleted = 0
    else:
        p_del = delete_by_pattern_in_dir(target_dir, pattern)
        img_del = delete_small_pngs_in_dir(target_dir, min_pixel_size)
        local_deleted = p_del + img_del
        print(f"  ✓ 完了: {local_deleted}個削除 (パターン:{p_del}, PNG:{img_del})")

    # 2. 7zアーカイブのクリーンアップ
    print("\n[2/2] 7zアーカイブのクリーンアップ中...")
    archives = find_7z_files(target_dir)
    if not archives:
        print("  7zファイルは見つかりませんでした。")
        archive_deleted = 0
    else:
        archive_deleted = 0
        for i, arc_path in enumerate(archives, 1):
            arc_name = os.path.basename(arc_path)
            print(f"  【{i}/{len(archives)}】 {arc_name} ...", end=" ", flush=True)
            
            if dry_run:
                print("スキップ")
                continue
                
            def modifier(d):
                return delete_by_pattern_in_dir(d, pattern) + delete_small_pngs_in_dir(d, min_pixel_size)
                
            count = process_archive(arc_path, modifier)
            archive_deleted += count
            print(f"完了 ({count}個削除)")

    print(f"\n{'='*60}")
    print(f"最終結果:")
    print(f"  通常フォルダ: {local_deleted}個削除")
    print(f"  7zアーカイブ内: {archive_deleted}個削除")
    print(f"  合計: {local_deleted + archive_deleted}個削除")
    print(f"{'='*60}")


if __name__ == "__main__":
    # 7zコマンドの存在確認
    try:
        subprocess.run(['7z'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("エラー: '7z' コマンドが見つかりません。7-Zipをインストールし、PATHを通してください。")
        sys.exit(1)

    # ターゲットディレクトリの取得
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = input("対象フォルダパスを入力してください: ").strip('\"').strip("'")
    
    if not os.path.exists(target_dir):
        print(f"エラー: フォルダが見つかりません: {target_dir}")
        sys.exit(1)

    # 設定
    pattern = "grid.*"
    min_pixel_size = 512
    
    # 実行確認
    confirm = input(f"'{target_dir}' 内のクリーンアップを開始しますか？ (y/n): ").lower().strip()
    if confirm != 'y':
        print("キャンセルしました。")
        sys.exit(0)

    run_cleanup(target_dir, pattern, min_pixel_size, dry_run=False)

