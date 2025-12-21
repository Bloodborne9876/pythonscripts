import asyncio
import aiohttp
import os
import re

async def get_tags():
    """
    Danbooru APIからキャラクタータグを取得し、search[name_matches]で指定したタグを含むものを選び、
    括弧内のオプションを除去し、キャラクター名 (タイトル) の形式で tags/star_rail.txt に出力。
    アンダースコアはスペースに置換。
    検索件数が0の場合はファイル保存をスキップ。
    """
    base_url = "https://danbooru.donmai.us/tags.json"
    params = {
        "search[name_matches]": "*star_rail*",
        "search[category]": "4",
        "search[post_count]": ">100",
        "limit": 100,
        "search[order]": "count",
    }

    search_name = params["search[name_matches]"].strip('*').replace('/', '').replace('\\', '')
    output_file = os.path.join("tags", f"{search_name}.txt")

    os.makedirs("tags", exist_ok=True)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(base_url, params=params) as response:
                if response.status != 200:
                    print(f"HTTPエラー: ステータスコード {response.status}")
                    return

                tags = await response.json()

                formatted_tags = []
                
                # ワイルドカードを正規表現のパターンに変換
                title_pattern = search_name.replace('_', ' ').lower()
                
                for tag in tags:
                    tag_name_raw = tag.get('name', '')
                    # アンダースコアをスペースに変換
                    tag_name_space = tag_name_raw.replace('_', ' ')
                    
                    # 括弧内のオプションを除去し、余分なスペースを削除
                    cleaned_tag_name = re.sub(r'\s*\([^)]*\)\s*', ' ', tag_name_space).strip()
                    
                    # 元のタグ名からキャラクター名とタイトルを抽出
                    if tag_name_raw.endswith(f"({search_name})"):
                        character_name = tag_name_raw.rsplit('_', 1)[0].replace('_', ' ')
                        title_name = search_name.replace('_', ' ')
                        formatted_tag = f"{character_name} ({title_name})"
                        formatted_tags.append(formatted_tag)
                        
                    # `search_name`をタグ名に含むが、上記のパターンにマッチしない場合のフォールバック処理
                    elif title_pattern in cleaned_tag_name.lower():
                        # タグ名からタイトル部分（star rail）を分離し、キャラクター名と結合
                        character_name = cleaned_tag_name.lower().replace(title_pattern, '').strip()
                        title_name = title_pattern
                        if character_name:
                            formatted_tag = f"{character_name.title()} ({title_name.title()})"
                            formatted_tags.append(formatted_tag)

                if not formatted_tags:
                    print(f"検索結果が0件のため、{output_file} は作成されませんでした。")
                    return

                with open(output_file, 'w', encoding='utf-8') as f:
                    for tag in formatted_tags:
                        f.write(f"{tag}\n")
                
                print(f"タグを {output_file} に保存しました。総タグ数: {len(formatted_tags)}")
                print("最初の5タグ（プレビュー）:")
                for tag in formatted_tags[:5]:
                    print(f"タグ: {tag}")

        except aiohttp.ClientError as e:
            print(f"ネットワークエラーが発生しました: {e}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    asyncio.run(get_tags())