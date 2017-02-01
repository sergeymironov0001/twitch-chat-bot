""" The module contains parent class for twitch chat bot's commands.

"""


class Command:
    """ Parent class of twitch chat bot commands.
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
