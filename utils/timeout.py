def raise_timeout(timeout_message):
    def message_decorator(func):
        def decorated_func(*args, **kwargs):
            if func(*args, **kwargs) == "TIMED OUT":
                raise Exception(timeout_message)
        return decorated_func
    return message_decorator