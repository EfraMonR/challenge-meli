class DatabasePersistenceEntity:
    def __init__(self, host: str, username: str, password: str, port: str, id: int = None):
        self.id = id
        self.host = host
        self.username = username
        self.password = password
        self.port = port