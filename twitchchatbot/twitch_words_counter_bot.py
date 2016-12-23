import irc.bot
import irc.strings

from twitchchatbot.commands import HelpCommand
from twitchchatbot.commands import TopUsedWordsCommand
from twitchchatbot.words_counter import WordsCounter


class TwitchWordsCounterBot(irc.bot.SingleServerIRCBot):
    """
    Twitch chat bot class which counts words used in the channel.
    """

    def __init__(self, server, port, channel, nickname, password):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.server = server
        self.channel = channel
        self.words_counter = WordsCounter()
        self.commands_map = {}
        self.__register_default_commands()

    def __register_default_commands(self):
        self.add_command(HelpCommand(self.commands_map))
        self.add_command(TopUsedWordsCommand(self.words_counter))

    def add_command(self, command):
        self.commands_map[command.get_name()] = command

    def remove_command(self, command_name):
        if command_name in self.commands_map:
            del self.commands_map[command_name]

    def start(self):
        print("Connecting to the server '%s'..." % self.server)
        super(TwitchWordsCounterBot, self).start()

    def on_welcome(self, connection, event):
        print("Connected to the server '%s'." % self.server)
        print("Joining to the channel '%s'..." % self.channel)
        connection.join(self.channel)

    def _on_join(self, connection, event):
        super(TwitchWordsCounterBot, self)._on_join(connection, event)
        print("Joined to the channel '%s'!" % self.channel)

    def _on_disconnect(self, connection, event):
        super(TwitchWordsCounterBot, self)._on_disconnect(connection, event)
        print("Disconnected from the server '%s'." % self.server)
        print(event)

    def on_pubmsg(self, connection, event):
        message = event.arguments[0]
        channel = event.target
        command = self.commands_map.get(message)
        if command is not None:
            command.execute(connection, channel)
        else:
            self.words_counter.count_words(message)
