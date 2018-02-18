import requests as re
from requests import RequestException

from RelevantWord import RelevantWord
from WordFetcher import WordFetcher


class DataMuseWordFetcher(WordFetcher):

    API_URL = "https://api.datamuse.com/words?sp={}&max={}&md=f"

    def fetch_relevant_words(self, words, max_results=1000):
        for word in words:
            word.relevant_words = self._get_words(word.param, max_results)

    @staticmethod
    def _get_words(sp, max_results):
        try:
            response = re.get(DataMuseWordFetcher.API_URL.format(sp, max_results))
            if response.status_code == 200:
                response_json = response.json()
                return sorted(list(map(lambda x: DataMuseWordFetcher.parse_relevant_word(x), response_json)),
                              key=lambda x: x.score, reverse=True)[0:10]
        except RequestException as e:
            print("DataMuseWordFetcher seems down!")
            raise e

    @staticmethod
    def parse_relevant_word(x):
        score = float(x['tags'][0].split(':')[1])
        return RelevantWord(x['word'], score)
