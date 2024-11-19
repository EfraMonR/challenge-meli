class InformationClassificationEntity:
    def __init__(self, id: int, information_type: str, information_expression: str, user_id: int):
        self.id = id
        self.information_type = information_type
        self.information_expression = information_expression
        self.user_id = user_id