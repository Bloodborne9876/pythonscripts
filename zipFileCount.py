import os
import zipfile
from pathlib import Path

def get_zip_contents(zip_path):
    """zipファイルの内容を取得する"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        return len(zip_ref.namelist())

def get_valid_folder_path():
    """有効なフォルダパスを取得する"""
    while True:
        folder_path = input("フォルダパスを入力してください: ")
        if os.path.exists(folder_path):
            if os.path.isdir(folder_path):
                return folder_path
            else:
                print("エラー: 入力されたパスはフォルダではありません。")
        else:
            print("エラー: 指定されたフォルダが見つかりません。")

def main():
    # 有効なフォルダパスを取得
    folder_path = get_valid_folder_path()
    
    # 結果を格納するリスト
    results = []
    
    # フォルダ内のすべてのフォルダを取得
    total_files = 0
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            file_count = len([f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))])
            total_files += file_count
            result = f"フォルダ: {item} - {file_count}ファイル\n"
            results.append(result)
            print(result, end='')
    
    # 合計ファイル数を追加
    total_result = f"\n合計ファイル数: {total_files}\n"
    results.append(total_result)
    print(total_result)
    
    # 結果をファイルに保存
    if results:
        parent_folder = str(Path(folder_path).parent)
        folder_name = os.path.basename(folder_path)
        output_file = os.path.join(parent_folder, f"{folder_name}_詳細.txt")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("".join(results))
            print(f"\n結果を保存しました: {output_file}")
        except Exception as e:
            print(f"エラー: 結果の保存に失敗しました。\n{str(e)}")
if __name__ == "__main__":
    main()