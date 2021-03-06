import os
from unittest import TestCase

from BEM import deoverlap


class testDeoverlap(TestCase):
    def setUp(self):
        self.path = os.path.dirname(__file__)
        self.unsorted_filename = os.path.join(self.path, "test_deoverlap.txt")
        unsorted_file = open(self.unsorted_filename, "r").readlines()
        self.unsorted_elements = [x.split() for x in unsorted_file]

        sorted_file = open(os.path.join(
            self.path, "test_deoverlap_sorted.txt"), "r").readlines()
        self.sorted_elements = [x.split() for x in sorted_file]

        self.unsorted_single_element = [
            ["38.8", "81.25", "PegasusA", "210",
             "710", "+", "4e", "138", "638"]]
        self.single_element = [
            ["38.8", "81.25", "PegasusA", "210", "710",
             "+", "4e", "138", "638"]]
        self.unsorted_and_cut_elements = [
            ['38.8', '81.25', 'PegasusA', '210', '710',
             '+', '4e', '138', '638'],
            ['34.8', '81.25', 'PegasusA', '2107', '2139',
             '+', '4e', '138', '170'],
            ['34.3', '88.89', 'PegasusA', '1613', '1639',
             '+', '4e', '71', '97'],
            ['29.7', '69.49', 'PegasusA', '711', '757',
             '+', '4e', '910', '956']]

    def test_adjust_score(self):
        """Test if the score is adjusting properly."""
        # Turn the string into ints
        for pos in [3, 4, 7, 8]:
            self.single_element[0][pos] = int(self.single_element[0][pos])
        # If the element had double length, the actual score is half
        self.assertEqual(
            deoverlap.adjust_score(self.single_element[0], 1000)[0], "19.4")

    def test_sort_by_score(self):
        """Check if the sorting is doing the sort by score"""
        deoverlap.sort_by_score(self.unsorted_elements)
        assert self.unsorted_elements ==\
            self.sorted_elements

    def test_sort_by_score_one_element(self):
        """Check the sorting of only one element, should return the same"""
        deoverlap.sort_by_score(self.unsorted_single_element)
        assert self.unsorted_single_element == self.single_element

    def test_int_vs_str(self):
        """Test the mutual transformation from ints to str and viceversa."""
        assert deoverlap.int_vs_str(self.single_element[0]) == \
            ["38.8", "81.25", "PegasusA", 210, 710, "+", "4e", 138, 638]
        assert ["38.8", "81.25", "PegasusA", "210",
                "710", "+", "4e", "138", "638"] == \
            deoverlap.int_vs_str(self.single_element[0], to_str=True)

    def test_cut_element_by_other_head(self):
        """Test the cut of element if the head is overlapping"""
        overlapped_head = ['37.4', '69.49', 'PegasusA', '699', '757',
                           '+', '4e', '898', '956']

        assert deoverlap.cut_element_by_other(
            self.single_element[0], overlapped_head) == \
            ['29.7', '69.49', 'PegasusA', '711', '757', '+',
             '4e', '910', '956']

    def test_cut_element_by_other_tail(self):
        """Test the cut of element if the tail is overlapping"""
        overlapped_tail = ['37.4', '69.49', 'PegasusA', '1', '500',
                           '+', '4e', '400', '900']

        assert deoverlap.cut_element_by_other(
            self.single_element[0], overlapped_tail) == \
            ['15.6', '69.49', 'PegasusA', '1', '209', '+',
             '4e', '400', '609']

    def test_cut_element_by_other_embedded(self):
        """Test the cut of element if the head is overlapping"""
        overlapped_embed = ['37.4', '69.49', 'PegasusA', '211',
                            '709', '+', '4e', '898', '956']

        assert deoverlap.cut_element_by_other(
            self.single_element[0], overlapped_embed) == []

    def test_cut_elements_one_element(self):
        """Test the cut of only one element. Should return the same element"""
        assert deoverlap.cut_elements(self.single_element, return_list=[]) ==\
            self.single_element

    def test_load_input_file(self):
        """Test the correct loading and processing of an output file"""
        # load_input_file does a cut_element that removes elements under a
        # MIN_LENGTH, so self.unsorted_elements may have more elements.
        deoverlapped = deoverlap.load_input_file(self.unsorted_filename)
        assert deoverlapped == self.unsorted_and_cut_elements
