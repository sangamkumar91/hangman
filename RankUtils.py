
class RankUtils:
    @staticmethod
    def find_next_guess(word_list, guessed_chars):
        rank_list_each_word = []
        for word in word_list:
            if not word.filled:
                ranks = RankUtils.get_rankings_for_word(RankUtils.get_search_complexity(word.word),
                                                        word.relevant_words, guessed_chars)
                rank_list_each_word.append(ranks)
        rank_list_each_word = zip(*rank_list_each_word)
        merged_ranks = list(map(RankUtils.get_merged_ranks, rank_list_each_word))

        return sorted(merged_ranks, key=lambda tup: tup[1], reverse=True)[0][0]

    @staticmethod
    def get_merged_ranks(score):
        sum = 0
        for x in score:
            sum += x[1]
        return score[0][0], sum

    @staticmethod
    def get_search_complexity(word):
        return (len(word) - word.count('_'))/len(word)

    @staticmethod
    def get_rankings_for_word(word_complexity, word_results, guessed_chars):
        char_rank_list = []
        for i in range(26):
            if chr(65 + i) not in guessed_chars:
                char_rank_list.append((chr(65 + i), RankUtils.get_character_ranking(chr(65 + i), word_results) * word_complexity))
        return char_rank_list

    @staticmethod
    def get_character_ranking(character, word_results):
        if len(word_results) == 0:
            return 0
        else:
            filtered_list = list(filter(lambda word: character.lower() in word.word, word_results))
            score = 0
            for filtered_word in filtered_list:
                score = score + filtered_word.score
            return score
