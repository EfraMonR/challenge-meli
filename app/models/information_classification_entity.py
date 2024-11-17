class InformationClassificationEntity:
    def __init__(self, id: int, information_type: str, information_expression: str):
        self.id = id
        self.information_type = information_type
        self.information_expression = information_expression