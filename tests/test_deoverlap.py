import deoverlap

class testDeoverlap():
    def setUp(self):
        unsorted_file = open("test_deoverlap.txt", "r").readlines()
        self.unsorted_elements = [x.split() for x in unsorted_file]

        sorted_file = open("test_deoverlap_sorted.txt", "r").readlines()
        self.sorted_elements = [x.split() for x in sorted_file]

    def test_sort_by_score(self):
        """Check if the sorting is doing the sort by score
        """
        deoverlap.sort_by_score(self.unsorted_elements)
        assert self.unsorted_elements ==\
            self.sorted_elements

    def test_cut_elements(self):
        """Test if the cut of elements is propperly done
        """

        deoverlap.cut_elements(self.sorted_elements)
        assert True

