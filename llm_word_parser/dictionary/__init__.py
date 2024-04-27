from typing import Optional


class Dictionary:
    def __init__(self, id: Optional[int], name: str, path: str, active: bool = True):
        self.id = id
        self.name = name
        self.path = path
        self.active = active
