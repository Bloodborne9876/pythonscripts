import glob
from os.path import dirname, basename, join, isdir
import os
import sys
from psd_tools import PSDImage

# 生成する際のコマンド
# .\env_small\Scripts\activate
# pyinstaller ClipingLayer.py --onefile --exclude docopt --exclude Pillow --exclude numpy --exclude networkx --exclude attrs --exclude aggdraw --exclude tifffile --exclude scip --exclude lazy-loader --exclude imageio --exclude scikit-image

def main():
    if len(sys.argv) > 1:
        psd_files = sys.argv[1:]
    else:
        print("PSDファイルをドラッグ＆ドロップしてください。")
        return

    total_files = len(psd_files)
    processed_files = 0

    for psd_file in psd_files:
        if not os.path.isfile(psd_file):
            print(f"指定されたファイルが存在しません: {psd_file}")
            continue

        if not psd_file.lower().endswith('.psd'):
            print(f"PSDファイルではありません: {psd_file}")
            continue

        try:
            psd = PSDImage.open(psd_file)
        except Exception as e:
            print(f"PSDファイルの読み込みに失敗しました: {psd_file}, エラー: {e}")
            continue

        output_dir = os.path.join(dirname(psd_file), 'clip')
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        for layer in psd:
            if 'コピー' not in layer.name:
                pil_img = layer.topil()
                outputPath = os.path.join(output_dir, layer.name + "_clip.png")
                pil_img.save(outputPath)
                print(f"保存しました: {outputPath}")

        processed_files += 1
        print(f"処理が終わったファイル数: {processed_files}/{total_files}")

if __name__ == '__main__':
    main()