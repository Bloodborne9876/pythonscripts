import argparse
import logging
import os
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image

# ログ設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class CleanupStats:
    pattern_deleted: int = 0
    small_png_deleted: int = 0
    archives_processed: int = 0
    archives_failed: int = 0

    @property
    def total_deleted(self) -> int:
        return self.pattern_deleted + self.small_png_deleted


def deleteWithRetries(path: Path, retries: int) -> bool:
    """指数バックオフ付きでファイル削除を試行する。"""
    for attempt in range(1, retries + 1):
        try:
            path.unlink()
            logger.info("削除しました: %s", path)
            return True
        except PermissionError:
            if attempt == retries:
                logger.error("削除できませんでした (使用中): %s", path)
                return False
            delay = 0.5 * (2 ** (attempt - 1))
            logger.warning("使用中のため再試行 %s/%s (待機 %.1fs): %s", attempt, retries, delay, path)
            time.sleep(delay)
        except Exception as exc:  # pragma: no cover - safety net
            logger.error("削除エラー %s: %s", path, exc)
            return False
    return False


def imageSize(path: Path) -> Optional[tuple[int, int]]:
    """画像サイズを返す。失敗時は None。"""
    try:
        with Image.open(path) as img:
            return img.size
    except Exception as exc:
        logger.warning("画像読み込みエラー %s: %s", path, exc)
        return None


def deleteReason(path: Path, pattern: re.Pattern[str], min_png_px: int) -> Optional[str]:
    """削除対象なら理由を返す。対象外なら None。"""
    name = path.name
    if pattern.search(name):
        return "pattern"
    if path.suffix.lower() == ".png":
        size = imageSize(path)
        if size:
            width, height = size
            if width <= min_png_px or height <= min_png_px:
                return "small_png"
    return None


def cleanupDirectory(root: Path, pattern: re.Pattern[str], min_png_px: int, retries: int, stats: CleanupStats, skip_archives: bool = True) -> None:
    """フォルダ内のファイルをルールに従い削除する。"""
    for dirpath, _, files in os.walk(root):
        for filename in files:
            path = Path(dirpath) / filename
            if skip_archives and path.suffix.lower() == ".7z":
                continue
            reason = deleteReason(path, pattern, min_png_px)
            if not reason:
                continue
            if deleteWithRetries(path, retries):
                if reason == "pattern":
                    stats.pattern_deleted += 1
                elif reason == "small_png":
                    stats.small_png_deleted += 1


def run7zCommand(args: list[str], cwd: Optional[Path] = None) -> bool:
    """7z.exeを実行し、成功ならTrue。"""
    result = subprocess.run(args, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    if result.returncode == 0:
        return True
    logger.error("7zコマンド失敗 (%s): %s", result.returncode, result.stderr.strip())
    if result.stdout:
        logger.info("7z出力: %s", result.stdout.strip())
    return False


def extractArchive(archive: Path, dest: Path, seven_zip: str) -> bool:
    """7z.exeで展開する。"""
    cmd = [seven_zip, "x", "-y", str(archive), f"-o{dest}"]
    return run7zCommand(cmd)


def compressArchive(source: Path, dest_archive: Path, seven_zip: str) -> bool:
    """7z.exeで圧縮する。"""
    if dest_archive.exists():
        dest_archive.unlink()
    cmd = [seven_zip, "a", "-y", str(dest_archive), "."]
    return run7zCommand(cmd, cwd=source)


def createBackup(archive: Path) -> Path:
    """7zのバックアップを作成する。"""
    suffix = archive.suffix + ".bak"
    backup = archive.with_suffix(suffix)
    counter = 1
    while backup.exists():
        backup = archive.with_suffix(f"{archive.suffix}.bak{counter}")
        counter += 1
    shutil.copy2(archive, backup)
    logger.info("バックアップ作成: %s", backup)
    return backup


def restoreBackup(backup: Path, archive: Path) -> None:
    if backup.exists():
        shutil.copy2(backup, archive)
        logger.info("バックアップから復元しました: %s", backup)


def processArchive(archive: Path, pattern: re.Pattern[str], min_png_px: int, retries: int, stats: CleanupStats, seven_zip: str) -> None:
    backup = createBackup(archive)
    for attempt in range(1, retries + 1):
        logger.info("処理中 %s (%s/%s)", archive, attempt, retries)
        temp_dir = Path(tempfile.mkdtemp(prefix=f"cleanup_{archive.stem}_", dir=str(archive.parent)))
        temp_archive = archive.with_suffix(f"{archive.suffix}.new")
        try:
            if not extractArchive(archive, temp_dir, seven_zip):
                continue
            cleanupDirectory(temp_dir, pattern, min_png_px, retries, stats, skip_archives=False)
            if not compressArchive(temp_dir, temp_archive, seven_zip):
                continue
            os.replace(temp_archive, archive)
            stats.archives_processed += 1
            logger.info("アーカイブ更新完了: %s", archive)
            backup.unlink(missing_ok=True)
            return
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
            if temp_archive.exists():
                temp_archive.unlink(missing_ok=True)
        logger.warning("再試行します: %s", archive)
        restoreBackup(backup, archive)
    logger.error("規定回数失敗: %s", archive)
    stats.archives_failed += 1
    restoreBackup(backup, archive)


def findArchives(root: Path) -> list[Path]:
    archives: list[Path] = []
    for dirpath, _, files in os.walk(root):
        for filename in files:
            if filename.lower().endswith(".7z"):
                archives.append(Path(dirpath) / filename)
    return archives


def runCleanup(target: Path, pattern_text: str, min_png_px: int, retries: int, seven_zip: str) -> CleanupStats:
    compiled_pattern = re.compile(pattern_text, re.IGNORECASE)
    stats = CleanupStats()

    logger.info("フォルダ内のクリーンアップを開始します: %s", target)
    # cleanupDirectory(target, compiled_pattern, min_png_px, retries, stats, skip_archives=True)

    archives = findArchives(target)
    if archives:
        logger.info("7zアーカイブを検出: %s件", len(archives))
    else:
        logger.info("7zアーカイブは見つかりませんでした")

    for archive in archives:
        processArchive(archive, compiled_pattern, min_png_px, retries, stats, seven_zip)

    logger.info(
        "サマリー 削除合計=%s (パターン=%s, PNG=%s), アーカイブ処理=%s, 失敗=%s",
        stats.total_deleted,
        stats.pattern_deleted,
        stats.small_png_deleted,
        stats.archives_processed,
        stats.archives_failed,
    )
    return stats


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="フォルダおよび7z内でパターン一致ファイルと小さなPNGを削除します。")
    parser.add_argument("target", nargs="?", default="D:\\000_Backup\\000_AI\\001_Output", help="対象フォルダパス (省略時は現在のフォルダ)")
    parser.add_argument("--pattern", default="grid.*", help="削除する正規表現パターン (デフォルト: grid.*)")
    parser.add_argument("--min-px", type=int, default=512, help="PNGの幅・高さがこの値以下なら削除 (デフォルト: 512)")
    parser.add_argument("--retries", type=int, default=3, help="ファイル/7z操作の最大リトライ回数")
    parser.add_argument("--7z-path", dest="seven_zip", default="7z", help="7z.exeへのパス (デフォルト: 7z)")
    return parser.parse_args()


def main() -> None:
    try:
        args = parseArgs()
    except SystemExit:
        logger.error("引数が不足しているか不正です。例: python archive_cleanup.py \"C:/path/to/folder\" --pattern \"grid.*\" --min-px 512 --retries 3 --7z-path \"C:/Program Files/7-Zip/7z.exe\"。省略時はカレントフォルダを対象に既定値で実行します。")
        return
    target = Path(args.target).expanduser()
    if not target.is_dir():
        logger.error("フォルダが無効です: %s", target)
        return
    runCleanup(target, args.pattern, args.min_px, args.retries, args.seven_zip)


if __name__ == "__main__":
    main()
