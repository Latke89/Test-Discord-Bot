class Condition:
    _id: str
    index: str
    name: str
    description: [str]
    url: str

    def __init__(self, id: str, index: str, name: str, desc: [str], url: str):
        self._id = id
        self.index = index
        self.name = name
        self.description = desc
        self.url = url

