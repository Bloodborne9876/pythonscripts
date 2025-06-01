import random
import sys
import pyperclip

def add_prompt_strength(input_string, minimum_elements=3):
    elements = input_string.split(',')
    num_elements = random.randint(minimum_elements, len(elements))
    selected_elements = random.sample(elements, num_elements)
    result = []
    for element in selected_elements:
        strength = round(random.uniform(0.8, 1.3), 1)
        if strength != 1:
            result.append(f"({element}:{strength})")
        else:
            result.append(element)
    return ','.join(result)

def is_valid_input(input_string):
    return ',' in input_string and len(input_string.split(',')) > 1

def main():
    input_string = ""
    minimum_elements = -1

    if len(sys.argv) > 2:
        minimum_elements = int(sys.argv[2])
    
    print("カンマ区切りの文字列を入力してください")
    while True:
        if len(sys.argv) > 1:
            input_string = sys.argv[1]
            if is_valid_input(input_string):
                break
            print("コマンドライン引数が不正です: カンマ区切りで2つ以上の要素が必要です")
            print("Invalid command-line argument: Requires comma-separated string with at least 2 elements")
            sys.exit(1)
        else:
            print("カンマ区切りで文字列を入力してください (例: cat,dog,bird):")
            input_string = input().strip()
            if is_valid_input(input_string):
                break
    if minimum_elements < 3:  # Only ask if not set from command line
        try:
            print("最小要素数を入力してください (デフォルト: 3):")
            input_min = input().strip()
            if input_min:
                minimum_elements = int(input_min)
        except ValueError:
            print("不正な入力です。デフォルト値の3を使用します。")
            minimum_elements = 3
    all_outputs = []
    for _ in range(20):
        output_string = add_prompt_strength(input_string, minimum_elements)
        print(output_string)
        all_outputs.append(output_string)
    
    # Copy all outputs to clipboard, separated by newlines
    pyperclip.copy('\n'.join(all_outputs))

if __name__ == "__main__":
    main()
    