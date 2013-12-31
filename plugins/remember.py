from pyaib.plugins import (
    keyword,
    observe,
)
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint

#: a base model that should be inherited by all submodels,
#: in order to be mapped into SQLAlchemy session automatically
Model = declarative_base()


class Remember(Model):
    """Acts as mapper for a database's table to manage keywords.
    """

    __tablename__ = "remember"
    __table_args__ = (
        UniqueConstraint("channel", "slug", name="uniq_chan_slug"),
    )

    id = Column(Integer, primary_key=True)
    channel = Column(String, index=True)
    user = Column(String)
    slug = Column(String)
    content = Column(Text)


@keyword("remember")
def remember(ctx, msg, trigger, args, kwargs):
    """Remembers a thing.

    Example::

        !remember foobar is a madeup name

    Given the syntax above, things you need to know:

    1. the bot requires 3 words or more (``!remember`` is omitted)
    2. the first word is a keyword
    3. the second word **must** use `is`, otherwise the syntax is incorrect
    4. the rest of the words is the content of a keyword
    """
    if len(args) > 2 and args[1] == "is":
        nick = msg.nick
        slug = args[0]

        remember = Remember()
        remember.channel = msg.channel
        remember.user = nick
        remember.slug = slug
        remember.content = " ".join(args[2:])
        ctx.db.session.add(remember)

        try:
            ctx.db.session.commit()
            out = "thx {0}, it's good to know".format(nick)
        except IntegrityError:
            # unique constraint is violated, bail out then
            ctx.db.session.rollback()
            out = (
                "sorry {0}, {1} is exist; "
                "please try using another keyword".format(nick, slug)
            )
        finally:
            msg.reply(out)


@keyword("whatis")
def what(ctx, msg, trigger, args, kwargs):
    """Finds a thing.

    Let's say a user with `janedoe` needs to know about `foobar` thing,
    the appropriate syntax would be::

        !whatis foobar

    Given the syntax above, things you need to know:

    1. the bot requires exactly 1 word (``!whatis`` is omitted)
    2. the only recognized word **must not** use any whitespace character
    """
    if len(args) == 1:
        slug = args[0]
        channel = msg.channel
        nick = msg.nick

        content = ctx.db.session.query(Remember).filter_by(
            slug=slug, channel=channel).value(Remember.content)

        if not content:
            out = "sorry {0}, i don't know what {1} is".format(nick, slug)
        else:
            out = "{0}, {1} is {2}".format(nick, slug, content)
        msg.reply(out)


@keyword("tell")
def tell(ctx, msg, trigger, args, kwargs):
    """Finds a thing.

    In contrast with :func:`what`, this function
    returns the content (if any) to the targeted user.

    Let's say a user with `janedoe` nickname wants to inform
    another user with `johndoe` nickname about `foobar` thing,
    the appropriate syntax would be::

        !tell johndoe about foobar

    Given the syntax above, things you need to know:

    1. the bot requires exactly 3 words (``!tell`` is omitted)
    2. the first word is user's nickname
    3. the second word **must** use `about`, otherwise the syntax is incorrect
    4. the last word is a keyword stored in database backend
    """
    if len(args) == 3 and args[1] == "about":
        slug = args[2]
        channel = msg.channel
        nick = msg.nick

        content = ctx.db.session.query(Remember).filter_by(
            slug=slug, channel=channel).value(Remember.content)

        if not content:
            out = "sorry {0}, i don't know what {1} is".format(nick, slug)
        else:
            # change the nick to use target instead,
            # not the one who calls this command
            nick = args[0]
            out = "{0}, {1} is {2}".format(nick, slug, content)
        msg.reply(out)


@keyword("forget")
def forget(ctx, msg, trigger, args, kwargs):
    """Forgets a thing.

    Example::

        !forget foobar
    """
    if len(args) == 1:
        slug = args[0]
        channel = msg.channel

        ctx.db.session.query(Remember).filter_by(
            slug=slug, channel=channel).delete()
        ctx.db.session.commit()

        # no matter the row is successfully deleted or not,
        # this always be executed
        msg.reply("ok")


@observe("IRC_ONCONNECT")
def register_models(ctx):
    """Registers all classes that inherit base ``Model`` class.
    """
    Model.metadata.create_all(ctx.db.engine)
