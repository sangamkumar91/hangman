import requests
import time

from requests import RequestException
from Gallow import Gallow
from Word import Word
from DataMuseWordFetcher import DataMuseWordFetcher
from RankUtils import RankUtils


class Hangman:

    EMAIL = "shantanu27.bits@gmail.com"
    INIT_URL = "http://gallows.hulu.com/play?code="
    GALLOW_URL = "http://gallows.hulu.com/play?code={}&token={}&guess={}"
    MOST_FREQUENT = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'H']

    def __init__(self):
        self.gallow = None
        self.parse_gallow(Hangman.INIT_URL + Hangman.EMAIL)
        self.words = list()
        self.guess_list = list()
        self.word_fetcher = DataMuseWordFetcher()

        self.next_guess_char = None # Remove

    def begin(self):
        self.warmup()
        self.init_words()
        while self.check_game_complete_state() is False:
            self.word_fetcher.fetch_relevant_words(words=self.words)
            self.do_next_guess()
        return self.check_gallow_free(), self.gallow.state

    def do_next_guess(self):
        next_guess_char = RankUtils.find_next_guess(self.words, self.guess_list)
        print("Next Guess: {}".format(next_guess_char))
        self.next_guess_char = next_guess_char
        self.parse_gallow(Hangman.GALLOW_URL.format(Hangman.EMAIL, self.gallow.token, next_guess_char))
        self.guess_list.append(next_guess_char)
        self.update_word_params()
        print(self.gallow)

    def update_word_params(self):
        for i, w in enumerate(self.gallow.state.split()):
            self.words[i].update_state(w)

    def init_words(self):
        for word in self.gallow.state.split():
            self.words.append(Word(word))

    def warmup(self):
        index = 0
        self.parse_gallow(Hangman.GALLOW_URL.format(Hangman.EMAIL, self.gallow.token, Hangman.MOST_FREQUENT[index]))
        self.guess_list.append(Hangman.MOST_FREQUENT[index])
        index += 1
        self.parse_gallow(Hangman.GALLOW_URL.format(Hangman.EMAIL, self.gallow.token, Hangman.MOST_FREQUENT[index]))
        self.guess_list.append(Hangman.MOST_FREQUENT[index])

    def parse_gallow(self, url):
        gallow_response = Hangman.request_url(url)
        if self.gallow is None:
            self.gallow = Gallow(gallow_response['status'],
                                 gallow_response['token'],
                                 gallow_response['remaining_guesses'],
                                 gallow_response['state'])
        else:
            self.gallow.status = gallow_response['status']
            self.gallow.token = gallow_response['token']
            self.gallow.rem = gallow_response['remaining_guesses']
            self.gallow.state = gallow_response['state']

    def check_game_complete_state(self):
        return self.check_gallow_dead() or self.check_gallow_free()

    def check_gallow_dead(self):
        return self.gallow.status == "DEAD"

    def check_gallow_free(self):
        return self.gallow.status == "FREE"

    @staticmethod
    def request_url(url):
        while True:
            try:
                r = requests.get(url)
                status_code = r.status_code
                while status_code != 200:
                    r = requests.get(url)
                    status_code = r.status_code
                    time.sleep(10)
                return r.json()
            except RequestException:
                time.sleep(10)
                continue
