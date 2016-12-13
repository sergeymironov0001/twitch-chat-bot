import irc.bot
import irc.strings

from .words_counter import WordsCounter


class TwitchWordsCounterBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, password, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.server = server
        self.channel = channel
        self.words_counter = WordsCounter()

    def start(self):
        print("Connecting to the server '%s'..." % self.server)
        super(TwitchWordsCounterBot, self).start()

    def on_welcome(self, c, e):
        print("Connected to the server '%s'." % self.server)
        print("Joining to the channel '%s'..." % self.channel)
        c.join(self.channel)

    def _on_join(self, c, e):
        super(TwitchWordsCounterBot, self)._on_join(c, e)
        print("Joined to the channel '%s'!" % self.channel)

    def _on_disconnect(self, c, e):
        super(TwitchWordsCounterBot, self)._on_disconnect(c, e)
        print("Disconnected from the server '%s'." % self.server)
        print(e)

    def on_pubmsg(self, c, e):
        message = e.arguments[0]
        self.words_counter.count_words(message)
        print(self.words_counter)
