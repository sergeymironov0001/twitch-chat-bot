class Command:
    def __init__(self, command_name):
        self.__command_name = command_name

    def get_name(self):
        return self.__command_name

    def execute(self, connection, channel):
        pass

    def __str__(self):
        return self.get_name()


class HelpCommand(Command):
    def __init__(self, commands_map):
        Command.__init__(self, "!help")
        self.__commands_map = commands_map

    def execute(self, connection, channel):
        message = "[available commands: "
        for command_name in self.__commands_map:
            message += command_name + ", "
        message = message[:-2] + "]"
        connection.privmsg(channel, message)


class TopUsedWordsCommand(Command):
    def __init__(self, words_counter):
        Command.__init__(self, "!top_words")
        self.__words_counter = words_counter

    def execute(self, connection, channel):
        connection.privmsg(channel, "[%s]" % self.__words_counter.top_words_to_string())
