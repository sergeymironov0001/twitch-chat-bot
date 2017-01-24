import logging

import irc.bot
import irc.strings

from twitchchatbot.commands import HelpCommand
from twitchchatbot.commands import TopUsedWordsCommand
from twitchchatbot.words_counter import WordsCounter


class TwitchWordsCounterBot(irc.bot.SingleServerIRCBot):
    """ The class of twitch chat bot which counts used words in the chat and
    supports several commands:
    1. !help - returns all available commands of the chat bot
    2. !top_words - returns top used words in the chat
    """

    def __init__(self, server, port, channel, nickname, password):
        """
        :param server: - twitch chat server
        :param port: - twitch chat server port
        :param channel: - twitch channel
        :param nickname: - bot nickname
        :param password: - bot token
        """
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.server = server
        self.channel = channel
        self.words_counter = WordsCounter()
        self.commands_map = {}
        self.__register_default_commands()

    def __register_default_commands(self):
        """ Method register default chat commands for the bot.
        """
        self.add_command(HelpCommand(self.commands_map))
        self.add_command(TopUsedWordsCommand(self.words_counter))
        # TODO add new default chat commands here

    def add_command(self, command):
        """ Add a chat command to the bot.

        :param command: instance of a class which is children of the twitchchatbot.commands.Command class.
        """
        self.commands_map[command.get_name()] = command

    def remove_command(self, command_name):
        """ Remove a chat command from the bot.

        :param command_name: - name of a command. If command with the name not found
        in the bot method will do nothing
        """
        if command_name in self.commands_map:
            del self.commands_map[command_name]

    def start(self):
        """ Start the bot.
        """
        logging.info("Connecting to the server '%s'..." % self.server)
        super(TwitchWordsCounterBot, self).start()

    def on_welcome(self, connection, event):
        """ Method will be called automatically after connecting to the twitch chat server.

        :param connection:
        :param event:
        """
        logging.info("Connected to the server '%s'." % self.server)
        logging.info("Joining to the channel '%s'..." % self.channel)
        connection.join(self.channel)

    def _on_join(self, connection, event):
        """ Method will be called automatically after joining to the twitch channel.

        :param connection:
        :param event:
        :return:
        """
        super(TwitchWordsCounterBot, self)._on_join(connection, event)
        logging.info("Joined to the channel '%s'!" % self.channel)

    def _on_disconnect(self, connection, event):
        """ Method will be called automatically after disconnecting from the twitch chat server.

        :param connection:
        :param event:
        :return:
        """
        super(TwitchWordsCounterBot, self)._on_disconnect(connection, event)
        logging.info("Disconnected from the server '%s'." % self.server)

    def on_pubmsg(self, connection, event):
        """ Method will be called automatically after receiving public message from the chat.

        :param connection:
        :param event:
        :return:
        """
        message = event.arguments[0]
        channel = event.target
        command = self.commands_map.get(message)
        if command is not None:
            logging.info("Received command \'%s\' from the user \'%s\'" % (command, event.source.user))
            command.execute(connection, channel)
        else:
            self.words_counter.count_words(message)
