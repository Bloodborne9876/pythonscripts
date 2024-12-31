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
    
    # zipファイルの存在確認
    zip_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.zip')]
    if not zip_files:
        print("zipファイルが見つかりませんでした。")
        return
    # 指定フォルダ内のzipファイルを検索
    total_files = 0  # 合計ファイル数を追跡
    for file in zip_files:
        try:
            zip_path = os.path.join(folder_path, file)
            file_count = get_zip_contents(zip_path)
            total_files += file_count  # ファイル数を合計に追加
            
            # 結果を追加
            result = f"ファイル名: {file}\nファイル数: {file_count}\n"
            result += "-"*50 + "\n"
            results.append(result)
            
            # 画面に表示
            print(result)
            
        except zipfile.BadZipFile:
            print(f"警告: {file} は破損しているか不正なzipファイルです。")
    
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