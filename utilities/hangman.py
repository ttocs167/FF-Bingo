import random
import discord

def load_word_list():
    with open('resources/hangman/google-10000-english-no-swears.txt', 'r') as f:
        words = f.read().splitlines()
    return words


def generate_random_word():
    word = random.choice(load_word_list()).lower()
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
        self.guessed_letters = []

    def guess_letter(self, letter):
        assert len(letter) == 1, "You can only guess one letter at a time."

        if letter in self.guessed_letters:
            return False, self.word_list

        letter = letter.lower()
        if letter in self.word:
            for i in range(len(self.word)):
                if letter == self.word[i]:
                    self.word_list[i] = letter

            self.guessed_letters.append(letter)
            success = True
        else:
            self.guesses -= 1
            success = False
        return success, self.word_list

    def reset_game(self):
        self.word = generate_random_word()
        self.word_list = set_up_game(self.word)
        self.guesses = 6
        self.guessed_letters = []

    def reset_guesses(self):
        self.guesses = self.max_guesses

