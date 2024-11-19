class UserDataEntity:
    def __init__(self, username: str, password: str, id: int = None):
        self.id = id
        self.username = username
        self.password = password