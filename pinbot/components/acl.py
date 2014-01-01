from functools import wraps

from pyaib.components import component_class


@component_class("acl")
class ACL(object):
    def __init__(self, ctx, config):
        self.permissions = config.get("permissions", {})

    def allowed(self, trigger, chan, nick):
        channel = self.permissions.get(chan, {})
        cmd = channel.get(trigger, {})

        # allows nick in `allow` list
        if nick in set(cmd.get("allow", [])):
            return True

        # denies nick in `deny` list
        if nick in set(cmd.get("deny", [])):
            return False

        # default to allows all nicks
        return True


def icanhaz(func):
    @wraps(func)
    def wrapped(ctx, msg, trigger, args, kwargs):
        nick = msg.nick
        if not ctx.acl.allowed(trigger, msg.channel, nick):
            msg.reply("sorry {0}, you're not allowed".format(nick))
            return
        return func(ctx, msg, trigger, args, kwargs)
    return wrapped
