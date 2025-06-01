import collections

text = """
arms up , arms wrap tentacles , bukkake, cum on breasts, facial , tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , knees together feet apart, pussy , from below,
arms up , arms wrap tentacles , bukkake, cum on breasts, facial , tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below,
clenched teeth, frown , disgust, looking at viewer, trembling, facial , cum on breasts ,tearing up ,streaming tears ,sobbing ,(trembling:1.3) ,embarrassed , surprised, arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, imminent penetration, tearing up,
arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, legs up , tearing up,
arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, legs up , tearing up, large insertion , one eye closed, frown
arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, legs up , tearing up, large insertion , tentacle sex , vaginal , one eye closed, frown , heavy breathing, (orgasm, ecstasy:1.1), open mouth,
arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, legs up , tearing up, large insertion , tentacle sex , vaginal , one eye closed, frown , heavy breathing, (orgasm, ecstasy:1.1), open mouth, breast sucking,
arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, legs up , tearing up, large insertion , tentacle sex , vaginal , one eye closed, frown , heavy breathing, (orgasm, ecstasy:1.1), open mouth, breast sucking, anal insertion, anal,
looking at viewer, trembling, facial , cum on breasts ,tearing up ,streaming tears ,(trembling:1.3) , arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, legs up , tearing up, large insertion , tentacle sex , vaginal , frown , heavy breathing, (orgasm, trembling, ecstasy:1.3), open mouth, breast sucking, anal insertion, anal, (japanese sound effects:1.2), (uterus:1.2)
looking at viewer, trembling, facial , cum on breasts ,tearing up ,streaming tears ,(trembling:1.3) , arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, legs up , tearing up, large insertion , tentacle sex , vaginal , frown , heavy breathing, (orgasm, trembling, ecstasy:1.3), open mouth, breast sucking, anal insertion, anal, (japanese sound effects:1.2), motion lines , motion blur, tearing up, clenched teeth,
looking at viewer, trembling, facial , cum on breasts ,tearing up ,streaming tears ,(trembling:1.3) , arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, legs up , tearing up, large insertion , tentacle sex , vaginal , frown , heavy breathing, (orgasm, trembling, ecstasy:1.3), open mouth, breast sucking, anal insertion, anal, (japanese sound effects:1.2), motion lines , motion blur, tearing up, open mouth, from above , cum in pussy , (uterus:1.2)
looking at viewer, trembling, facial , cum on breasts ,tearing up ,streaming tears ,(trembling:1.3) , arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, legs up , tearing up, large insertion , tentacle sex , vaginal , frown , heavy breathing, (orgasm, trembling, ecstasy:1.3), open mouth, breast sucking, anal insertion, anal, (japanese sound effects:1.4), motion lines , motion blur, tearing up, open mouth, from below , cum in pussy , (uterus:1.2)
looking at viewer, trembling, facial , cum on breasts , arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, spread legs, legs up , tearing up, large insertion , tentacle sex , vaginal , heavy breathing, (orgasm, trembling, ecstasy:1.3), open mouth, breast sucking, anal insertion, anal, (japanese sound effects:1.4), motion lines , motion blur, open mouth, from below , cum in pussy , (uterus:1.2)
looking at viewer, trembling, facial , cum on breasts ,tearing up ,streaming tears ,(trembling:1.3) , arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, legs up , tearing up, large insertion , tentacle sex , vaginal , frown , heavy breathing, (orgasm, trembling, ecstasy:1.3), open mouth, breast sucking, anal insertion, anal, (japanese sound effects:1.4), motion lines , motion blur, tearing up, open mouth, from below , cum in pussy , (uterus:1.2) , ahegao,
looking at viewer, trembling, facial , cum on breasts ,tearing up ,streaming tears ,(trembling:1.3) , arms up , arms wrap tentacles , bukkake, cum on breasts, tentacles wrap breasts ,legs wrap tentacles ,torso wrap tentacles , pussy , from below, legs up , tearing up, large insertion , tentacle sex , vaginal , frown , heavy breathing, (orgasm, trembling, ecstasy:1.3), open mouth, breast sucking, anal insertion, anal, (japanese sound effects:1.4), motion lines , motion blur, tearing up, open mouth, from below , cum in pussy , (uterus:1.2) , ahegao, pink eyes, heart-shaped pupils,
"""

lines = text.strip().split('\n')
all_words = []
for line in lines:
    words = [word.strip() for word in line.split(',')]
    all_words.extend(words)

word_counts = collections.Counter(all_words)
duplicate_words = set([word for word, count in word_counts.items() if count > 1])

processed_lines = []
for line in lines:
    words = [word.strip() for word in line.split(',')]
    non_duplicate_words = [word for word in words if word not in duplicate_words]
    processed_lines.append(','.join(non_duplicate_words))

duplicate_words_list = sorted(list(duplicate_words))
duplicate_words_string = ','.join(duplicate_words_list)

print("重複を取り除いた文字列:\n")
print('\n'.join(processed_lines))
print("\n重複していた文字列:\n")
print(duplicate_words_string)