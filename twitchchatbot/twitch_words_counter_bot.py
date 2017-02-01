from twitchchatbot.commands import HelpCommand
from twitchchatbot.commands import TopUsedWordsCommand
from twitchchatbot.twitch_chat_bot import TwitchChatBot
from twitchchatbot.words_counter import WordsCounter


class TwitchWordsCounterBot(TwitchChatBot):
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
        super(TwitchWordsCounterBot, self).__init__(server, port, channel, nickname, password)
        self.words_counter = WordsCounter()
        self.register_commands()

    def register_commands(self):
        """ Method registers chat commands for the bot.
        """
        self.add_command(HelpCommand(self.commands_map))
        self.add_command(TopUsedWordsCommand(self.words_counter))

    def process_message(self, event, user, message):
        self.words_counter.count_words(message)
