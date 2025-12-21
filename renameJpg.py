import os
import sys

def rename_files_in_folder(root_dir, target_ext, is_test=False):
    # 拡張子のドット処理（入力でドットがない場合を考慮）
    if not target_ext.startswith('.'):
        target_ext = '.' + target_ext
    target_ext = target_ext.lower()

    count_total = 0
    
    # os.walkで探索
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 対象拡張子のファイルを抽出
        target_files = [f for f in filenames if f.lower().endswith(target_ext)]
        
        if not target_files:
            continue

        # ファイル名順にソート（リネーム順序を一定にするため）
        target_files.sort()
        
        parent_name = os.path.basename(dirpath)
        
        # ルートディレクトリなどで親フォルダ名が空の場合の対策（通常はないはずだが念のため）
        if not parent_name:
            parent_name = "root"

        # 連番の桁数（ファイルの数に合わせて調整してもいいが、要望の `_***` に合わせて3桁固定にするか、あるいは自動調整か）
        # ここでは最低3桁、ファイル数が多い場合は桁数を増やす実装にする
        digit_len = max(3, len(str(len(target_files))))

        for i, filename in enumerate(target_files, 1):
            old_path = os.path.join(dirpath, filename)
            
            # 新しいファイル名: 親フォルダ名_連番.拡張子
            new_filename = f"{parent_name}_{i:0{digit_len}d}{target_ext}"
            new_path = os.path.join(dirpath, new_filename)
            
            # 既に同じ名前の場合はスキップ（自分自身へのリネームも含む）
            if old_path.lower() == new_path.lower():
                continue
                
            if os.path.exists(new_path) and old_path.lower() != new_path.lower():
                print(f"Skip: {new_path} は既に存在します。")
                continue

            if is_test:
                print(f"[TEST] Would rename: {filename} -> {new_filename} in {dirpath}")
                count_total += 1
            else:
                print(f"Renaming: {filename} -> {new_filename}")
                try:
                    os.rename(old_path, new_path)
                    count_total += 1
                except Exception as e:
                    print(f"Error renaming {old_path}: {e}")

    if is_test:
        print(f"テスト完了: 合計 {count_total} 個のファイルが変更対象です。")
    else:
        print(f"完了: 合計 {count_total} 個のファイル名を変更しました。")

if __name__ == "__main__":
    # 1. フォルダパスの取得
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        print("指定したフォルダ以下のファイルを '親フォルダ名_連番.拡張子' にリネームします。")
        target_dir = input("検索対象のフォルダパスを入力してください: ").strip('"').strip("'")
    
    if not os.path.exists(target_dir):
        print(f"指定されたフォルダが存在しません: {target_dir}")
        sys.exit(1)

    # 2. 拡張子の取得
    ext_input = input("対象の拡張子を入力してください (デフォルト: jpg): ").strip()
    if not ext_input:
        target_ext = "jpg"
    else:
        target_ext = ext_input

    # 3. テストモードの確認
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

    rename_files_in_folder(target_dir, target_ext, is_test=is_test)
