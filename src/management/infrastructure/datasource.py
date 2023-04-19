from contextlib import contextmanager, AbstractContextManager
from sqlalchemy import MetaData, URL, create_engine, Connection


metadata = MetaData()


@contextmanager
def _ConnWrapper(connection: Connection):
    try:
        yield connection
    except Exception:
        connection.rollback()
    else:
        connection.commit()
    finally:
        connection.close()


class Database:
    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        dialect: str,
        driver: str,
    ) -> None:

        self.url = URL.create(
            f"{dialect}+{driver}",
            username=user,
            password=password,
            host=host,
            port=port,
            database=database,
        )
        self.engine = create_engine(self.url)

    def conn(self) -> AbstractContextManager[Connection]:
        return _ConnWrapper(self.engine.connect())
