import logging

import irc.bot
import irc.strings


class TwitchChatBot(irc.bot.SingleServerIRCBot):
    """ The base class of twitch chat bot.

     The implementation supports chat commands.
    """

    @staticmethod
    def get_message_from_event(event):
        return event.arguments[0]

    @staticmethod
    def get_channel_from_event(event):
        return event.target

    @staticmethod
    def get_user_from_event(event):
        return event.source.user

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
        self.commands_map = {}

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
        super(TwitchChatBot, self).start()

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
        super(TwitchChatBot, self)._on_join(connection, event)
        logging.info("Joined to the channel '%s'!" % self.channel)

    def _on_disconnect(self, connection, event):
        """ Method will be called automatically after disconnecting from the twitch chat server.

        :param connection:
        :param event:
        :return:
        """
        super(TwitchChatBot, self)._on_disconnect(connection, event)
        logging.info("Disconnected from the server '%s'." % self.server)

    def on_pubmsg(self, connection, event):
        """ Method will be called automatically after receiving public message from the chat.

        :param connection:
        :param event:
        :return:
        """
        message = TwitchChatBot.get_message_from_event(event)
        if self._is_command(message):
            self._execute_command(connection, event)
        else:
            self.process_message(event, TwitchChatBot.get_user_from_event(event), message)

    def _execute_command(self, connection, event):
        """ Method to execute chat commands.

        :param connection:
        :param event:
        :return:
        """

        command = self._get_command_by_message(self.get_message_from_event(event))
        logging.info("Received command \'%s\' from the user \'%s\'"
                     % (command, TwitchChatBot.get_user_from_event(event)))
        command.execute(connection, TwitchChatBot.get_channel_from_event(event))

    def process_message(self, event, user, message):
        """ Method to process messages.

            The method is called automatically if received message not a command.
            Don't use this method to process commands. For this purpose you
            can use the _execute_command method.

              :param event:
              :param user: who sent the message
              :param message: chat message
              :return:
              """
        pass

    def _is_command(self, message):
        """ Method checks is the message a chat command or not.

        :param message: chat message
        :return: True or False
        """
        return self.commands_map.get(message) is not None

    def _get_command_by_message(self, message):
        """ Method returns a command object by chat message.

        :param message: chat message
        :return: Instance of twitchchatbot.commands.Command subclass
        or None if command was not found.
        """
        return self.commands_map.get(message)
