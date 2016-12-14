# twitch-chat-bot
Simple twitch chat bot which counts words in the chat.

## Details
Project written in Python 3.5 and uses [irs library](https://pypi.python.org/pypi/irc).

## Installation
To install all necessary dependencies use the following command from the root dir of the project:
```
pip install -r requirements.txt
```

## Run
To run twitch chat bot you can use the following command from the root dir:
```
python -m twitchchatbot -c <channel> -n <username> -k <password>
```
For password you should use OAuth Token. It looks like this:
```
oauth:<some_hash_code>
```
If you don't have one, please use [this link](https://twitchapps.com/tmi/) to generate it for your account.

Besides, to run the bot you can put all your params to an .ini file and pass the path to the file via command
line argument like this:
```
python -m twitchchatbot --config <path_to_ini_file>
```
An .ini file should looks like the following:
```
[Connection]
Channel = <channel_name>
Nickname = <nickname>
Password = <password>
```
## Additional details
By default twitch chat bot tries to connect to the __irc.chat.twitch.tv__ server to __6667__ port.
If you want to change it please use this command line arguments: 
```
-s <server> -p <port>
``` 
Or add the following lines to your .ini file: 
```
Server = <server>
Port = <port>
```

## Tests
To run all unit tests use the following command from the root dit of the project:
```
python -m unittest discover tests/ -p '*_tests.py'
```