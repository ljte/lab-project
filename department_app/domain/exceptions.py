class RecordAlreadyExistsError(Exception):

    def __init__(self, record):
        self.message = "`%s` already exists"
        super().__init__(self.message % record)
