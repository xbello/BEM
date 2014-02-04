"""Tests for the match object."""


from unittest import TestCase

from BEM import match


class testMatch(TestCase):
    def setUp(self):
        self.match1 = match.Match()
        self.match2 = match.Match()
        self.match3 = match.Match(query_name="Query_Name",
                                  subject_name="Subject_Name",
                                  query=(10, 1000),
                                  subject=(5000, 5990),
                                  orientation="C",
                                  chromosome="contig12345")

    def test_loading_defaults(self):
        """Test that match object can be created empty."""
        self.assertEqual(self.match1.query, (0, 0))
        self.assertEqual(self.match1.subject, (0, 0))
        self.assertEqual(self.match1.orientation, "+")

    def test_loading_match(self):
        """Test that match object can handle assignment on creation."""
        self.assertEqual(self.match3.query, (10, 1000))
        self.assertEqual(self.match3.subject, (5000, 5990))
        self.assertEqual(self.match3.orientation, "C")

    def test_eq(self):
        """Test that two match objects are equal to join.

        (Starts in the same point).

        """
        self.match1.query_name = self.match2.query_name = "Query_1"
        self.match1.subject_name = self.match2.subject_name = "Subject_1"
        self.assertTrue(self.match1 == self.match2)
        self.assertFalse(self.match1 == self.match3)

    def test_lt(self):
        """Test that one match objects is lower than other (starts before)."""
        self.match2.query = (10, 10)
        self.match2.subject = (10, 10)
        self.assertTrue(self.match1 < self.match2)
        self.assertFalse(self.match2 < self.match1)
        # If matches are not from the same family, return false
        self.assertFalse(self.match1 < self.match3)

    def test_gt(self):
        """Test that one match objects is greater than other (starts after)."""
        self.match1.query = (20, 20)
        self.match1.subject = (20, 20)
        self.assertFalse(self.match1 < self.match2)
        self.assertTrue(self.match2 < self.match1)
        # If matches are not from the same family, return false
        self.assertFalse(self.match3 > self.match1)
