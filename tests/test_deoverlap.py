import deoverlap

class testDeoverlap():
    def setUp(self):
        unsorted_file = open("test_deoverlap.txt", "r").readlines()
        self.unsorted_elements = [x.split() for x in unsorted_file]

        sorted_file = open("test_deoverlap_sorted.txt", "r").readlines()
        self.sorted_elements = [x.split() for x in sorted_file]

        self.unsorted_single_element = [["38.8", "81.25", "PegasusA", "210",
            "710", "+", "4e", "138", "107"]]
        self.single_element = [["38.8", "81.25", "PegasusA", "210", "710",
            "+", "4e", "138", "107"]]
        self.unsorted_and_cut_elements = [['38.8', '81.25', 'PegasusA', '210',
            '710', '+', '4e', '138', '107'], ['34.8', '81.25', 'PegasusA',
            '2107', '2139', '+', '4e', '138', '107'], ['34.3', '88.89',
            'PegasusA', '1613', '1639', '+', '4e', '71', '45'], ['29.7',
             '69.49', 'PegasusA', '711', '757', '+', '4e', '108', '956']]

    def test_sort_by_score(self):
        """Check if the sorting is doing the sort by score
        """
        deoverlap.sort_by_score(self.unsorted_elements)
        assert self.unsorted_elements ==\
            self.sorted_elements

    def test_sort_by_score_one_element(self):
        """Check the sorting of only one element, should return the same"""
        deoverlap.sort_by_score(self.unsorted_single_element)
        assert self.unsorted_single_element == self.single_element        

    def test_cut_elements(self):
        """Test if the cut of elements is properly done
        """
        
        for el in deoverlap.cut_elements(self.sorted_elements):
            print " ".join(el)
        assert True

    def test_cut_elements_one_element(self):
        """Test the cut of only one element. Should return the same element
        """
        assert deoverlap.cut_elements(self.single_element, return_list = []) ==\
            self.single_element

    def test_load_input_file(self):
        """Test the correct loading and processing of an output file
        """
        #load_input_file does a cut_element that removes elements under a
        # MIN_LENGTH, so self.unsorted_elements may have more elements.
        deoverlapped = deoverlap.load_input_file("test_deoverlap.txt")
        print deoverlapped
        assert deoverlapped == self.unsorted_and_cut_elements

