import irc.bot
import irc.strings
import re

from twitchchatbot.words_counter import WordsCounter


class TwitchWordsCounterBot(irc.bot.SingleServerIRCBot):
    def __init__(self, server, port, channel, nickname, password):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.server = server
        self.channel = channel
        self.words_counter = WordsCounter()
        self.__command_pattern = re.compile('^![\w]+$', re.UNICODE)

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
        if self.__is_command(message):
            self.__do_command(message, channel)
        else:
            self.words_counter.count_words(message)

    def __is_command(self, message):
        if self.__command_pattern.search(message) is None:
            return False
        else:
            return True

    def __do_command(self, command, channel):
        command = command[1:]
        if "help" == command:
            self.__send_message(channel, "[available commands: !help, !top_words]")
        elif "top_words" == command:
            self.__send_message(channel, "[%s]" % self.words_counter.top_words_to_string())
            # add other commands here

    # Send the message to the target user or to the target channel
    def __send_message(self, target, message):
        self.connection.privmsg(target, message)
