"""Pinbot

Usage:
    pinbot -c <config>

Options:
    -h --help           show this screen
    -v --version        show version
"""
from docopt import docopt
from pyaib.ircbot import IrcBot

args = docopt(__doc__, version="0.1.0")
bot = IrcBot(args["<config>"])
bot.run()
