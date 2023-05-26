import random
import os


def load_word_list(language='en'):
    if language == 'es':
        encoding = "latin-1"
    else:
        encoding = "utf-8"

    filepath = 'resources/hangman/{}_long_words.txt'.format(language)

    if not os.path.exists(filepath):
        raise FileNotFoundError("File '{}' not found.".format(filepath))

    with open('resources/hangman/{}_long_words.txt'.format(language), 'r', encoding=encoding) as f:
        words = f.read().splitlines()
    return words


def generate_random_word(language='en'):
    word = random.choice(load_word_list(language)).lower()
    return word


def set_up_game(word):
    word_list = list(word)
    word_length = len(word_list)
    word_list = [' _ ' for _ in range(word_length)]
    return word_list


class Hangman:
    def __init__(self, language='en'):
        self.word = generate_random_word(language)
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
            response_text = None
        else:
            self.guesses -= 1
            success = False
            response_text = "That's not in the word"
        return success, self.word_list, response_text

    def guess_word(self, guess):
        if guess == self.word:
            success = True
            complete = True
            response_text = "Correct!"

        else:
            self.guesses -= 1
            success = False
            complete = False
            response_text = "That's not the word!"

        return success, self.word_list, response_text, complete

    def reset_game(self, language='en'):
        self.word = generate_random_word(language)
        self.word_list = set_up_game(self.word)
        self.guesses = self.max_guesses
        self.guessed_letters = set()

    def reset_guesses(self):
        self.guesses = self.max_guesses

