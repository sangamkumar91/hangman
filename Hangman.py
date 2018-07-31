import time
import os

import requests
from requests import RequestException

from DataMuseWordFetcher import DataMuseWordFetcher
from Gallow import Gallow
from RankUtils import RankUtils
from Word import Word


class Hangman:

    INIT_URL = '{}/play'.format(os.environ['HANGMAN_URL'])
    GALLOW_URL = INIT_URL + '?token={}&guess={}'
    MOST_FREQUENT = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'H']

    def __init__(self):
        print("Starting Game")
        self.gallow = None
        self.parse_gallow(Hangman.INIT_URL)
        self.words = list()
        self.guess_list = list()
        self.word_fetcher = DataMuseWordFetcher()

        self.next_guess_char = None # Remove

    def begin(self):
        print(self.gallow)
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
        self.parse_gallow(Hangman.GALLOW_URL.format(self.gallow.token, next_guess_char))
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
        print("Warming up.")
        index = 0
        self.parse_gallow(Hangman.GALLOW_URL.format(self.gallow.token, Hangman.MOST_FREQUENT[index]))
        print(self.gallow)
        self.guess_list.append(Hangman.MOST_FREQUENT[index])
        index += 1
        self.parse_gallow(Hangman.GALLOW_URL.format(self.gallow.token, Hangman.MOST_FREQUENT[index]))
        print(self.gallow)
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
