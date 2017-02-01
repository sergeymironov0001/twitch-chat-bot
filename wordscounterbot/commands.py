""" The module contains implementations twitch chat bot commands.

1. HelpCommand class - !help
2. TopUsedWordsCommand class- !top_words
"""

from twitchchatbot import Command


class HelpCommand(Command):
    """ Command returns all available commands of the chat bot.
        For call the command use '!help' message in the chat.
    """

    def __init__(self, commands_map):
        """
        :param commands_map: dictionary which contains command names as a keys, and instances of classes
        which are children of the Command class as values
        """
        Command.__init__(self, "!help")
        self.__commands_map = commands_map

    def execute(self, connection, channel):
        message = "[available commands: "
        for command_name in sorted(self.__commands_map):
            message += command_name + ", "
        message = message[:-2] + "]"
        connection.privmsg(channel, message)


class TopUsedWordsCommand(Command):
    """ Command returns top used words of the bot's channel
        For call the command use '!top_words' message in the chat.
    """

    def __init__(self, words_counter):
        """
        :param words_counter: instance of the twitchchatbot.words_counter.WordsCounter class
        """
        Command.__init__(self, "!top_words")
        self.__words_counter = words_counter

    def execute(self, connection, channel):
        connection.privmsg(channel, "[%s]" % self.__words_counter.top_words_to_string())
