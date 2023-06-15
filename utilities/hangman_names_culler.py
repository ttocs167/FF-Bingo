# loads a txt of names and a txt of words, and removes any names from the words list

with open(r'C:\Users\ttocs\PycharmProjects\FF Bingo\resources\hangman\es_long_words.txt', 'r', encoding='latin-1') as f:
    words = f.read().splitlines()

# loads the names as lowercase
with open(r'C:\Users\ttocs\PycharmProjects\FF Bingo\resources\hangman\names.txt', 'r', encoding='utf-8') as f:
    names = f.read().splitlines()
    names = [name.lower() for name in names]

for word in words:
    if word in names:
        print(word)
        words.remove(word)

with open(r'C:\Users\ttocs\PycharmProjects\FF Bingo\resources/hangman/es_long_words.txt', 'w', encoding='latin-1') as f:
    for word in words:
        f.write(word + '\n')
