import unittest
from unittest import mock

from wordscounterbot import HelpCommand
from wordscounterbot import TopUsedWordsCommand
from wordscounterbot import WordsCounter


class HelpCommandTests(unittest.TestCase):
    def setUp(self):
        self.commands_map = {}
        self.help_command = HelpCommand(self.commands_map)
        self.connection_mock = mock.Mock()
        self.channel_mock = mock.Mock()

    def test_get_name_returns_correct_string(self):
        self.assertEqual('!help', self.help_command.get_name())

    def test_execute_returns_correct_commands_list_for_one_command(self):
        self.commands_map['!command'] = ''
        self.help_command.execute(self.connection_mock, self.channel_mock)
        self.connection_mock.privmsg.assert_called_with(self.channel_mock, '[available commands: !command]')

    def test_execute_returns_correct_commands_list_for_several_commands(self):
        self.commands_map['!command2'] = ''
        self.commands_map['!command1'] = ''
        self.help_command.execute(self.connection_mock, self.channel_mock)
        self.connection_mock.privmsg.assert_called_with(self.channel_mock, '[available commands: !command1, !command2]')


class TopUsedWordsCommandTests(unittest.TestCase):
    def setUp(self):
        self.words_counter = WordsCounter()
        self.top_used_words_command = TopUsedWordsCommand(self.words_counter)
        self.connection_mock = mock.Mock()
        self.channel_mock = mock.Mock()

    def test_get_name_returns_correct_value(self):
        self.assertEqual('!top_words', self.top_used_words_command.get_name())

    def test_execute_returns_correct_message_if_no_words_used(self):
        self.top_used_words_command.execute(self.connection_mock, self.channel_mock)
        self.connection_mock.privmsg.assert_called_with(self.channel_mock, '[words haven\'t been counted yet]')

    def test_execute_returns_correct_message_if_less_when_10_different_words_used(self):
        self.words_counter.count_words('5 4 3 2 1 1 1 2')
        self.top_used_words_command.execute(self.connection_mock, self.channel_mock)
        self.connection_mock.privmsg.assert_called_with(self.channel_mock,
                                                        '[[ 1 : 3 ][ 2 : 2 ][ 3 : 1 ][ 4 : 1 ][ 5 : 1 ]]')

    def test_execute_returns_message_with_top_10_words_if_more_when_10_different_words_used(self):
        self.words_counter.count_words('999 99 9 8 7 6 5 4 1 5 3 2 1 1 1')
        self.top_used_words_command.execute(self.connection_mock, self.channel_mock)
        self.connection_mock.privmsg.assert_called_with(self.channel_mock,
                                                        '[[ 1 : 4 ][ 5 : 2 ][ 2 : 1 ][ 3 : 1 ][ 4 : 1 ]'
                                                        '[ 6 : 1 ][ 7 : 1 ][ 8 : 1 ][ 9 : 1 ][ 99 : 1 ]]')
