from abc import abstractmethod


class WordFetcher:

    @abstractmethod
    def fetch_relevant_words(self, words):
        pass
