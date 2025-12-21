import os
import sys
import subprocess

def convert_images(root_dir, src_ext, dst_ext, is_test=False, delete_original=False):
    # 拡張子の正規化（ドットなしの小文字に統一）
    src_ext = src_ext.lower().lstrip('.')
    dst_ext = dst_ext.lower().lstrip('.')
    
    src_dot_ext = f".{src_ext}"
    
    count = 0
    
    # os.walkで再帰的に探索
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(src_dot_ext):
                src_path = os.path.join(dirpath, filename)
                
                # 拡張子を除いたファイル名を取得して、新しい拡張子を付与
                base_name = os.path.splitext(filename)[0]
                dst_filename = f"{base_name}.{dst_ext}"
                dst_path = os.path.join(dirpath, dst_filename)
                
                # 変換先ファイルが既に存在する場合はスキップ（上書き防止）
                if os.path.exists(dst_path):
                    print(f"Skip: {dst_path} は既に存在します。")
                    continue

                if is_test:
                    print(f"[TEST] Would convert: {src_path} -> {dst_path}")
                    if delete_original:
                        print(f"[TEST] Would delete original: {src_path}")
                    count += 1
                else:
                    print(f"Converting: {src_path} -> {dst_path}")
                    try:
                        # ImageMagickコマンドの構築
                        # Windows環境では 'magick' コマンドを使用するのが一般的 (v7以降)
                        # v6以前の場合は 'convert' ですが、Windows標準コマンドと競合するため注意が必要
                        cmd = ["magick", src_path, dst_path]
                        
                        # コマンド実行
                        subprocess.run(cmd, check=True, capture_output=True)
                        
                        if delete_original:
                            print(f"Deleting original: {src_path}")
                            os.remove(src_path)

                        count += 1
                    except subprocess.CalledProcessError as e:
                        print(f"Error converting {src_path}: {e}")
                        if e.stderr:
                            try:
                                print(f"Stderr: {e.stderr.decode('utf-8', errors='ignore')}")
                            except:
                                pass
                    except FileNotFoundError:
                        print("Error: 'magick' コマンドが見つかりません。ImageMagickがインストールされ、PATHが通っているか確認してください。")
                        return

    if is_test:
        print(f"テスト完了: {count} 個のファイルが変換対象です。")
    else:
        print(f"完了: {count} 個のファイルを変換しました。")

if __name__ == "__main__":
    # 1. フォルダパスの取得
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        print("指定したフォルダ以下の画像ファイルをImageMagickを使って変換します。")
        target_dir = input("検索対象のフォルダパスを入力してください: ").strip('"').strip("'")
    
    if not os.path.exists(target_dir):
        print(f"指定されたフォルダが存在しません: {target_dir}")
        sys.exit(1)

    # 2. 変換元の拡張子
    src_ext = input("変換元の拡張子を入力してください (例: png): ").strip()
    if not src_ext:
        print("変換元の拡張子は必須です。")
        sys.exit(1)

    # 3. 変換先の拡張子
    dst_ext = input("変換先の拡張子を入力してください (例: jpg): ").strip()
    if not dst_ext:
        print("変換先の拡張子は必須です。")
        sys.exit(1)

    # 4. テストモードの確認
    is_test = False
    while True:
        mode_input = input("テストモードで実行しますか？ (y/n) [y]: ").lower().strip()
        if mode_input == '' or mode_input == 'y' or mode_input == 'yes':
            is_test = True
            break
        elif mode_input == 'n' or mode_input == 'no':
            is_test = False
            break
        else:
            print("y または n を入力してください。")

    # 5. 元ファイル削除の確認
    delete_original = False
    while True:
        del_input = input("変換後に元ファイルを削除しますか？ (y/n) [n]: ").lower().strip()
        if del_input == 'y' or del_input == 'yes':
            delete_original = True
            break
        elif del_input == '' or del_input == 'n' or del_input == 'no':
            delete_original = False
            break
        else:
            print("y または n を入力してください。")

    convert_images(target_dir, src_ext, dst_ext, is_test=is_test, delete_original=delete_original)
