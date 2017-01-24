import configparser
import getopt
import logging.config
import sys

from twitchchatbot.twitch_words_counter_bot import TwitchWordsCounterBot

default_server = "irc.chat.twitch.tv"
default_port = 6667


def main(argv):
    server, port, channel, nickname, password = read_command_line_args(argv)
    logging.info("server: %s, port: %d, channel: %s, nickname: %s" % (server, port, channel, nickname))
    bot = TwitchWordsCounterBot(server, port, channel, nickname, password)
    bot.start()


def read_command_line_args(argv):
    help_message = 'Possible arguments:\n' \
                   '-h - you will get this message\n' \
                   '-s <server> - optional, default value is irc.chat.twitch.tv\n' \
                   '-p <port> - optional, default port is 6667\n' \
                   '-c <channel>\n' \
                   '-n <nickname>\n' \
                   '-k <password>\n' \
                   'Or you can define all connection params in an ini file and pass path to the file via argument:\n' \
                   '--config <ini_file>'
    try:
        opts, args = getopt.getopt(argv, "hs:p:c:n:k:", ["config="])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)

    server = default_server
    port = default_port
    channel = ""
    nickname = ""
    password = ""

    if not opts:
        print(help_message)
        sys.exit()

    for opt, arg in opts:
        if opt in ("-h"):
            print(help_message)
            sys.exit()
        elif opt in ("-s"):
            server = arg
        elif opt in ("-p"):
            port = int(arg)
        elif opt in ("-c"):
            channel = "#" + arg
        elif opt in ("-n"):
            nickname = arg
        elif opt in ("-k"):
            password = arg
        elif opt in ("--config"):
            return read_connection_parameters_from_ini_file(arg)

    return server, port, channel, nickname, password


def read_connection_parameters_from_ini_file(file_name):
    conf = configparser.ConfigParser()
    conf.read(file_name)

    section_name = "connection"
    try:
        server = conf.get(section_name, "server")
    except configparser.NoOptionError:
        server = default_server

    try:
        port = int(conf.get(section_name, "port"))
    except configparser.NoOptionError:
        port = default_port

    try:
        channel = "#" + conf.get(section_name, "channel")
    except configparser.NoOptionError:
        print("Channel not defined in the ini file.")
        exit(2)

    try:
        nickname = conf.get(section_name, "nickname")
    except configparser.NoOptionError:
        print("Nickname not defined in the ini file.")
        exit(2)

    try:
        password = conf.get(section_name, "password")
    except configparser.NoOptionError:
        print("Password not defined in the ini file.")
        exit(2)

    return server, port, channel, nickname, password


if __name__ == '__main__':
    logging.config.fileConfig('./logger.ini')
    sys.exit(main(sys.argv[1:]))
