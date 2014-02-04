"""Object to represent each match from a Blast hit."""


class Match(object):

    """Represent a match between a query sequence and a subject."""

    def __init__(self, **kwargs):
        self.query_name = kwargs.get("query_name", "")
        self.subject_name = kwargs.get("subject_name", "")
        self.query = kwargs.get("query", (0, 0))
        self.subject = kwargs.get("subject", (0, 0))
        self.chromosome = kwargs.get("chromosome", "")
        self.orientation = kwargs.get("orientation", "+")  # Or "C"

    def _same_family(self, other):
        """Return True if self and other are the same match family."""
        return ((self.query_name == other.query_name) and
                (self.subject_name == other.subject_name))

    def __eq__(self, other):
        return ((self.query[0] == other.query[0]) and
                (self.subject[0] == other.subject[0]) and
                (self._same_family(other)))

    def __gt__(self, other):
        return ((self.query[0] > other.query[0]) and
                (self.subject[0] > other.subject[0]) and
                (self._same_family(other)))

    def __lt__(self, other):
        return ((self.query[0] < other.query[0]) and
                (self.subject[0] < other.subject[0]) and
                (self._same_family(other)))

    def __add__(self, other):
        pass
