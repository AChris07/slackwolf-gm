class Channel:
    """Channel model"""

    def __init__(self, id: str = '', name: str = ''):
        self.id = id
        self.name = name
        self.game = None
