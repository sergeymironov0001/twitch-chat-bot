import re
import json


class WordsCounter(object):
    """ This class counts used words in phrases and put all info to the usage statistics.
    """

    @classmethod
    def load_from_json(cls, file_name):
        """Method loads words usage statistics from a json file.

        :param file_name: name of a file for loading words usage statistics
        :return: instance of the WordsCounter class
        """
        with open(file_name, 'r') as file:
            return cls(json.load(file))

    def __init__(self, words_map=None):
        """
        :param words_map: dictionary with words usage statistics where key is a word and value is
        the word usage count. Also you can pass None.
        """
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
        """Method counts used words in the phrase and put it to the usage statistics.

        Method converts the phrase to lower case and split by non words characters.
        All used words will be put to the usage statistics.
        :param phrase: phrase to analyze
        """
        phrase = self.__remove_non_word_characters(phrase)
        for word in phrase.split():
            if word:
                self.__count_word(word)

    def get_top_words(self, words_count=10):
        """Get top used words from the usage statistics.

        :param words_count:
        :return:
        """
        top_words = sorted(self.__words_map, key=lambda k: k, reverse=False)
        top_words = sorted(top_words, key=self.__words_map.get, reverse=True)[:words_count]
        return [(word, self.__words_map[word]) for word in top_words]

    def save_to_json(self, file_name):
        """Save words usage statistics to a json file.

        :param file_name: file name where the statistics should be saved
        """
        with open(file_name, 'w') as file:
            json.dump(self.__words_map, file, ensure_ascii=False)

    def __len__(self):
        return len(self.__words_map)

    def top_words_to_string(self, words_count=10):
        """ Method returns top used words as a string from the usage statistics.

        The result string will have the following format.
        [ word1 : word1UsageCount ][ word2 : word1UsageCount ]...
        All words will be sorted by usage count. If two words have the same usage count
        the will be sorted alphabetically.

        If there are no words in the usage statistics the string
        'words haven't been counted yet' will be returned.

        :param words_count: how many words should be included in the result string
        :return: string - all details please see above
        """
        string = ""
        if len(self) == 0:
            string += "words haven't been counted yet"
        else:
            for (word, count) in self.get_top_words(words_count):
                string += ("[ %s : %d ]" % (word, count))
        return string
