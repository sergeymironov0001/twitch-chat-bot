import getopt
import sys
import configparser

from twitchchatbot import TwitchWordsCounterBot


def main(argv):
    server, port, channel, nickname, password = read_command_line_args(argv)
    print("server: %s, port: %d, channel: %s, nickname: %s" % (server, port, channel, nickname))
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

    server = "irc.chat.twitch.tv"
    port = 6667
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

    try:
        server = conf.get("Connection", "Server")
    except configparser.NoOptionError:
        server = ""

    try:
        port = int(conf.get("Connection", "Port"))
    except configparser.NoOptionError:
        port = ""

    try:
        channel = "#" + conf.get("Connection", "Channel")
    except configparser.NoOptionError:
        print("Channel not defined in the ini file.")
        exit(2)

    try:
        nickname = conf.get("Connection", "Nickname")
    except configparser.NoOptionError:
        print("Nickname not defined in the ini file.")
        exit(2)

    try:
        password = conf.get("Connection", "Password")
    except configparser.NoOptionError:
        print("Password not defined in the ini file.")
        exit(2)

    return server, port, channel, nickname, password


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
