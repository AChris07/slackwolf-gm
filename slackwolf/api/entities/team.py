class Team:
    """Team entity"""

    def __init__(self, id: str = '', domain: str = ''):
        self.id = id
        self.domain = domain
        self.channels = []
