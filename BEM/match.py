class Match(object):
    '''Represent a match between a query sequence and a subject.'''
    def __init__(self, **kwargs):
        self.query = kwargs.get("query", (0, 0))
        self.subject = kwargs.get("subject", (0, 0))
        self.chromosome = kwargs.get("chromosome", "")
        self.orientation = kwargs.get("orientation", "+") #Or "C"

    def __eq__(self, other):
        return (self.query[0] == other.query[0]) and \
                (self.subject[0] == other.subject[0])

    def __gt__(self, other):
        return (self.query[0] > other.query[0]) and \
                (self.subject[0] > other.subject[0])

    def __lt__(self, other):
        return (self.query[0] < other.query[0]) and \
                (self.subject[0] < other.subject[0])
    
    #TODO:
    # Implement __add__ to join two matches?
