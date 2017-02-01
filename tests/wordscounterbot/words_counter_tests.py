import unittest

from wordscounterbot import WordsCounter


class WordsCounterTests(unittest.TestCase):
    def setUp(self):
        self.words_counter = WordsCounter()

    def test_count_words_counts_words_correct(self):
        self.words_counter.count_words("word2 word1")
        self.assertEqual(self.words_counter.get_top_words(), [("word1", 1), ("word2", 1)])

        self.words_counter.count_words("word3 word3 word2 word3")
        self.assertEqual(self.words_counter.get_top_words(), [("word3", 3), ("word2", 2), ("word1", 1)])

    def test_count_words_does_not_count_non_words_characters(self):
        self.words_counter.count_words(",word2..,word1-+=")
        self.assertEqual(self.words_counter.get_top_words(), [("word1", 1), ("word2", 1)])

        self.words_counter.count_words("word3,word3.word2;word3!")
        self.assertEqual(self.words_counter.get_top_words(), [("word3", 3), ("word2", 2), ("word1", 1)])

    def test_get_top_words_returns_exact_words_number(self):
        self.words_counter.count_words("word2 word1")
        self.assertEqual(self.words_counter.get_top_words(1), [("word1", 1)])
        self.assertEqual(self.words_counter.get_top_words(2), [("word1", 1), ("word2", 1)])

        self.words_counter.count_words("word2")
        self.assertEqual(self.words_counter.get_top_words(1), [("word2", 2)])
        self.assertEqual(self.words_counter.get_top_words(2), [("word2", 2), ("word1", 1)])

        self.words_counter.count_words("word3 word3 word2 word3 word3")
        self.assertEqual(self.words_counter.get_top_words(1), [("word3", 4)])
        self.assertEqual(self.words_counter.get_top_words(2), [("word3", 4), ("word2", 3)])
        self.assertEqual(self.words_counter.get_top_words(3), [("word3", 4), ("word2", 3), ("word1", 1)])
        self.assertEqual(self.words_counter.get_top_words(4), [("word3", 4), ("word2", 3), ("word1", 1)])


if __name__ == '__main__':
    unittest.main()
