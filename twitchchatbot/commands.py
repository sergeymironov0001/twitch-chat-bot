""" The module contains classes for supporting twitch chat bot commands.

The module contains 'Command' class - parent class for all bot's commands
and several command implementations :
1. HelpCommand class - !help
2. TopUsedWordsCommand class- !top_words
"""


class Command:
    """ Parent class of all chat bot's commands.
    """

    def __init__(self, command_name):
        """
        :param command_name: name of the command. This name will be used for call the command
        if message with the command's name will be received from the chat.
        Recommend to use !<command_name> as the pattern for the name.
        """
        self.__command_name = command_name

    def get_name(self):
        """ Method will return the command's name which was passed via constructor.

        :return: string with the command's name
        """
        return self.__command_name

    def execute(self, connection, channel):
        """ Execute command

        :param connection: connection of the chat bot
        :param channel: channel of the chat bot
        """
        pass

    def __str__(self):
        return self.get_name()


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
