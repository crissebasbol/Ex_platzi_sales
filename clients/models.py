import uuid


class Client:

    def __init__(self, name, company, email, position, uid=None):
        self.name = name
        self.company = company
        self.email = email
        self.position = position
        self.uid = uid or uuid.uuid4()

    def to_dict(self):
        # var --> nos peermite acceder a una representtación como diccionario de nuestro objeto
        return vars(self)

    @staticmethod
    def schema():
        return ["name", "company", "email", "position", "uid"]
