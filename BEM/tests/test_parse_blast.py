import os

from nose.tools import raises
from BEM import parse_blast

class testParseBlastn():
    def setUp(self):
        self.path = os.path.dirname(__file__)
        self.blast_output = os.path.join(
            self.path, "small_blastn_search.txt")
        self.HSP_output = open(os.path.join(
            self.path, "small_blastn_HSP.txt"), "r").readlines()
        self.parsed_output = os.path.join(
            self.path, "small_blastn_output.txt")
        self.blast_expected = open(self.parsed_output, "r").readlines()

    def test_blast_table_consumer(self):
        line = 0
        for i in parse_blast.blast_table_consumer(self.blast_output):
            assert i == eval(self.HSP_output[line])
            line += 1

    def test_blast_output(self):
        line = 0
        for i in parse_blast.blast_table_consumer(self.blast_output):
            assert parse_blast.write_parsed(i) ==\
                self.blast_expected[line].strip()
            line += 1

    def test_selection_of_strategy_ncbiblast(self):
        """Test the selection of the strategy from the output.
        """
        blast_line = ['BEL1-I_AG', '3293e', '78.95', '38', '8', '0', '1429',
            '1466', '798', '761', '0.26', '35.9']
        assert parse_blast.select_blaster_keys(blast_line) == \
            parse_blast.BLAST_HSP_KEYS

    def test_selection_of_strategy_wublast(self):
        """Test the selection of the strategy from the output.
        """
        wublast_line = ['1129g', '1129g', '0.', '1', '2787.80', '18540',
            '3708', '3708', '3708', '0', '100.00', '100.00', '0', '0', '0',
            '0', '+1', '1', '3708', '+1', '1', '3708']
        assert parse_blast.select_blaster_keys(wublast_line) == \
            parse_blast.WUBLAST_HSP_KEYS
    
    @raises(Exception)    
    def test_selection_of_strategy_wrong_blast(self):
        """Test the selection of the strategy from the output.
        """
        wrong_line = ['This', 'is', 'wrong']
        parse_blast.select_blaster_keys(wrong_line)
