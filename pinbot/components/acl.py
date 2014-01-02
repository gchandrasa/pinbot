from functools import wraps

from pyaib.components import component_class


@component_class("acl")
class ACL(object):
    def __init__(self, ctx, config):
        self.permissions = config.get("permissions", {})

    def allowed(self, trigger, chan, nick):
        channel = self.permissions.get(chan, {})
        cmd = channel.get(trigger, {})

        # denies nick in `deny` list then bail out
        # `deny` is the main priority here
        denied_nicks = set(cmd.get("deny", []))
        if "*" in denied_nicks or nick in denied_nicks:
            return False

        # allows nick in `allow` list
        allowed_nicks = set(cmd.get("allow", []))
        if "*" in allowed_nicks or nick in allowed_nicks:
            return True

        # default to deny all nicks if trigger is specified
        return False if cmd else True


def icanhaz(func):
    @wraps(func)
    def wrapped(ctx, msg, trigger, args, kwargs):
        nick = msg.nick
        if not ctx.acl.allowed(trigger, msg.channel, nick):
            msg.reply("sorry {0}, you're not allowed".format(nick))
            return
        return func(ctx, msg, trigger, args, kwargs)
    return wrapped
