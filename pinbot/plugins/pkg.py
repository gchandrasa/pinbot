from pyaib.plugins import keyword

from ..utils import hint

REMOTES = {
    "pypi": "https://pypi.python.org/pypi?%3Aaction=search&term={pkg}",
    "github": "https://github.com/search?l=Python&q={pkg}&type=Repositories",
    "bitbucket": "https://bitbucket.org/repo/all/relevance?name={pkg}&language=python",  # NOQA
}

DEFAULT_REMOTE = REMOTES["pypi"]
REMOTE_KEYS_STR = "|".join(REMOTES.keys())


@hint(
    "finds a Python package | "
    "usage: {{prefix}}{{trigger}} <name> [--remote=(%s)]" % REMOTE_KEYS_STR
)
@keyword("pkg")
def search(ctx, msg, trigger, args, kwargs):
    """Finds a python package.
    """

    if len(args) == 1:
        remote = kwargs.get("remote")
        remote_url = REMOTES.get(remote, DEFAULT_REMOTE)
        msg.reply("please have a look at {0}".format(
            remote_url.format(pkg=args[0])
        ))
