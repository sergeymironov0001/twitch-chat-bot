from distutils.core import setup

install_requires = []

try:
    import configparser
except ImportError:
    install_requires.append('configparser==3.5.0')

try:
    import irc
except ImportError:
    install_requires.append('irc==15.0.5')

setup(name='TwitchChatBot',
      version='1.0',
      description='Simple twitch chat bot for counting used words in the chat',
      author='Sergey Mironov',
      author_email='sergeymironov0001@gmail.com',
      license='MIT',
      url='https://github.com/sergeymironov0001/twitch-chat-bot',
      packages=['twitchchatbot'],
      install_requires=install_requires
      )
