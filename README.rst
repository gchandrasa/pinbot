PinBot
~~~~~~

It began when **Fellowship of The PythonID** discussed about having extra bot.

.. image:: convo.png

Requirements
============

* Python 2.7.x
* `pip <http://www.pip-installer.org/en/latest/>`_ installer

Crash Course
============

Grab the source:

.. sourcecode:: sh

    (venv)$ git clone git://github.com/iromli/pinbot.git
    (venv)$ cd pinbot
    (venv)$ pip install -r requirements.txt

Create a file to store all required configuration:

.. sourcecode:: yaml

    # config.yml
    IRC:
        servers: irc.example.com:6667
        nick: __pinbot__
        user: pinbot
        # password: testing
        realname: "__pinbot__"
        auto_ping: 300

    triggers:
        prefix: "."

    components.load:
        - nickserv
        - /components.db

    plugins:
        base: plugins
        load: remember

    channels:
        autojoin:
            - "#pinbot"

    db:
        url: sqlite:///var/pinbot.db

Afterwards, invoke the following command:

.. sourcecode:: sh

    (venv)$ py pinbot.py -c config.yml
