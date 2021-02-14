from department_app.domain.interfaces import IDatabase


class DatabaseService:

    def __init__(self, database: IDatabase):
        self.db = database