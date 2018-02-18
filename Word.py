class Word:

    def __init__(self, word):
        self.word = word
        self.param = None
        self.relevant_words = list()
        self.filled = False
        self.update_state(word)

    def update_state(self, state):
        self.word = state
        self.param = state
        self.param = self.param.replace('_', '?')
        if '?' not in self.param:
            self.filled = True
