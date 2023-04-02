import random

def load_word_list(language='en'):
    with open('resources/hangman/{}_long_words.txt'.format(language), 'r') as f:
        words = f.read().splitlines()
    return words


def generate_random_word(language='en'):
    word = random.choice(load_word_list(language)).lower()
    return word


def set_up_game(word):
    word_list = list(word)
    word_length = len(word_list)
    word_list = ['_ ' for _ in range(word_length)]
    return word_list


class Hangman:
    def __init__(self):
        self.word = generate_random_word()
        self.word_list = set_up_game(self.word)
        self.max_guesses = 6
        self.guesses = self.max_guesses
        self.guessed_letters = set()

    def guess_letter(self, letter):
        assert len(letter) == 1, "You can only guess one letter at a time."

        if letter in self.guessed_letters:
            return False, self.word_list, "you already guessed that letter"

        self.guessed_letters.add(letter)

        if letter in self.word:
            for i in range(len(self.word)):
                if letter == self.word[i]:
                    self.word_list[i] = letter

            success = True
        else:
            self.guesses -= 1
            success = False
        return success, self.word_list, None

    def reset_game(self, language='en'):
        self.word = generate_random_word(language)
        self.word_list = set_up_game(self.word)
        self.guesses = self.max_guesses
        self.guessed_letters = set()

    def reset_guesses(self):
        self.guesses = self.max_guesses

