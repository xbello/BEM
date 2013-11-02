import os

from BEM import sort_by_element

class testSortParsed():
    def setUp(self):
        self.path = os.path.dirname(__file__)
        self.input_filename = os.path.join(
            self.path, "small_blastn_output.txt")
        self.output_filename = os.path.join(
            self.path, "small_blastn_sorted_by_element.txt")

    def test_check_sorting(self):
        input_sorted = sort_by_element.sort_file(self.input_filename)
        output_lines = open(self.output_filename, "r").readlines()
        
        input_values = []

        for line in input_sorted:
            input_values.append(" ".join(line) + "\n")

        assert input_values == output_lines
