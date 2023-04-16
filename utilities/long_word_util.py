
def load_word_list(fp):
    with open(fp, 'r', encoding="utf-8") as f:
        words = f.read().splitlines()
    return words


lang_code = "nl"
og_filename = r"C:\Users\ttocs\PycharmProjects\FF Bingo\resources\hangman\dutch.txt"

words = load_word_list(og_filename)

long_words = []
for word in words:
    if len(word) > 3:
        long_words.append(word)

with open(r'C:\Users\ttocs\PycharmProjects\FF Bingo\resources\hangman\/{}_long_words.txt'.format(lang_code), 'w', encoding="utf-8") as fp:
    for word in long_words:
        fp.write("%s\n" % word)
    print("Done")