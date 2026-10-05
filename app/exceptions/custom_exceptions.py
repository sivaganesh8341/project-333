class DuplicateNameException(Exception):
    def __init__(self, name: str):
        self.name = name

class NotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name
