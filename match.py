class Match(object):
    '''Represent a match between a query sequence and a subject.'''
    def __init__(self):
        self.query = (0, 0)
        self.subject = (0, 0)
        self.chromosome = ""
        self.orientation = "+" #Or "C"
