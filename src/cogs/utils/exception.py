class BadRequest(Exception):
    """
    Raised when the request is not valid.
    """

    pass


class Ratelimited(Exception):
    """
    Raised when the bot is ratelimited.
    """

    pass
