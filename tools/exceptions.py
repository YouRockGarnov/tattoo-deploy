

class ManualException(BaseException):
    def __init__(self, mes_to_user):
        self._message = mes_to_user

    @property
    def message(self):
        return self._message

