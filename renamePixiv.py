import os
import sys

def rename_pixiv_folders(root_dir, is_test=False):
    target_folders = []
    
    # まずは対象フォルダを探索
    # os.walkで探索。ディレクトリ構造を変更するため、リストアップしてから処理する
    for dirpath, dirnames, filenames in os.walk(root_dir, True):
        # 大文字小文字を区別せずに 'pixiv' を含むフォルダを探す
        for dirname in dirnames:
            if 'pixiv' in dirname.lower():
                # pixivフォルダのフルパス
                pixiv_path = os.path.join(dirpath, dirname)
                target_folders.append(pixiv_path)

    if not target_folders:
        print("pixivフォルダは見つかりませんでした。")
        return

    # リネーム処理
    count = 0
    for pixiv_path in target_folders:
        parent_dir = os.path.dirname(pixiv_path)
        parent_name = os.path.basename(parent_dir)
        current_folder_name = os.path.basename(pixiv_path)
        
        # 既に親フォルダ名で始まっている場合はスキップ（重複付与防止）
        if current_folder_name.startswith(f"{parent_name}_"):
            continue

        # 親フォルダ名_元のフォルダ名 という名前にする
        new_name = f"{parent_name}_{current_folder_name}"
        new_path = os.path.join(parent_dir, new_name)

        # 既に同名のフォルダが存在する場合はスキップするなど考慮が必要だが
        # 今回は単純にリネームを試みる
        if os.path.exists(new_path):
            print(f"Skip: {new_path} は既に存在します。")
            continue

        if is_test:
            print(f"[TEST] Would rename: {pixiv_path} -> {new_path}")
            count += 1
        else:
            print(f"Renaming: {pixiv_path} -> {new_path}")
            try:
                os.rename(pixiv_path, new_path)
                count += 1
            except Exception as e:
                print(f"Error renaming {pixiv_path}: {e}")
            
    if is_test:
        print(f"テスト完了: {count} 個のフォルダが変更対象です。")
    else:
        print(f"完了: {count} 個のフォルダ名を変更しました。")

if __name__ == "__main__":
    # 引数でパスが渡されればそれを使用、なければ入力を求める
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        print("指定したフォルダ以下の 'pixiv' フォルダを '親フォルダ名_pixiv' にリネームします。")
        target_dir = input("検索対象のフォルダパスを入力してください: ").strip('"').strip("'")
    
    if os.path.exists(target_dir):
        # テストモードの確認
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

        rename_pixiv_folders(target_dir, is_test=is_test)
    else:
        print(f"指定されたフォルダが存在しません: {target_dir}")
