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
        self.score = kwargs.get("score", 0.0)

    def _same_family(self, other):
        """Return True if self and other are the same match family."""
        return ((self.query_name == other.query_name) and
                (self.subject_name == other.subject_name and
                 self.orientation == other.orientation and
                 self.chromosome == other.chromosome))

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
        """Return a Match resulting from adding two matches."""
        if self._same_family(other):

            query = (min(self.query[0], other.query[0]),
                     max(self.query[1], other.query[1]))
            subject = (min(self.subject[0], other.subject[0]),
                       max(self.subject[1], other.subject[1]))
            # TODO: This is a rough approach. Here we need the gap open, extend
            # and mismatches corrections.
            score = ((self.score + other.score) / abs(max(query) - min(query)))

            return Match(query_name=self.query_name,
                         subject_name=self.subject_name,
                         self_chromosome=self.chromosome,
                         orientation=self.orientation,
                         score=score,
                         query=query,
                         subject=subject)
        else:
            raise ValueError("Matches cannot be added.")
