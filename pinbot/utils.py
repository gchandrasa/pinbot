from functools import wraps


def hint(usage):
    def hinted(func):
        @wraps(func)
        def wrapped(ctx, msg, trigger, args, kwargs):
            if "h" in kwargs or "help" in kwargs:
                usage_str = usage.replace("{{prefix}}", ctx.triggers.prefix)
                usage_str = usage_str.replace("{{trigger}}", trigger)
                msg.reply("{0} :: {1}".format(trigger, usage_str))
                return
            return func(ctx, msg, trigger, args, kwargs)
        return wrapped
    return hinted
