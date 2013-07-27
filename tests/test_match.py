import match

class testMatch():
    def setUp(self):
        self.match1 = match.Match()
        self.match2 = match.Match()
        self.match3 = match.Match(query = (10, 1000),
            subject = (5000, 5990),
            orientation = "C",
            chromosome = "contig12345")

    def test_loading_defaults(self):
        """Test that match object can be created empty"""
        assert self.match1.query == (0, 0)
        assert self.match1.subject == (0, 0)
        assert self.match1.orientation == "+"
    
    def test_loading_match(self):
        """Test that match object can handle assignment on creation"""
        assert self.match3.query == (10, 1000)
        assert self.match3.subject == (5000, 5990)
        assert self.match3.orientation == "C"
    
    def test_eq(self):
        """Test that two match objects are equal to join (starts in the same
        point"""
        assert self.match1 == self.match2

    def test_lt(self):
        """Test that one match objects is lower than other (starts before)"""
        assert self.match1 < self.match3

    def test_gt(self):
        """Test that one match objects is greater than other (starts after)"""
        assert self.match3 > self.match1
