import re
import json


class WordsCounter(object):
    @classmethod
    def load_from_file(cls, file_name):
        with open(file_name, 'r') as file:
            return cls(json.load(file))

    def __init__(self, words_map=None):
        self.__non_word_characters_pattern = re.compile('[\W_]+', re.UNICODE)
        if words_map:
            self.__words_map = words_map
        else:
            self.__words_map = {}

    def __count_word(self, word):
        self.__words_map[word.lower()] = self.__words_map.get(word, 0) + 1

    def __remove_non_word_characters(self, phrase):
        return self.__non_word_characters_pattern.sub(' ', phrase)

    def count_words(self, phrase):
        phrase = self.__remove_non_word_characters(phrase)
        for word in phrase.split():
            if word:
                self.__count_word(word)

    def get_top_words(self, words_count=10):
        top_words = sorted(self.__words_map, key=lambda k: k, reverse=False)
        top_words = sorted(top_words, key=self.__words_map.get, reverse=True)[:words_count]
        return [(word, self.__words_map[word]) for word in top_words]

    def save_to_file(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.__words_map, file, ensure_ascii=False)

    def __len__(self):
        return len(self.__words_map)

    def __str__(self):
        string = "============================================================\n"
        string += "Different words count: {}\n".format(len(self))
        string += "==================Top popular words=====================\n"
        for (word, count) in self.get_top_words():
            string += ("[ %s : %d ]\n" % (word, count))
        return string
