class RecordAlreadyExistsError(Exception):
    def __init__(self, record):
        self.message = "`%s` already exists"
        super().__init__(self.message % record)


class InvalidModelError(Exception):
    pass


class InvalidRecordError(Exception):
    pass


class ModelNotFoundError(Exception):
    pass


class RecordNotFoundError(Exception):
    pass
